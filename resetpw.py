import requests
import re
import sys

def get_viewstate(session, url):
    """Retrieve javax.faces.ViewState dynamically from the page source."""
    #headers = {
    #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #    "Accept-Language": "en-US,en;q=0.9",
    #    "Connection": "keep-alive"
    #}

    response = session.get(url)

    # Debugging: Print response snippet if needed
    # print(response.text[:2000])  

    #match = re.search(r'name="javax\.faces\.ViewState".*?value="(-?\d+:\d+)"', response.text)
    match = re.search(r'name="javax\.faces\.ViewState".*?value="(-?\d+:\d+)"', response.text)
    if match:
        return match.group(1)

    print("[ERROR] Failed to retrieve ViewState.")
    return None

def send_password_reset(domain, email):
    """Send password reset request to the specified domain."""
    base_url = f"https://{domain}.no/controlpanel/password/"
    session = requests.Session()

    viewstate = get_viewstate(session, base_url)
    if not viewstate:
        return

    form_data = {
        "retrieve-form": "retrieve-form",
        "retrieve-form:query": email,
        "javax.faces.ViewState": viewstate,
        "javax.faces.source": "retrieve-form:j_idt35",
        "javax.faces.partial.event": "click",
        "javax.faces.partial.execute": "retrieve-form:j_idt35 retrieve-form",
        "javax.faces.partial.render": "retrieve-form:query retrieve-form:queryMessage retrieve-form:backMessage",
        "javax.faces.partial.ajax": "true"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    response = session.post(base_url, data=form_data, headers=headers)

    print(f"[INFO] Sent request to {base_url}")
    print(f"[INFO] Status Code: {response.status_code}")
#    print(f"[INFO] Response: {response.text[:500]}")  # Print first 500 chars of response for debugging

#if __name__ == "__main__":
#    if len(sys.argv) != 3:
#        print("Usage: python resetpw.py <domain> <email>")
#        print("Example: python resetpw.py uniweb mats@ratlab.xyz")
#        sys.exit(1)
#
#    domain = sys.argv[1]
#    email = sys.argv[2]
#
#    send_password_reset(domain, email)
