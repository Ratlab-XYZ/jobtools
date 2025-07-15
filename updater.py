import shutil
import sys
import os
import tempfile
import requests
import click

REPO = "Ratlab-xyz/jobtools"  # Change this to your actual repo
CURRENT_VERSION = "v0.0.0"   # This should be injected during CI build

def get_latest_release_info():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    tag = data['tag_name']
    asset_url = next(asset['browser_download_url'] for asset in data['assets'] if 'uw' in asset['name'])
    return tag, asset_url

def check_for_update_notification():
    try:
        latest_tag, _ = get_latest_release_info()
        if latest_tag != CURRENT_VERSION:
            click.echo(f"⚠️  Update available: {latest_tag} (you have {CURRENT_VERSION}). Run 'uw update' to upgrade.")
    except Exception:
        pass  # Ignore update check errors silently

def update_binary(download_url):
    click.echo("Downloading update...")
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)

    with requests.get(download_url, stream=True) as r:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    # Use shutil.which() instead of sys.argv[0]
    current_path = shutil.which(sys.argv[0])
    if not current_path:
        click.echo("Error: Could not determine current binary path.")
        sys.exit(1)

    backup_path = current_path + ".bak"

    click.echo(f"Replacing binary at {current_path}...")
    shutil.move(current_path, backup_path)
    shutil.move(temp_path, current_path)
    os.chmod(current_path, 0o755)

    sys.exit(0)

def perform_update():
    try:
        latest_tag, download_url = get_latest_release_info()
        if latest_tag != CURRENT_VERSION:
            click.echo(f"Updating from {CURRENT_VERSION} to {latest_tag}...")
            update_binary(download_url)
        else:
            click.echo("Already up to date.")
    except Exception as e:
        click.echo(f"Update failed: {e}")
