import requests
import click


def get_ehf(org_number):

    """
    Check EHF status for an organization number.

    uw ehf [ORG_NUMBER]
    """
    url = f"https://directory.peppol.eu/public/locale-en_US/menuitem-search?q={org_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        click.echo(f"Failed to fetch data: {e}")
        raise SystemExit(1)

    html = response.text

    # Check if entity is found
    if "Found 1 entity matching" in html:
        return f"{org_number} Can receive EHF"
    else:
        return f"{org_number} Can not receive EHF"