import urllib.request
import os
import time

repo = "alibaba/open-code-review"
branch = "main"

# Files that need re-download (those < 200 bytes)
small_files = [
    "internal/config/rules/rule_docs/build_gradle.md",
    "internal/config/rules/rule_docs/json.md",
    "internal/config/rules/rule_docs/package_json.md",
    "internal/config/rules/rule_docs/php.md",
    "internal/config/rules/rule_docs/po.md",
    "internal/config/rules/rule_docs/pom_xml.md",
    "internal/config/rules/rule_docs/pot.md",
    "internal/config/rules/rule_docs/prisma.md",
    "internal/config/rules/rule_docs/properties.md",
    "internal/config/rules/rule_docs/protobuf.md",
    "internal/config/rules/rule_docs/pug.md",
    "internal/config/rules/rule_docs/python.md",
    "internal/config/rules/rule_docs/r.md",
    "internal/config/rules/rule_docs/rego.md",
    "internal/config/rules/rule_docs/rust.md",
    "internal/config/rules/rule_docs/solidity.md",
    "internal/config/rules/rule_docs/swift.md",
    "internal/config/rules/rule_docs/terraform.md",
    "internal/config/rules/rule_docs/thrift.md",
    "internal/config/rules/rule_docs/ts_js_tsx_jsx.md",
    "internal/config/rules/rule_docs/verilog.md",
    "internal/config/rules/rule_docs/vhdl.md",
    "internal/config/rules/rule_docs/vyper.md",
    "internal/config/rules/rule_docs/yaml.md",
    "internal/config/rules/rule_docs/zig.md",
]

for path in small_files:
    filename = os.path.basename(path)
    target = f'downloaded_rules/{filename}'
    url = f'https://raw.githubusercontent.com/{repo}/{branch}/{path}'
    
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Codex/1.0'})
        resp = urllib.request.urlopen(req, timeout=30)
        content = resp.read().decode('utf-8')
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK: {len(content)} bytes")
    except Exception as e:
        print(f"  ERROR: {e}')
    time.sleep(0.3)

print("\nFinal check:")
for f in sorted(os.listdir('downloaded_rules')):
    sz = os.path.getsize(f'downloaded_rules/{f}')
    print(f"  {f}: {sz} bytes")
