#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-resume-pdf.py — Build a clean, publication-ready PDF for the QNFO resume portfolio.
Strips box-drawing characters, emojis, and xelatex-incompatible Unicode before build.
Uses the research skill's build-paper.py pipeline for verified rendering.

Usage:
    python build-resume-pdf.py [--output resume.pdf]
"""
import os, re, sys, subprocess, argparse

def preprocess(source_dir, output_md):
    """Combine all portfolio files, strip xelatex-incompatible characters."""
    sections = []
    for fn in ['README.md', 'RESUME.md', 'PORTFOLIO.md', 'SKILLS-TECHNOLOGY.md']:
        fp = os.path.join(source_dir, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Strip box-drawing characters (Unicode U+2500-U+257F)
        content = ''.join(c for c in content if not (0x2500 <= ord(c) <= 0x257F))
        
        # Strip emojis and variation selectors
        content = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\uFE00-\uFE0F\u200D]', '', content)
        
        # Strip shields.io badge images
        content = re.sub(r'!\[.*?\]\(https://img\.shields\.io/.*?\)\s*\n?', '', content)
        content = re.sub(r'\[!\[.*?\]\(https://img\.shields\.io/.*?\)\]\(https://.*?\)\s*\n?', '', content)
        
        # Convert combining circumflex
        content = content.replace('x\u0302', r'$\hat{x}$')
        
        # Convert degree/copyright to LaTeX
        content = content.replace('\u00b0', r'\textdegree{}')
        content = content.replace('\u00a9', r'\textcopyright{}')
        
        sections.append(content)
    
    combined = f"""---
title: "Rowan Brad Quni-Gudzinas — Research & Technology Leader Portfolio"
author: "Rowan Brad Quni-Gudzinas"
date: "July 31, 2026"
geometry: margin=1in
documentclass: article
classoption: 11pt
mainfont: DejaVu Sans
monofont: DejaVu Sans Mono
header-includes: |
  \\usepackage{{fancyhdr}}
  \\usepackage{{fontspec}}
  \\usepackage{{xunicode}}
  \\usepackage{{textcomp}}
  \\setmainfont{{DejaVu Sans}}
  \\setsansfont{{DejaVu Sans}}
  \\setmonofont{{DejaVu Sans Mono}}
  \\pagestyle{{fancy}}
  \\fancyhf{{}}
  \\fancyhead[L]{{Rowan Brad Quni-Gudzinas — Portfolio}}
  \\fancyhead[R]{{\\thepage}}
  \\fancyfoot[C]{{CC-BY-4.0 | github.com/QNFO/resume}}
---

\\tableofcontents
\\newpage

{sections[0]}

\\newpage
{sections[1]}

\\newpage
{sections[2]}

\\newpage
{sections[3]}
"""
    combined = re.sub(r'\n{3,}', '\n\n', combined)
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(combined)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', '-o', default='rowan-quni-portfolio.pdf')
    args = ap.parse_args()
    
    src = os.path.dirname(os.path.abspath(__file__))
    tmp = os.path.join(os.environ.get('TEMP', '/tmp'), '_resume_build.md')
    
    preprocess(src, tmp)
    print(f"[1/3] Preprocessed: {tmp}")
    
    # Use build-paper.py for verified rendering
    bp = os.path.join(os.environ['USERPROFILE'], '.deepchat', 'skills', 'research', 'scripts', 'build-paper.py')
    if not os.path.exists(bp):
        print("[FAIL] build-paper.py not found — install research skill first")
        sys.exit(1)
    
    result = subprocess.run(['python', bp, tmp, '-o', args.output], capture_output=False)
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
