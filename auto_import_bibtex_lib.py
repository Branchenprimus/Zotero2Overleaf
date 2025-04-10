import re
import os
import subprocess
from urllib.parse import urlparse, urlunparse
import requests
from dotenv import load_dotenv
import psutil  # Import psutil to check running processes

# Load .env file
load_dotenv()

# Config
ZOTERO_API_URL = os.getenv("ZOTERO_API_URL")
OVERLEAF_REPO_PATH = os.getenv("OVERLEAF_REPO_PATH")
EXPORT_FILENAME = os.getenv("EXPORT_FILENAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def is_zotero_running():
    """Check if Zotero is running."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] and 'zotero' in process.info['name'].lower():
            return True
    return False

def inject_git_credentials(repo_path):
    """Injects credentials into the remote Git URL."""
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
    cwd=repo_path, capture_output=True, text=True, check=True)
    remote_url = result.stdout.strip()

    parsed_url = urlparse(remote_url)
    netloc = f"{USERNAME}:{PASSWORD}@{parsed_url.hostname}"
    if parsed_url.port:
        netloc += f":{parsed_url.port}"
    authenticated_url = urlunparse(parsed_url._replace(netloc=netloc))

    subprocess.run(['git', 'remote', 'set-url', 'origin', 
    authenticated_url], cwd=repo_path, check=True)
    print("🔐 Git remote URL updated with credentials.")

def export_zotero_bibtex(export_path):
    try:
        response = requests.get(ZOTERO_API_URL)
        response.raise_for_status()
        with open(export_path, 'wb') as f:
            f.write(response.content)
        print("✅ Zotero library exported successfully to", export_path)
    except requests.RequestException as e:
        print(f"❌ Error fetching Zotero library: {e}")
        exit(1)

def run_git_command(repo_path, command):
    try:
        result = subprocess.run(command, cwd=repo_path, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e.stderr if e.stderr else e.stdout}")
        exit(1)

def extract_new_citekeys(diff_text):
    """
    Parses the git diff and extracts citekeys from added BibTeX entries.
    """
    added_lines = [line for line in diff_text.splitlines() if line.startswith('+@')]
    citekeys = []
    for line in added_lines:
        match = re.match(r'\+@[\w]+\{([^,]+),', line)
        if match:
            citekeys.append(match.group(1))
    return citekeys

def update_overleaf_repo(repo_path, filename):
    inject_git_credentials(repo_path)

    print("🔄 Pulling latest changes from remote...")
    run_git_command(repo_path, ['git', 'pull'])

    # Capture diff before the commit
    diff_before_commit = run_git_command(repo_path, ['git', 'diff', filename])

    # Add the updated file
    run_git_command(repo_path, ['git', 'add', filename])

    # Check if there are changes to commit
    result = subprocess.run(['git', 'status', '--porcelain'], cwd=repo_path, capture_output=True, text=True)
    if result.stdout.strip() == '':
        print("✅ No changes to commit. Repository is already up-to-date.")
        return

    # Extract citekeys from diff
    new_citekeys = extract_new_citekeys(diff_before_commit)
    if new_citekeys:
        print("🆕 New citekeys added:")
        for key in new_citekeys:
            print(f"  - {key}")
    else:
        print("ℹ️ No new citekeys found in this update.")

    # Commit the changes
    run_git_command(repo_path, ['git', 'commit', '-m', 'Automated Zotero export update'])

    # Pull again to make sure we're up-to-date before pushing (avoiding race conditions)
    print("🔄 Pulling again before pushing to handle any new remote changes...")
    run_git_command(repo_path, ['git', 'pull', '--rebase'])

    # Push the changes to remote
    run_git_command(repo_path, ['git', 'push'])
    print("🚀 Overleaf repository successfully updated.")

if __name__ == "__main__":
    # Check if Zotero is running
    if not is_zotero_running():
        print("❌ Zotero is not running. Please start Zotero and try again.")
        exit(1)

    export_path = os.path.join(OVERLEAF_REPO_PATH, EXPORT_FILENAME)
    export_zotero_bibtex(export_path=export_path)
    update_overleaf_repo(OVERLEAF_REPO_PATH, EXPORT_FILENAME)
