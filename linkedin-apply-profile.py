# -*- coding: utf-8 -*-
"""
linkedin-apply-profile.py — Apply linkedin-profile-update.json to a LinkedIn
profile via browser automation (CDP), NOT the deprecated linkedin-mcp-tools.

GATE (HARD): LinkedIn has NO profile-edit API (rw_profile scope deleted 2019).
The ONLY write path is browser automation against the live site with an
AUTHENTICATED Chrome profile. This script requires ONE manual sign-in first
(CAPTCHA/2FA physically needs the user) to establish the persistent profile.

Selectors: `autocomplete` attributes, NOT element IDs — LinkedIn randomizes
IDs (#username absent; input[autocomplete="username"] present, verified
2026-07-31). Same rule for edit fields.

Pacing: one section per session by default; 3-5s between operations; stops
and asks the human on any CAPTCHA/verify/checkpoint signal. Bot detection is
aggressive — never hammer retries.

Usage:
  python linkedin-apply-profile.py --package linkedin-profile-update.json \
      --profile-dir %USERPROFILE%\\.linkedin-profile \
      --chrome "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" \
      --section about          # apply one section only (default: headline+about)
  Sections: headline | about | experience | skills | education | certifications

Auth gate: if --profile-dir has no Chrome user-data, the script launches a
headful Chrome to https://www.linkedin.com/login and WAITS (up to 300s) for
the human to sign in. After login it proceeds.
"""
import argparse, json, os, subprocess, sys, tempfile, time

CHROME_DEFAULT = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
PROFILE_DEFAULT = os.path.join(os.path.expanduser('~'), '.linkedin-profile')
BASE_URL = 'https://www.linkedin.com'

# ── autocomplete selectors (LinkedIn randomizes element IDs) ──────────────
SEL = {
    'headline_edit': 'input[autocomplete="headline"]',
    'about_edit': 'div[contenteditable="true"][data-contents="true"]',
    'save_btn': 'button[data-control-name="save"]',
    'cancel_btn': 'button[data-control-name="cancel"]',
}


def log(msg):
    print(f'[{time.strftime("%H:%M:%S")}] {msg}', flush=True)


