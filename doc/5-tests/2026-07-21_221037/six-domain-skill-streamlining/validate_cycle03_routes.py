from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

CYCLE_SOURCES = {
    'implementation-planning-rules',
    'project-interface-release-execution-rules',
    'test-doc-rules',
    'test-naming-rules',
    'test-scattered-asset-location-rules',
    'test-task-root-layout-rules',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='验证周期03 owner route、正负触发别名和退役 source 状态')
    parser.add_argument('--repo-root', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--phase', choices=['pre-delete', 'post-delete'], required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo_root).resolve()
    manifest = yaml.safe_load(Path(args.manifest).read_text(encoding='utf-8'))
    errors: list[str] = []
    cases_path = root / 'doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/fixtures/trigger-cases.yaml'
    cases = yaml.safe_load(cases_path.read_text(encoding='utf-8'))['cases']
    candidates = {item['source_skill']: item for item in manifest['candidates'] if item['source_skill'] in CYCLE_SOURCES}

    for source, candidate in candidates.items():
        target = candidate['target_owner']
        target_path = root / target / 'SKILL.md'
        if not target_path.is_file():
            errors.append(f'target owner 缺失: {target}')
            continue
        target_text = '\n'.join(path.read_text(encoding='utf-8') for path in sorted((root / target).rglob('*')) if path.is_file())
        route = candidate['target_route']
        if route not in target_text:
            errors.append(f'owner route marker 缺失: {target} -> {route}')
        for alias in candidate.get('trigger_contract', {}).get('trigger_aliases', []):
            if alias not in target_text:
                errors.append(f'触发别名未承接: {source} -> {target}: {alias}')

        source_path = root / source
        if args.phase == 'pre-delete' and candidate['action'] == 'merge_retire' and not (source_path / 'SKILL.md').is_file():
            errors.append(f'pre-delete source 缺失: {source}')
        if args.phase == 'post-delete' and candidate['action'] == 'merge_retire' and source_path.exists():
            errors.append(f'post-delete source 仍存在: {source}')

    by_source = {case['source_skill']: case for case in cases if case['source_skill'] in CYCLE_SOURCES}
    for source, case in by_source.items():
        target_text = '\n'.join(path.read_text(encoding='utf-8') for path in sorted((root / case['target_owner']).rglob('*')) if path.is_file())
        if case['id'].endswith('-POS'):
            for token in case.get('required_target_tokens', []):
                if token not in target_text:
                    errors.append(f'正例 target token 缺失: {case["id"]}: {token}')
            if not case.get('required_source_tokens'):
                errors.append(f'正例 source token 为空: {case["id"]}')
        if case['id'].endswith('-NEG'):
            if case.get('required_source_tokens') or case.get('required_target_tokens'):
                errors.append(f'负例不应携带 required token: {case["id"]}')

    report = {
        'schema_version': 1,
        'phase': args.phase,
        'candidate_count': len(candidates),
        'positive_negative_cases_checked': len(by_source),
        'valid': not errors,
        'errors': errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
