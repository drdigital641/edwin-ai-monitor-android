"""R&C Spaceworks "AI concept of the day": add one dated concept, rebuild, commit and push.

Usage: python3 daily_publish.py <image file> <entry.json>
  entry.json = {"date": "YYYY-MM-DD", "title": "...", "space": "F&B", "summary": "40-60 words",
                "ideas": ["4 short bullets"], "alt": "... (AI design concept)"}
Prints the site commit SHA to pass to the Bridge sync_from_github call (see DAILY-RUN.md).
Needs: Pillow, git push access to drdigital641/edwin-ai-monitor-android (branch site-assets).
"""
import json
import os
import shutil
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
REPO = os.environ.get('RC_REPO', '/home/user/edwin-ai-monitor-android')
SHARED = '/mnt/project-files/rc-design-build'  # shared working copy, updated too when mounted
GIT = ['git', '-C', REPO, '-c', 'user.name=Claude', '-c', 'user.email=noreply@anthropic.com']
TRAILER = '\n\nCo-Authored-By: Claude <noreply@anthropic.com>'


def run(cmd):
    print('+', ' '.join(cmd))
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip()


def ensure_repo():
    if not os.path.isdir(os.path.join(REPO, '.git')):
        run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--no-checkout', '--branch', 'site-assets',
             'https://github.com/drdigital641/edwin-ai-monitor-android', REPO])
        run(['git', '-C', REPO, 'sparse-checkout', 'set', '--no-cone', '/site-assets/rc-design-build/', '/pageone-site/clients/rc-design-build/'])
        run(['git', '-C', REPO, 'checkout', 'site-assets'])
    run(['git', '-C', REPO, 'fetch', '--depth', '1', 'origin', 'site-assets'])
    run(['git', '-C', REPO, 'checkout', '-q', '-B', 'site-assets', 'FETCH_HEAD'])


def main(img_path, entry_path):
    e = json.load(open(entry_path))
    for k in ('date', 'title', 'space', 'summary', 'ideas', 'alt'):
        assert e.get(k), 'missing ' + k
    assert '(AI design concept)' in e['alt']
    ensure_repo()
    daily_path = os.path.join(PROJ, 'content', 'daily.json')
    daily = json.load(open(daily_path))
    if any(d['date'] == e['date'] for d in daily):
        print('already published for', e['date'])
        return
    # 1) image -> webp, commit to site-assets
    im = Image.open(img_path).convert('RGB')
    im.thumbnail((1024, 1024), Image.LANCZOS)
    bases = [os.path.join(REPO, 'site-assets', 'rc-design-build', 'daily')]
    if os.path.isdir(SHARED):
        bases.append(os.path.join(SHARED, 'assets', 'daily'))
    for base in bases:
        os.makedirs(base, exist_ok=True)
        im.save(os.path.join(base, e['date'] + '.webp'), 'WEBP', quality=76, method=6)
        im.resize((640, 640), Image.LANCZOS).save(os.path.join(base, e['date'] + '-640.webp'), 'WEBP', quality=72, method=6)
    run(GIT + ['add', 'site-assets/rc-design-build/daily'])
    run(GIT + ['commit', '-q', '-m', 'R&C concept of the day image %s%s' % (e['date'], TRAILER)])
    run(['git', '-C', REPO, 'push', '-q', 'origin', 'HEAD:site-assets'])
    img_sha = run(['git', '-C', REPO, 'rev-parse', '--short', 'HEAD'])
    # 2) data entry
    e['image'] = 'daily/' + e['date']
    e['asset_sha'] = img_sha
    daily.append(e)
    json.dump(daily, open(daily_path, 'w'), indent=2, ensure_ascii=False)
    if os.path.isdir(SHARED) and os.path.realpath(SHARED) != os.path.realpath(PROJ):
        shutil.copy(daily_path, os.path.join(SHARED, 'content', 'daily.json'))
    # 3) rebuild and commit site
    subprocess.run([sys.executable, os.path.join(PROJ, 'build.py')], check=True)
    dst = os.path.join(REPO, 'pageone-site', 'clients', 'rc-design-build')
    if os.path.realpath(dst) != os.path.realpath(PROJ):
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(PROJ, dst, ignore=shutil.ignore_patterns('__pycache__', 'assets', 'uploads-original', 'real', 'daily', 'screens', 'logo-512.png'))
    run(GIT + ['add', '-A', 'pageone-site/clients/rc-design-build'])
    run(GIT + ['commit', '-q', '-m', 'R&C concept of the day %s%s' % (e['date'], TRAILER)])
    run(['git', '-C', REPO, 'push', '-q', 'origin', 'HEAD:site-assets'])
    print('SITE_SHA', run(['git', '-C', REPO, 'rev-parse', 'HEAD']))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
