"""
Scale paragraph spacing (space-before / space-after) across an entire .docx
by a fixed factor, to reclaim vertical space when a translation overflows
the source's page count.

This never touches font size, margins, or line spacing within a paragraph —
only the gap between paragraphs and around headings. It is deliberately a
separate, explicit step from the content rewrite: compressing wording
(docx_rewrite.py's job) should always be tried first, since it doesn't
change the document's visual density at all. Scaling spacing does change
density slightly, so only use it once the user has agreed to it.

A factor of 1.0 changes nothing. 0.75 tightens every paragraph gap by a
quarter. Only paragraphs that already have an explicit space_before or
space_after set are touched; paragraphs inheriting spacing from the style
are left alone (there's nothing explicit here to scale).

Usage:
    python scale_spacing.py <input.docx> <factor> <output.docx>
"""
import sys

import docx
from docx.shared import Emu


def scale_spacing(input_path, factor, output_path):
    d = docx.Document(input_path)
    touched = 0
    for p in d.paragraphs:
        pf = p.paragraph_format
        if pf.space_before is not None:
            pf.space_before = Emu(round(pf.space_before.emu * factor))
            touched += 1
        if pf.space_after is not None:
            pf.space_after = Emu(round(pf.space_after.emu * factor))
            touched += 1
    d.save(output_path)
    print(f"Scaled spacing on {touched} paragraph-spacing value(s) by factor {factor}. Saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scale_spacing.py <input.docx> <factor> <output.docx>", file=sys.stderr)
        sys.exit(2)
    scale_spacing(sys.argv[1], float(sys.argv[2]), sys.argv[3])
