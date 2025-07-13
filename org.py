import requests

from ehf import get_ehf

URL = "https://data.brreg.no/enhetsregisteret/api/enheter/"

def get_org_details(org_number, search_option=None):

    response = requests.get(f"{URL}{org_number}").json()
    ehf = get_ehf(org_number)


    print(f"Navn: {response.get('navn')}")
    print(f"Organisasjonsnummer: {response.get('organisasjonsnummer')}")
    print(f"Organisasjonsform: {response['organisasjonsform']['beskrivelse']} ({response['organisasjonsform']['kode']})")
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
    
