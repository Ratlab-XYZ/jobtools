import click

from check_helper import extract_domain, query_dns, resolve_mx_ips
from resetpw import send_password_reset
from connect import ssh_connect
from cheat import cheat_sheet
from org import get_org_details, get_org_details_short
from updater import check_for_update_notification, perform_update, CURRENT_VERSION


VALID_BRANDS = "fastname", "syse", "proisp", "uniweb"

@click.group()
@click.version_option(version=CURRENT_VERSION)
def cli():
    check_for_update_notification()


@cli.command()
def update():
    """Download and install the latest version."""
    perform_update()


@cli.command()
@click.argument('target')
@click.option('--nameserver', '-n', help='Optional nameserver to query against')
def check(target, nameserver):
    """
    Check DNS records for a domain, email, or URL.

    uw check [DOMAIN] -n/--nameserver 1.1.1.1
    """
    domain = extract_domain(target)

    for record in ["A", "CNAME", "MX", "TXT", "NS"]:
        query_dns(domain, record, nameserver)

    click.echo("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    resolve_mx_ips(domain)


@cli.command()
@click.argument('org_number')
def ehf(org_number):
    """
    Check EHF status for an organization number.

    uw ehf [ORG_NUMBER]
    """
    get_org_details_short(org_number)

@cli.command()
@click.argument('email')
@click.argument('brand')
def resetpw(email, brand):
    """ 
    Send Reset password mail to any customer for the brands

    uw resetpw [EMAIL] [BRAND]
    """
    if brand not in VALID_BRANDS:
        click.echo(f"Error: {brand} is not a valid brand")
        raise SystemExit(1)
    send_password_reset(brand, email)


@cli.command()
@click.argument("cluster")
@click.option("--password", '-p', help='Optional password if not the default one')
def connect(cluster, password):
    """
    ssh into to clustered webhotel
    
    uw connect [CLUSTER_USERNAME] -p/--password [password] 
    """
    if not password:
        ssh_connect(cluster)
    else:
        ssh_connect(cluster, password)


@cli.command()
@click.argument("search_word")
def cheat(search_word):
    """
    Cheat sheet

    uw cheat [SEARCH_WORD]

    """
    for line in cheat_sheet(search_word):
        print(line)


@cli.command()
@click.argument("org_number")
def org(org_number):
   """
   Get org details
   """
   get_org_details(org_number)


if __name__ == "__main__":
    cli()
