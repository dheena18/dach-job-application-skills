"""
Page-count and PDF-export check for a .docx. Cross-platform.

python-docx has no layout engine, so it cannot tell you how many pages a
document renders to. This script renders the document with a real engine:

  1. Microsoft Word via COM (Windows, if Word and `pywin32` are installed) -
     the most exact rendering of glyphs (umlauts, ß, German quotes) and pages.
  2. LibreOffice headless (`soffice`, any OS) otherwise. The page count is
     read from the exported PDF with `pypdf`.

Force an engine with --engine word|libreoffice (default: auto).

Usage:
    python check_pages.py pages <file.docx> [--engine E]
    python check_pages.py pdf   <file.docx> <out.pdf> [--engine E]
    python check_pages.py both  <file.docx> <out.pdf> [--engine E]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

WD_STATISTIC_PAGES = 2
WD_FORMAT_PDF = 17


def _word_available():
    if sys.platform != "win32":
        return False
    try:
        import win32com.client  # noqa: F401
        return True
    except ImportError:
        return False


def _soffice():
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for p in (r"C:\Program Files\LibreOffice\program\soffice.exe",
              r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
              "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if os.path.exists(p):
            return p
    return None


def pick_engine(requested="auto"):
    if requested == "word":
        if not _word_available():
            sys.exit("Word engine requested but Word/pywin32 is not available.")
        return "word"
    if requested == "libreoffice":
        if not _soffice():
            sys.exit("LibreOffice engine requested but `soffice` was not found.")
        return "libreoffice"
    if _word_available():
        return "word"
    if _soffice():
        return "libreoffice"
    sys.exit("No rendering engine found. Install LibreOffice (https://www.libreoffice.org) "
             "or, on Windows, Microsoft Word plus `pip install pywin32`.")


# ---- Word -----------------------------------------------------------------

def _word_open():
    import win32com.client as win32
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    return word


def _word_pages(path):
    word = _word_open()
    try:
        doc = word.Documents.Open(os.path.abspath(path), ReadOnly=True)
        try:
            doc.Repaginate()
            return doc.ComputeStatistics(WD_STATISTIC_PAGES)
        finally:
            doc.Close(False)
    finally:
        word.Quit()


def _word_pdf(path, pdf_path):
    word = _word_open()
    try:
        doc = word.Documents.Open(os.path.abspath(path), ReadOnly=True)
        try:
            doc.SaveAs(os.path.abspath(pdf_path), FileFormat=WD_FORMAT_PDF)
        finally:
            doc.Close(False)
    finally:
        word.Quit()


# ---- LibreOffice ----------------------------------------------------------

def _lo_pdf(path, pdf_path):
    out_dir = os.path.dirname(os.path.abspath(pdf_path)) or "."
    with tempfile.TemporaryDirectory() as profile:
        # A throwaway profile avoids lock/first-start problems.
        cmd = [_soffice(), f"-env:UserInstallation=file:///{profile.replace(os.sep, '/')}",
               "--headless", "--convert-to", "pdf", "--outdir", out_dir,
               os.path.abspath(path)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    produced = os.path.join(out_dir, os.path.splitext(os.path.basename(path))[0] + ".pdf")
    if os.path.abspath(produced) != os.path.abspath(pdf_path):
        os.replace(produced, pdf_path)


def _pdf_pages(pdf_path):
    from pypdf import PdfReader
    return len(PdfReader(pdf_path).pages)


# ---- public API -----------------------------------------------------------

def get_page_count(path, engine="auto"):
    engine = pick_engine(engine)
    if engine == "word":
        return _word_pages(path)
    with tempfile.TemporaryDirectory() as tmp:
        pdf = os.path.join(tmp, "check.pdf")
        _lo_pdf(path, pdf)
        return _pdf_pages(pdf)


def export_pdf(path, pdf_path, engine="auto"):
    engine = pick_engine(engine)
    pdf_path = os.path.abspath(pdf_path)
    (_word_pdf if engine == "word" else _lo_pdf)(path, pdf_path)
    return pdf_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["pages", "pdf", "both"])
    ap.add_argument("docx")
    ap.add_argument("pdf", nargs="?")
    ap.add_argument("--engine", choices=["auto", "word", "libreoffice"], default="auto")
    a = ap.parse_args()
    if a.cmd in ("pdf", "both") and not a.pdf:
        ap.error(f"`{a.cmd}` needs an output .pdf path")
    if a.cmd == "pages":
        print(get_page_count(a.docx, a.engine))
    elif a.cmd == "pdf":
        print(export_pdf(a.docx, a.pdf, a.engine))
    else:
        pdf = export_pdf(a.docx, a.pdf, a.engine)
        print(f"pages={_pdf_pages(pdf)}")
        print(f"pdf={pdf}")


if __name__ == "__main__":
    main()
