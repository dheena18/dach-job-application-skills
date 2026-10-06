"""
Page-count and PDF-export check for a .docx, using the real Microsoft Word
rendering engine via COM automation (Windows only).

Identical to the copy used by `cv-translate-de` and `resume-tailor` — kept
as a self-contained duplicate so this skill works standalone.

Usage:
    python check_pages.py pages <file.docx>
    python check_pages.py pdf <file.docx> <out.pdf>
    python check_pages.py both <file.docx> <out.pdf>
"""
import os
import sys

import win32com.client as win32

WD_STATISTIC_PAGES = 2
WD_FORMAT_PDF = 17


def _open_word():
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    return word


def get_page_count(path):
    path = os.path.abspath(path)
    word = _open_word()
    try:
        doc = word.Documents.Open(path, ReadOnly=True)
        try:
            doc.Repaginate()
            return doc.ComputeStatistics(WD_STATISTIC_PAGES)
        finally:
            doc.Close(False)
    finally:
        word.Quit()


def export_pdf(path, pdf_path):
    path = os.path.abspath(path)
    pdf_path = os.path.abspath(pdf_path)
    word = _open_word()
    try:
        doc = word.Documents.Open(path, ReadOnly=True)
        try:
            doc.SaveAs(pdf_path, FileFormat=WD_FORMAT_PDF)
        finally:
            doc.Close(False)
    finally:
        word.Quit()
    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == "pages":
        print(get_page_count(sys.argv[2]))
    elif cmd == "pdf":
        print(export_pdf(sys.argv[2], sys.argv[3]))
    elif cmd == "both":
        pages = get_page_count(sys.argv[2])
        pdf = export_pdf(sys.argv[2], sys.argv[3])
        print(f"pages={pages}")
        print(f"pdf={pdf}")
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(2)
