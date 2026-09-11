#!/usr/bin/env python3
"""Yayın öncesi depo/bağlantı denetimi. Gereksinim: Python 3 ve PyYAML.

Örnek: python3 scripts/audit-publication.py --base 820641c^ --live
Build'i önce çalıştırın. Kaynak içerikleri değiştirmez.
"""
import argparse
import collections
import concurrent.futures
import hashlib
import json
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for key in ['src', 'href', 'poster']:
            if attrs.get(key):
                self.refs.append(attrs[key])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='820641c^')
    parser.add_argument('--head', default='HEAD')
    parser.add_argument('--output', default='docs/kitapcik-hazirlik')
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    dist = ROOT / 'dist'
    if not (dist / 'index.html').exists():
        raise SystemExit('Önce npm run build çalıştırın.')
    pages = {}
    for file in dist.rglob('*.html'):
        page = Page()
        page.feed(file.read_text())
        pages[file] = page
    broken, fragments, live_paths = [], [], set()
    for file, page in pages.items():
        if file.name != '404.html':
            live_paths.add('/' + str(file.relative_to(dist)).replace('index.html', ''))
        for ref in page.refs:
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path)
            target = dist / path.lstrip('/') if path.startswith('/') else file.parent / path if path else file
            if target.is_dir():
                target /= 'index.html'
            if not target.exists():
                broken.append([str(file.relative_to(dist)), ref])
            if parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                fragments.append([str(file.relative_to(dist)), ref])
            if path.startswith(('/media/', '/_astro/', '/logo-', '/matro-')):
                live_paths.add(path)
    data = {}
    for kind in ['teams', 'haberler', 'activities']:
        data[kind] = []
        for file in sorted((ROOT / 'src/content' / kind).glob('*.md')):
            record = yaml.safe_load(file.read_text().split('---', 2)[1])
            record['id'] = file.stem
            data[kind].append(record)
    read = lambda name: json.loads((ROOT / 'src/data' / (name + '.json')).read_text())
    assets, achievements = read('assets')['assets'], read('achievements')['items']
    files = [f for f in (ROOT / 'public/media').rglob('*') if f.is_file()]
    hashes, aliases = collections.defaultdict(list), collections.defaultdict(set)
    for file in files:
        hashes[hashlib.sha256(file.read_bytes()).hexdigest()].append(str(file.relative_to(ROOT / 'public')))
    for team in data['teams']:
        for name in [team['title'], *team.get('aliases', [])]:
            # Türkçe adların noktalı/noktasız I harfini koru.
            key = name.strip().replace('I', 'ı').replace('İ', 'i').lower()
            aliases[key].add(team['id'])
    report = {
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'base': git('rev-parse', args.base), 'head': git('rev-parse', args.head),
        'commits': git('log', f'{args.base}..{args.head}', '--format=%h %ad %s', '--date=iso').splitlines(),
        'changed_files': git('diff', '--name-only', args.base, args.head).splitlines(),
        'pages': len(pages), 'broken_local_references': broken, 'broken_fragments': fragments,
        'assets': len(assets), 'gallery_count': len(read('gallery')['images']),
        'media_files': len(files), 'media_bytes': sum(f.stat().st_size for f in files),
        'duplicates': [v for v in hashes.values() if len(v) > 1],
        'unlisted_media': [str(f.relative_to(ROOT / 'public')) for f in files if '/' + str(f.relative_to(ROOT / 'public')) not in {a['file'] for a in assets}],
        'achievement_counts': {
            'records': len(achievements),
            'firstPlaces': sum(bool(re.search(r'(^|[^0-9])1\.', a['degree'])) for a in achievements),
            'finalists2026': sum(a['year'] == 2026 and 'finalist' in a['degree'].lower() for a in achievements),
        },
        'alias_collisions': {k: sorted(v) for k, v in aliases.items() if len(v) > 1},
        'team_summary': [{k: t.get(k) for k in ['id', 'title', 'status', 'aliases', 'image', 'gallery', 'video']} for t in data['teams']],
        'news_by_type': dict(collections.Counter(t['type'] for t in data['haberler'])),
        'sponsor_packages': dict(collections.Counter(s['package'] for s in read('sponsors')['current'])),
        'duplicates_html_ids': [[str(f.relative_to(dist)), [i for i, c in collections.Counter(p.ids).items() if c > 1]] for f, p in pages.items() if len(p.ids) != len(set(p.ids))],
    }
    (out / 'denetim-verisi.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if args.live:
        def check(path):
            try:
                request = urllib.request.Request('https://btumatro.com' + path, method='HEAD')
                with urllib.request.urlopen(request, timeout=25) as response:
                    return [path, response.status]
            except Exception as error:
                return [path, str(error)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(check, sorted(live_paths)))
        live = {'generatedAt': report['generatedAt'], 'total_checks': len(results), 'failures': [r for r in results if r[1] != 200], 'results': results}
        (out / 'canli-kontrol.json').write_text(json.dumps(live, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'pages': len(pages), 'broken': len(broken), 'brokenFragments': len(fragments), 'output': str(out)}, ensure_ascii=False))
    if broken or fragments:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
