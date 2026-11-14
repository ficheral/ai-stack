#!/usr/bin/env python3
"""Converte documento para Markdown e preserva estrutura de tabela.

docling (MIT) para PDF/DOCX complexo; markitdown (MIT) para o resto.
Ambos rodam local, sem API.
"""
import sys, pathlib


def convert(path: str) -> str:
    p = pathlib.Path(path)
    ext = p.suffix.lower()

    if ext in {".pdf", ".docx", ".pptx", ".xlsx"}:
        try:
            from docling.document_converter import DocumentConverter
            return DocumentConverter().convert(str(p)).document.export_to_markdown()
        except ImportError:
            pass

    from markitdown import MarkItDown
    return MarkItDown().convert(str(p)).text_content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: convert.py <arquivo> [saida.md]")
        raise SystemExit(1)
    md = convert(sys.argv[1])
    if len(sys.argv) > 2:
        pathlib.Path(sys.argv[2]).write_text(md, encoding="utf-8")
        print(f"ok -> {sys.argv[2]}")
    else:
        print(md)
