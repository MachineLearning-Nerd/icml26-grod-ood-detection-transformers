import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class TestClaim1SyntheticGrodToy(unittest.TestCase):
    def test_fixture_metrics_and_control(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                ["python3", "src/claim1_synthetic_grod_toy.py", "--out", directory],
                cwd=ROOT,
                check=True,
            )
            summary = json.loads((Path(directory) / "summary.json").read_text())
            with (Path(directory) / "results.csv").open() as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(summary["verdict"], "toy")
            self.assertEqual(len(rows), 3)
            self.assertTrue(
                all(
                    float(row["synthetic_after_filter"])
                    < float(row["synthetic_before_filter"])
                    for row in rows
                )
            )
            self.assertTrue(
                all(
                    0 <= float(row["grod_auroc"]) <= 1
                    and 0 <= float(row["grod_fpr95"]) <= 1
                    for row in rows
                )
            )


if __name__ == "__main__":
    unittest.main()
