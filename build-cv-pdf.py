# -*- coding: utf-8 -*-
"""
build-cv-pdf.py - Render RESUME.md to a print-ready PDF with headless Chrome/Chromium.

Cross-platform replacement for the CV part of build-resume-cdp.py (which is Windows-only and
builds the combined v3.x portfolio). Needs Python's `markdown` package and a Chrome or Chromium binary.

Usage:
  python build-cv-pdf.py                      # finds chrome/chromium on PATH or CHROME env var
  python build-cv-pdf.py --chrome /path/to/chrome --out rowan-quni-cv-v4.0.pdf
"""
import argparse, os, shutil, subprocess, sys, tempfile

import markdown

SRC = os.path.dirname(os.path.abspath(__file__))
VERSION = "v4.0"

CSS = """
@page { size: A4; margin: 16mm 16mm 16mm 16mm; }
body { font-family: "Public Sans", "Helvetica Neue", Arial, "Liberation Sans", sans-serif; color: #1b1f2a;
       font-size: 10pt; line-height: 1.42; }
h1 { font-family: "Fraunces", Georgia, "DejaVu Serif", serif; font-size: 22pt; color: #24315e; margin: 0 0 2pt; letter-spacing: 0.5pt; }
h2 { font-size: 11.5pt; color: #24315e; margin: 2pt 0 6pt; font-weight: 600; }
h2 + p { margin-top: 0; }
h3 { font-size: 10.5pt; margin: 10pt 0 1pt; color: #1b1f2a; }
hr { border: 0; border-top: 1px solid #c9cfdd; margin: 9pt 0; }
p { margin: 3pt 0 5pt; }
ul, ol { margin: 2pt 0 6pt 16pt; padding: 0; }
li { margin: 1.5pt 0; }
a { color: #24315e; text-decoration: none; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0 6pt; font-size: 9.5pt; }
th, td { text-align: left; padding: 2pt 6pt 2pt 0; border-bottom: 1px solid #e3e6ee; }
th { color: #5a6275; font-weight: 600; }
h3, li, tr { break-inside: avoid; }
"""


def find_chrome(explicit):
    for c in [explicit, os.environ.get("CHROME"), "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
              shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("chrome")]:
        if c and os.path.exists(c):
            return c
    sys.exit("No Chrome/Chromium found: pass --chrome or set CHROME")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome")
    ap.add_argument("--out", default=os.path.join(SRC, f"rowan-quni-cv-{VERSION}.pdf"))
    a = ap.parse_args()
    with open(os.path.join(SRC, "RESUME.md"), encoding="utf-8") as f:
        body = markdown.markdown(f.read(), extensions=["tables", "sane_lists"])
    html = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Rowan Brad Quni-Gudzinas CV {VERSION}</title>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "cv.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(html)
        subprocess.run([find_chrome(a.chrome), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={a.out}", "file://" + page], check=True, capture_output=True)
    print(a.out)


if __name__ == "__main__":
    main()
