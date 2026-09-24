import urllib.request
import json
import os
import time

def download_raw(repo, path, branch="main", retries=3):
    """Download file from raw.githubusercontent.com."""
    url = f'https://raw.githubusercontent.com/{repo}/{branch}/{path}'
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Codex/1.0'})
            resp = urllib.request.urlopen(req, timeout=30)
            return resp.read().decode('utf-8')
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return f'# ERROR: {e}'

def get_rule_docs_from_tree(repo, branch="main"):
    """Get rule_docs file list from GitHub API."""
    url = f'https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Codex/1.0'})
    resp = urllib.request.urlopen(req, timeout=30)
    d = json.loads(resp.read())
    return sorted([
        p['path'] for p in d.get('tree', [])
        if p['path'].startswith('internal/config/rules/rule_docs/') and p['path'].endswith('.md')
    ])

repo = "alibaba/open-code-review"
branch = "main"

print("Fetching tree...")
rule_docs = get_rule_docs_from_tree(repo, branch)
print(f"Found {len(rule_docs)} files")

# Download raw files directly (no API rate limits)
for path in rule_docs:
    filename = os.path.basename(path)
    target = f'downloaded_rules/{filename}'
    
    # Skip if file already has real content (>= 200 bytes)
    if os.path.exists(target):
        size = os.path.getsize(target)
        if size >= 200:
            print(f"  SKIP {filename} (already {size} bytes)")
            continue
    
    print(f"  DOWNLOAD {filename}...")
    content = download_raw(repo, path, branch)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"    -> {len(content)} bytes")

print("\nDone!")
for f in sorted(os.listdir('downloaded_rules')):
    sz = os.path.getsize(f'downloaded_rules/{f}')
    print(f"  {f}: {sz} bytes")
