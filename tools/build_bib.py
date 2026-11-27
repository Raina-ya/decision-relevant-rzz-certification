"""Generate the review BibTeX file from the verified literature CSV."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "docs" / "literature" / "library.csv"
OUTPUT = ROOT / "docs" / "literature" / "references.bib"


def bib_escape(value: str) -> str:
    return value.replace("\\", r"\textbackslash{}")


def build_entry(row: dict[str, str]) -> str:
    authors = " and ".join(part.strip() for part in row["authors"].split(";"))
    fields = [
        ("title", "{" + bib_escape(row["title"]) + "}"),
        ("author", "{" + bib_escape(authors) + "}"),
        ("year", "{" + row["year"] + "}"),
    ]
    identifier = row["identifier"]
    if identifier.startswith("arXiv:"):
        arxiv_id = identifier.removeprefix("arXiv:")
        fields.extend(
            [
                ("eprint", "{" + arxiv_id + "}"),
                ("archivePrefix", "{arXiv}"),
            ]
        )
    fields.extend(
        [
            ("url", "{" + row["source_url"] + "}"),
            ("note", "{Reading status: " + row["reading_status"] + "}"),
        ]
    )
    body = ",\n".join(f"  {key} = {value}" for key, value in fields)
    return f"@misc{{{row['id']},\n{body}\n}}"


def main() -> None:
    with LIBRARY.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    text = "% Generated from library.csv by tools/build_bib.py; do not edit by hand.\n\n"
    text += "\n\n".join(build_entry(row) for row in rows) + "\n"
    OUTPUT.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
