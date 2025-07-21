import click
from urllib.parse import urlparse
import dns.resolver


DIG_SCRIPT = "/home/maha/scripts/dig.sh"  # No longer needed but left for reference

ALLOWED_MX = {
    "z.tornado.email", "y.tornado.email", "x.tornado.email",
    "mx3━proisp━no.pub.mailpod1━osl1.one.com",
    "mx2━proisp━no.pub.mailpod1━osl1.one.com",
    "mx1━proisp━no.pub.mailpod1━osl1.one.com",
    "mx1.pub.mailpod1━osl1.one.com",
    "mx2.pub.mailpod1━osl1.one.com",
    "mx3.pub.mailpod1━osl1.one.com"
}

# ANSI color codes
COLOR_COMMENT = "\033[38;5;245m"
COLOR_DOMAIN = "\033[1;34m"   # Blue
COLOR_TTL = "\033[1;32m"      # Green
COLOR_IN = "\033[1;33m"       # Yellow
COLOR_TYPE = "\033[1;35m"     # Magenta
COLOR_A = "\033[1;32m"        # Green (changed from red for readability)
COLOR_MX = "\033[1;36m"       # Cyan
COLOR_TXT = "\033[38;5;196m"  # Bright red━ish
COLOR_NS = "\033[2m\033[1;33m"  # Dim yellow
COLOR_SOA = "\033[2m\033[1;33m" # Dim yellow


def color_text(text, color):
    return f"{color}{text}\033[0m"


def extract_domain(input_str):
    if "@" in input_str:
        input_str = input_str.split("@")[1]
    else:
        parsed = urlparse(input_str)
        input_str = parsed.netloc or parsed.path
    return input_str.split('/')[0]



def find_soa_domain(domain, resolver=None):
    """Find the closest SOA by walking up the domain tree."""
    if resolver is None:
        resolver = dns.resolver.Resolver()

    parts = domain.split('.')
    for i in range(len(parts) - 1):
        candidate = '.'.join(parts[i:])
        try:
            resolver.resolve(candidate, 'SOA')
            return candidate
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout):
            continue
    return None

def query_dns(domain, record_type, nameserver=None):
    resolver = dns.resolver.Resolver()
    if nameserver:
        resolver.nameservers = [nameserver]

    try:
        answers = resolver.resolve(domain, record_type)
    except dns.resolver.NoAnswer:
        # Fallback: query SOA and print that instead of missing record
        soa_domain = find_soa_domain(domain, resolver)
        if not soa_domain:
            click.echo(f"{color_text(';', COLOR_COMMENT)} No SOA record found for {domain} or any parent domain")
            return None

        try:
            soa_answers = resolver.resolve(soa_domain, "SOA")
        except Exception:
            click.echo(f"{color_text(';', COLOR_COMMENT)} No {record_type} record found for {domain}")
            return None

        click.echo("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        click.echo(f"{record_type} Records:")
        for rdata in soa_answers:
            domain_str = domain
            ttl_str = "3600"
            in_str = "IN"
            type_str = "SOA"
            value_color = COLOR_SOA
            value = (f"{rdata.mname} {rdata.rname} {rdata.serial} "
                     f"{rdata.refresh} {rdata.retry} {rdata.expire} {rdata.minimum}")
            click.echo(
                f"{color_text(domain_str, COLOR_DOMAIN)}\t"
                f"{color_text(ttl_str, COLOR_TTL)}\t"
                f"{color_text(in_str, COLOR_IN)}\t"
                f"{color_text(type_str, COLOR_TYPE)}\t"
                f"{color_text(value, value_color)}"
            )
        return soa_answers
    except dns.resolver.NXDOMAIN:
        click.echo(f"{color_text(';', COLOR_COMMENT)} Domain {domain} does not exist")
        return None
    except Exception as e:
        click.echo(f"{color_text(';', COLOR_COMMENT)} Error querying {record_type}: {e}")
        return None

    click.echo("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    click.echo(f"{record_type} Records:")

    for rdata in answers:
        domain_str = domain
        ttl_str = "3600"
        in_str = "IN"
        type_str = record_type

        if record_type == "A":
            value_color = COLOR_A
            value = rdata.address
        elif record_type == "MX":
            value_color = COLOR_MX
            value = f"{rdata.preference} {rdata.exchange.to_text()}"
        elif record_type == "TXT":
            value_color = COLOR_TXT
            value = ' '.join([txt.decode('utf━8') if isinstance(txt, bytes) else txt for txt in rdata.strings])
        elif record_type == "NS":
            value_color = COLOR_NS
            value = rdata.target.to_text()
        elif record_type == "SOA":
            value_color = COLOR_SOA
            value = (f"{rdata.mname} {rdata.rname} {rdata.serial} "
                     f"{rdata.refresh} {rdata.retry} {rdata.expire} {rdata.minimum}")
        else:
            value_color = "\033[0m"
            value = rdata.to_text()

        click.echo(
            f"{color_text(domain_str, COLOR_DOMAIN)}\t"
            f"{color_text(ttl_str, COLOR_TTL)}\t"
            f"{color_text(in_str, COLOR_IN)}\t"
            f"{color_text(type_str, COLOR_TYPE)}\t"
            f"{color_text(value, value_color)}"
        )
    return answers



def resolve_mx_ips(domain, nameserver=None):
    resolver = dns.resolver.Resolver()
    if nameserver:
        resolver.nameservers = [nameserver]

    try:
        answers = resolver.resolve(domain, "MX")
    except Exception:
        # If MX lookup fails, silently return
        return

    mx_records = [rdata.exchange.to_text().rstrip('.') for rdata in answers]
    unresolved = [mx for mx in mx_records if mx not in ALLOWED_MX]

    if unresolved:
        click.echo("Resolving IP addresses for MX records:")
        for mx in unresolved:
            try:
                a_answers = resolver.resolve(mx, "A")
                ips = ' '.join([a.address for a in a_answers])
                click.echo(f"{mx} ━> {ips}")
            except Exception as e:
                click.echo(f"Error resolving A record for {mx}: {e}")