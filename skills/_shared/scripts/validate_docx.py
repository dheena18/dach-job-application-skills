"""
Portable structural check that a .docx is still a sound Word file after
scripted edits. No Claude-specific tooling or LibreOffice needed.

Checks: valid zip, required parts present, every XML part is well-formed,
document opens with python-docx. It says nothing about content or page
count (use check_pages.py for that).

Usage:
    python validate_docx.py <file.docx>
Exit code 0 = OK, 1 = problems found.
"""
import sys
import zipfile
from xml.etree import ElementTree

REQUIRED = ("[Content_Types].xml", "_rels/.rels", "word/document.xml")


def validate(path):
    problems = []
    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, FileNotFoundError) as e:
        return [f"not a readable zip/docx: {e}"]
    with zf:
        bad = zf.testzip()
        if bad:
            problems.append(f"corrupt zip member: {bad}")
        names = set(zf.namelist())
        problems += [f"missing required part: {r}" for r in REQUIRED if r not in names]
        for n in sorted(names):
            if n.endswith((".xml", ".rels")):
                try:
                    ElementTree.fromstring(zf.read(n))
                except ElementTree.ParseError as e:
                    problems.append(f"malformed XML in {n}: {e}")
    try:
        import docx
        docx.Document(path)
    except Exception as e:  # noqa: BLE001 - report any open failure
        problems.append(f"python-docx cannot open it: {e}")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    issues = validate(sys.argv[1])
    if issues:
        print("INVALID")
        for i in issues:
            print(" -", i)
        sys.exit(1)
    print("OK")
