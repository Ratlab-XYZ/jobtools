import requests
import click

URL = "https://data.brreg.no/enhetsregisteret/api/enheter/"


def get_ehf(org_number):
    """
    Check EHF status for an organization number using elma.tunnel.ratlab.xyz,
    falling back to Peppol if necessary.
    """
    tunnel_url = f"https://elma.tunnel.ratlab.xyz/{org_number}"
    peppol_url = f"https://directory.peppol.eu/search/1.0/json?q={org_number}"

    # Try elma.tunnel.ratlab.xyz first
    try:
        response = requests.get(tunnel_url, timeout=5)
        response.raise_for_status()
        data = response.json() 

        
        # Expecting JSON response
        # Example JSON: {"orgnr": "811928682", "can_receive_ehf": 1, "org_name": "KEBAKS AS"}

        can_receive = data.get("can_receive_ehf")
        if can_receive == 1:
            return {"org_number": org_number, "navn": data.get("org_name"), "ehf": True}
        else:
            return {"org_number": org_number, "navn": data.get("org_name"), "ehf": False}
    except (requests.RequestException, ValueError, KeyError):
        # On any error (HTTP, JSON parsing, missing keys), fallback to Peppol
        click.echo("Fallback to Peppol directory...")

    # Fallback to Peppol JSON endpoint
    try:
        response = requests.get(peppol_url, timeout=10)
        peppol_data = response.json()
    except requests.RequestException as e:
        click.echo(f"Failed to fetch data from Peppol: {e}")
        raise SystemExit(1)

    matches = peppol_data.get("matches", [])
    if matches:
        entity_name = matches[0]["entities"][0]["name"][0]["name"] if matches[0].get("entities") else "Ukjent"
        return {"org_number": org_number, "navn": entity_name, "ehf": True}
    else:
        response = requests.get(f"{URL}{org_number}").json()
        return {"org_number": org_number, "navn": response.get('navn'), "ehf": False}



def get_org_details(org_number):

    response = requests.get(f"{URL}{org_number}").json()
    ehf = get_ehf(org_number)


    print(f"Navn: {response.get('navn')}")
    print(f"Organisasjonsnummer: {response.get('organisasjonsnummer')}")
    #print(f"Organisasjonsform: {response['organisasjonsform']['beskrivelse']} ({response['organisasjonsform']['kode']})")
    print(f"EHF: {'Nei' if 'not' in ehf else 'Ja'}")
    print()

    print("Postadresse:")
    post = response.get('postadresse', {})
    for linje in post.get('adresse', []):
        print(f"  {linje}")
    print(f"  {post.get('postnummer')} {post.get('poststed')}")
    print()

    print("Forretningsadresse:")
    for linje in response['forretningsadresse'].get('adresse', []):
        print(f"  {linje}")
    print(f"  {response['forretningsadresse']['postnummer']} {response['forretningsadresse']['poststed']}")
    print()

    print("Status:")
    print(f"  Konkurs: {'Ja' if response.get('konkurs') else 'Nei'}")
    print(f"  Under avvikling: {'Ja' if response.get('underAvvikling') else 'Nei'}")
    print(f"  Tvangsavvikling/-oppløsning: {'Ja' if response.get('underTvangsavviklingEllerTvangsopplosning') else 'Nei'}")
    
def get_org_details_short(org_number):
    ehf = get_ehf(org_number)

    print(f"Navn: {ehf["navn"]}")
    print(f"Organisasjonsnummer: {ehf["org_number"]}")
    print(f"EHF: {'Ja' if ehf["ehf"] else 'Nei'}")



