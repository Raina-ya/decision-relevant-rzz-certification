import csv
from pathlib import Path
import re
import unittest


class LiteratureLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "docs" / "literature" / "library.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            cls.rows = list(csv.DictReader(stream))

    def test_ids_and_identifiers_are_unique(self):
        ids = [row["id"] for row in self.rows]
        identifiers = [row["identifier"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_arxiv_identifiers_have_canonical_shape(self):
        for row in self.rows:
            if row["identifier"].startswith("arXiv:"):
                self.assertRegex(row["identifier"], re.compile(r"^arXiv:\d{4}\.\d{4,5}$"))
                self.assertIn(row["identifier"].removeprefix("arXiv:"), row["source_url"])

    def test_abstract_only_rows_are_explicitly_limited(self):
        for row in self.rows:
            if row["reading_status"] == "abstract only":
                self.assertIn("[abstract only]", row["notes"])

    def test_known_mismatched_ids_are_not_supporting_entries(self):
        identifiers = {row["identifier"] for row in self.rows}
        self.assertNotIn("arXiv:2508.10997", identifiers)
        self.assertNotIn("arXiv:2609.28825", identifiers)


if __name__ == "__main__":
    unittest.main()
