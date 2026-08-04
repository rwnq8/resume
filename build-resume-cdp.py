# -*- coding: utf-8 -*-
"""
build-resume-cdp.py — Build resume PDF via CDP pipeline (pandoc + MathJax SVG + puppeteer-core).
Replaces the old xelatex-based build-resume-pdf.py.
No character stripping needed — browsers render Unicode natively.

Usage: python build-resume-cdp.py
Output: rowan-quni-portfolio-v3.10.pdf
"""
import os, sys, subprocess, shutil

SRC = os.path.dirname(os.path.abspath(__file__))
TMP = os.environ['TEMP']
PANDOC = r'C:\Users\LENOVO\AppData\Local\Pandoc\pandoc.exe'
MATHJAX_CACHE = os.path.join(TMP, 'mathjax', 'tex-svg-full.js')
VERSION = 'v3.10'
DATE = '2026-08-04'
OUTPUT_PDF = os.path.join(SRC, f'rowan-quni-portfolio-{VERSION}.pdf')

def step(s):
    print(f'[{s}]...', flush=True)

# Step 1: Combine source files
step('1/6 Combining source files')
sections = []
for fn in ['README.md', 'RESUME.md', 'PORTFOLIO.md', 'SKILLS-TECHNOLOGY.md']:
    fp = os.path.join(SRC, fn)
    with open(fp, 'r', encoding='utf-8') as f:
        sections.append(f.read())

# Add YAML frontmatter for pandoc
combined = f"""---
title: "Rowan Brad Quni-Gudzinas — Research & Technology Leader Portfolio"
author: "Rowan Brad Quni-Gudzinas"
date: "{DATE}"
version: "{VERSION}"
---

{sections[0]}

\\newpage

{sections[1]}

\\newpage

{sections[2]}

\\newpage

{sections[3]}
"""

combined_md = os.path.join(TMP, '_resume_combined.md')
with open(combined_md, 'w', encoding='utf-8') as f:
    f.write(combined)
print(f'  Combined: {len(combined):,} chars -> {combined_md}')

# Step 2: pandoc --mathjax -> HTML
step('2/6 pandoc --mathjax -> HTML')
combined_html = os.path.join(TMP, '_resume_combined.html')
result = subprocess.run(
    [PANDOC, '--mathjax', '--standalone', combined_md, '-o', combined_html],
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f'PANDOC ERROR: {result.stderr}')
    sys.exit(1)
print(f'  HTML: {os.path.getsize(combined_html):,} bytes')

# Step 3: Switch CHTML -> SVG
step('3/6 Switching MathJax CHTML -> SVG')
with open(combined_html, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('tex-chtml-full.js', 'tex-svg-full.js')

with open(combined_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'  Switched (HTML now {len(html):,} chars)')

# Step 4: Inline MathJax locally (CDN unreachable from headless Chrome)
step('4/6 Inlining MathJax SVG from local cache')
with open(MATHJAX_CACHE, 'r', encoding='utf-8') as f:
    mathjax_js = f.read()
print(f'  MathJax JS: {len(mathjax_js):,} chars')

# Find the MathJax script tag and replace with inlined version
import re
matches = list(re.finditer(r'<script[^>]*tex-svg[^>]*>[^<]*</script>', html))
if not matches:
    print('  WARNING: No MathJax script tag found (no math in document?)')
    # Try broader match
    matches = list(re.finditer(r'<script[^>]*mathjax[^>]*>.*?</script>', html, re.DOTALL))
if matches:
    full_match = matches[0].group(0)
    inline_tag = f'<script>{mathjax_js}</script>'
    html = html.replace(full_match, inline_tag)  # str.replace NOT re.sub
    print(f'  Inlined MathJax')
else:
    print('  WARNING: Could not find MathJax script tag to inline')

with open(combined_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'  Final HTML: {len(html):,} chars')

# Step 5: puppeteer-core CDP -> PDF
step('5/6 puppeteer-core CDP render')
render_js = os.path.join(TMP, '_render_resume.mjs')
with open(render_js, 'w', encoding='utf-8') as f:
    f.write(f'''import {{ existsSync, statSync }} from 'fs';
import {{ resolve }} from 'path';
import os from 'os';
import puppeteer from 'puppeteer-core';

const chromeExe = '{r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'.replace(chr(92),'/')}';
const htmlFile = '{combined_html.replace(chr(92), '/')}';
const pdfFile = '{OUTPUT_PDF.replace(chr(92), '/')}';

console.log('HTML:', htmlFile);
console.log('PDF:', pdfFile);

if (!existsSync(htmlFile)) throw new Error('HTML not found');

const browser = await puppeteer.launch({{
    executablePath: chromeExe,
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
}});

try {{
    const page = await browser.newPage();
    const fileUrl = 'file:///' + htmlFile;
    
    console.log('Loading page...');
    await page.goto(fileUrl, {{ waitUntil: 'load', timeout: 120000 }});
    
    // Wait for MathJax if present
    try {{
        const hasMj = await page.evaluate(() => typeof window.MathJax !== 'undefined');
        if (hasMj) {{
            console.log('Waiting for MathJax...');
            await page.evaluate(() => {{
                if (window.MathJax.startup && window.MathJax.startup.promise)
                    return window.MathJax.startup.promise;
            }});
            console.log('MathJax done');
        }} else {{
            console.log('No MathJax on page');
        }}
    }} catch (e) {{
        console.log('MathJax wait:', e.message.substring(0, 100));
    }}
    
    // Extra settle time
    await new Promise(r => setTimeout(r, 2000));
    
    console.log('Rendering PDF...');
    await page.pdf({{
        path: pdfFile,
        format: 'A4',
        printBackground: true,
        margin: {{ top: '2cm', bottom: '2cm', left: '2cm', right: '2cm' }}
    }});
    
    const size = statSync(pdfFile).size;
    console.log(`PDF: ${{(size/1024).toFixed(1)}} KB, size=${{size}} bytes`);
    if (size < 102400) {{
        console.error('PDF < 100KB — substandard render!');
        process.exit(1);
    }}
    console.log('PDF BUILD OK');
}} finally {{
    await browser.close();
}}
''')

result = subprocess.run(['node', render_js], capture_output=True, text=True, cwd=TMP)
print(result.stdout)
if result.returncode != 0:
    print(f'RENDER ERROR: {result.stderr}')
    sys.exit(1)

# Step 6: Verify PDF quality
step('6/6 Verifying PDF quality')
try:
    import fitz  # PyMuPDF
    doc = fitz.open(OUTPUT_PDF)
    pages = len(doc)
    full_text = ''
    for page in doc:
        full_text += page.get_text()
    doc.close()
    
    fffd_count = full_text.count('\ufffd')
    ffff_count = full_text.count('\uffff')
    
    print(f'  Pages: {pages}')
    print(f'  Text chars: {len(full_text):,}')
    print(f'  U+FFFD: {fffd_count}')
    print(f'  U+FFFF: {ffff_count}')
    
    if fffd_count > 0 or ffff_count > 0:
        print('  FAIL: Glyph rendering errors detected!')
        sys.exit(1)
    else:
        print('  PASS: Zero rendering errors')
except ImportError:
    print('  WARNING: PyMuPDF not installed, skipping verification')
    # Fallback: just check size
    size = os.path.getsize(OUTPUT_PDF)
    print(f'  PDF size: {size:,} bytes ({(size/1024):.1f} KB)')

print(f'\nDone: {OUTPUT_PDF}')
