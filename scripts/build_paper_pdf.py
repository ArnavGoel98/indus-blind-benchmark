"""Build reports/drafts/paper_DRAFT.pdf from paper_DRAFT.md (reviewer notes in [Reviewer ...] /
[Stop ...] brackets are left out). Uses python-markdown and headless Chromium.
Usage: python scripts/build_paper_pdf.py
"""
import re
import subprocess
from pathlib import Path

import markdown

SRC = Path("reports/drafts/paper_DRAFT.md")
HTML = SRC.with_suffix(".html")
PDF = SRC.with_suffix(".pdf")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
CSS = """
@page { size: A4; margin: 20mm 18mm; }
body { font-family: 'DejaVu Serif', Georgia, serif; font-size: 10.5pt; line-height: 1.42; color: #111; }
h1 { font-size: 17pt; margin: 0 0 6pt; } h2 { font-size: 13pt; margin: 16pt 0 6pt; border-bottom: 1px solid #bbb; }
h3 { font-size: 11pt; margin: 12pt 0 4pt; } p { margin: 4pt 0 7pt; text-align: justify; }
table { border-collapse: collapse; margin: 6pt 0 10pt; font-size: 8.6pt; width: 100%; page-break-inside: avoid; }
th, td { border: 1px solid #999; padding: 2.5pt 4pt; vertical-align: top; } th { background: #eee; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.8pt; } li { margin: 2pt 0; }
"""


def main():
    text = SRC.read_text(encoding="utf-8")
    text = re.sub(r"(?ms)^\[(Reviewer|Stop)[^\]]*\]\s*$\n?", "", text)
    body = markdown.markdown(text, extensions=["tables", "sane_lists"])
    HTML.write_text(f"<!doctype html><html><head><meta charset='utf-8'><title>IBDB draft</title>"
                    f"<style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={PDF.resolve()}", HTML.resolve().as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(PDF)


if __name__ == "__main__":
    main()
