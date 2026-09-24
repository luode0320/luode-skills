import urllib.request
import json
import os
import sys

def fetch_github_tree(repo, branch="main"):
    """Fetch recursive git tree from GitHub API."""
    url = f'https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Codex/1.0'})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

def download_file(repo, path, branch="main"):
    """Download a file from GitHub raw content."""
    url = f'https://api.github.com/repos/{repo}/contents/{path}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Codex/1.0',
        'Accept': 'application/vnd.github.raw'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.read().decode('utf-8')
    except Exception as e:
        return f'# ERROR downloading {path}: {e}'

def main():
    repo = "alibaba/open-code-review"
    branch = "main"
    
    print("Fetching repo tree...")
    tree_data = fetch_github_tree(repo, branch)
    
    # Collect all rule_docs files
    rule_docs = sorted([
        p['path'] for p in tree_data.get('tree', [])
        if p['path'].startswith('internal/config/rules/rule_docs/') and p['path'].endswith('.md')
    ])
    
    print(f"Found {len(rule_docs)} rule_docs files")
    
    # Create output directory
    os.makedirs('downloaded_rules', exist_ok=True)
    
    # Download system_rules.json
    print("\nDownloading system_rules.json...")
    content = download_file(repo, 'internal/config/rules/system_rules.json', branch)
    with open('downloaded_rules/system_rules.json', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  system_rules.json: {len(content)} bytes")
    
    # Download each rule file
    for path in rule_docs:
        filename = os.path.basename(path)
        print(f"Downloading {filename}...")
        content = download_file(repo, path, branch)
        with open(f'downloaded_rules/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {filename}: {len(content)} bytes")
    
    print(f"\nDone! Downloaded {len(rule_docs)} rule files + system_rules.json")
    print(f"Files in downloaded_rules/: {os.listdir('downloaded_rules')}")

if __name__ == '__main__':
    main()