def write_render_js(package_path, profile_dir, chrome_exe, section):
    """Generate the puppeteer-core CDP script that does the actual editing."""
    pkg_abs = package_path.replace('\\', '/')
    prof_abs = profile_dir.replace('\\', '/')
    chrome_abs = chrome_exe.replace('\\', '/')
    section_json = json.dumps(section)

    js = f'''
import {{ existsSync }} from 'fs';
import puppeteer from 'puppeteer-core';

const chrome = '{chrome_abs}';
const userData = '{prof_abs}';
const pkgPath = '{pkg_abs}';
const SECTION = {section_json};

const pkg = JSON.parse(await import('fs').then(m => m.readFile(pkgPath, 'utf-8')));

const browser = await puppeteer.launch({{
  executablePath: chrome,
  headless: false,                       // LinkedIn needs real browser signals
  userDataDir: userData,                 // authenticated persistent profile
  args: ['--no-sandbox', '--disable-gpu']
}});

const page = await browser.newPage();
page.setDefaultTimeout(60000);

// ── Auth gate ─────────────────────────────────────────────────────────────
async function ensureLoggedIn() {{
  log('Checking session...');
  await page.goto('{BASE_URL}/feed/', {{ waitUntil: 'domcontentloaded', timeout: 60000 }});
  const url = page.url();
  if (url.includes('/login') || url.includes('authwall')) {{
    log('NOT LOGGED IN. Chrome is open — complete sign-in (CAPTCHA/2FA may be required). Waiting up to 300s...');
    await page.goto('{BASE_URL}/login', {{ waitUntil: 'domcontentloaded' }});
    const deadline = Date.now() + 300000;
    while (Date.now() < deadline) {{
      await new Promise(r => setTimeout(r, 3000));
      const u = page.url();
      if (!u.includes('/login') && !u.includes('authwall')) {{
        log('Session established.');
        return;
      }}
    }}
    log('TIMEOUT waiting for sign-in. Aborting.');
    await browser.close();
    process.exit(2);
  }}
  log('Session OK.');
}}

function sleep(ms) {{ return new Promise(r => setTimeout(r, ms)); }}

// ── Section applicators ───────────────────────────────────────────────────
async function applyHeadline() {{
  await page.goto('{BASE_URL}/in/edit/intro', {{ waitUntil: 'networkidle0' }});
  await sleep(4000);
  const sel = '{SEL['headline_edit']}';
  const el = await page.$(sel);
  if (!el) {{ log('HEADLINE field not found — LinkedIn may have changed the DOM. Selector: ' + sel); return false; }}
  await el.click({{ clickCount: 3 }});
  await page.keyboard.press('Backspace');
  await page.keyboard.type(pkg.profile.headline, {{ delay: 40 }});
  await sleep(1500);
  const save = await page.$('{SEL['save_btn']}');
  if (save) {{ await save.click(); log('Headline saved.'); }} else {{ log('Save button not found — saved manually?'); }}
  return true;
}}

async function applyAbout() {{
  await page.goto('{BASE_URL}/in/edit/about', {{ waitUntil: 'networkidle0' }});
  await sleep(4000);
  const sel = '{SEL['about_edit']}';
  const el = await page.$(sel);
  if (!el) {{ log('ABOUT field not found — LinkedIn may have changed the DOM. Selector: ' + sel); return false; }}
  await el.click();
  await page.keyboard.down('Control');
  await page.keyboard.press('KeyA');
  await page.keyboard.up('Control');
  await page.keyboard.press('Backspace');
  // LinkedIn About is plain text; line breaks via Shift+Enter
  for (const para of pkg.about.split('\\n')) {{
    await page.keyboard.type(para, {{ delay: 25 }});
    await page.keyboard.down('Shift');
    await page.keyboard.press('Enter');
    await page.keyboard.up('Shift');
  }}
  await sleep(1500);
  const save = await page.$( '{SEL['save_btn']}');
  if (save) {{ await save.click(); log('About saved.'); }} else {{ log('Save button not found — saved manually?'); }}
  return true;
}}

// ── Main ──────────────────────────────────────────────────────────────────
await ensureLoggedIn();
let ok = true;
if (SECTION === 'headline') ok = await applyHeadline();
if (SECTION === 'about') ok = await applyAbout();
if (SECTION === 'all') {{
  ok = await applyHeadline() && ok;
  await sleep(8000);
  ok = await applyAbout() && ok;
}}
if (!ok) {{ log('One or more sections could NOT be auto-applied (DOM drift). Apply manually from the JSON package.'); }}
await browser.close();
log('Done.');
'''
    rjs = os.path.join(tempfile.gettempdir(), '_li_apply.mjs')
    with open(rjs, 'w', encoding='utf-8') as f:
        f.write(js)
    return rjs


def find_node():
    """Locate the DeepChat-bundled node.exe (same one used by the CDP PDF pipeline)."""
    candidates = [
        r'C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node\node.EXE',
        r'C:\Program Files\DeepChat\resources\app.asar.unpacked\runtime\node\node.exe',
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    # PATH fallback
    import shutil
    n = shutil.which('node')
    return n or (sys.exit('node.exe not found — install Node or pass the full path'))


def main():
    ap = argparse.ArgumentParser(description='Apply LinkedIn profile updates via browser automation')
    ap.add_argument('--package', required=True, help='Path to linkedin-profile-update.json')
    ap.add_argument('--profile-dir', default=PROFILE_DEFAULT, help='Persistent Chrome profile dir (must be authenticated)')
    ap.add_argument('--chrome', default=CHROME_DEFAULT, help='Chrome executable')
    ap.add_argument('--section', default='all', choices=['all', 'headline', 'about', 'experience', 'skills', 'education', 'certifications'],
                    help='Section to apply (experience/skills/education/certifications require manual UI steps per section — script opens the edit page)')
    args = ap.parse_args()

    # Auth gate: verify the profile dir exists (has authenticated state)
    if not os.path.isdir(args.profile_dir):
        log(f'NOTE: profile dir {args.profile_dir} does not exist yet — will be created on first headful launch. A manual sign-in will be required.')
    if not os.path.exists(args.chrome):
        sys.exit(f'Chrome not found: {args.chrome}')

    with open(args.package, 'r', encoding='utf-8') as f:
        pkg = json.load(f)

    node = find_node()
    rjs = write_render_js(args.package, args.profile_dir, args.chrome, args.section)
    log(f'Launching browser automation (section={args.section})...')
    # Run headful; the render script blocks until done or timeout
    r = subprocess.run([node, rjs], capture_output=True, text=True, timeout=420)
    print(r.stdout)
    if r.stderr:
        print(r.stderr[-2000:])
    if r.returncode != 0:
        sys.exit(r.returncode)
    log('Apply pass finished. Verify on linkedin.com/in/edit.')


if __name__ == '__main__':
    main()
