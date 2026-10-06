"""
Dump the exact paragraph/run structure of a .docx file as JSON.

Every paragraph's visible text, alignment, bullet status, tab stops, and
per-run formatting (bold, italic, color, size) is reported so that a
replacement plan can be written that reuses the same formatting exactly.

Usage:
    python docx_inspect.py <input.docx> [output.json]

If output.json is omitted, JSON is printed to stdout.
"""
import json
import sys

import docx
from docx.oxml.ns import qn


def _color_hex(run):
    try:
        c = run.font.color
        if c is not None and c.type is not None and c.rgb is not None:
            return str(c.rgb)
    except Exception:
        pass
    return None


def _pt(value):
    return None if value is None else round(value.pt, 2)


def inspect(path):
    d = docx.Document(path)
    paragraphs = []
    for i, p in enumerate(d.paragraphs):
        runs = []
        for r in p.runs:
            runs.append(
                {
                    "text": r.text,
                    "bold": r.font.bold,
                    "italic": r.font.italic,
                    "color": _color_hex(r),
                    "size_pt": _pt(r.font.size),
                }
            )
        pf = p.paragraph_format
        num_pr = p._p.find(qn("w:pPr") + "/" + qn("w:numPr"))
        tabs = [(t.position, str(t.alignment)) for t in pf.tab_stops]
        paragraphs.append(
            {
                "index": i,
                "text": p.text,
                "alignment": str(p.alignment) if p.alignment is not None else None,
                "is_bullet": num_pr is not None,
                "tabs": tabs,
                "runs": runs,
            }
        )
    return {
        "source": str(path),
        "paragraph_count": len(paragraphs),
        "paragraphs": paragraphs,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python docx_inspect.py <input.docx> [output.json]", file=sys.stderr)
        sys.exit(2)
    data = inspect(sys.argv[1])
    text = json.dumps(data, ensure_ascii=False, indent=1)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {sys.argv[2]}")
    else:
        print(text)
