import importlib.util
import json
import pathlib
import tempfile
import unittest


class TestClaim1Table1Audit(unittest.TestCase):
    def test_table_arithmetic_and_honest_scope(self):
        path = pathlib.Path(__file__).parents[1] / "src/claim1_table1_audit.py"
        spec = importlib.util.spec_from_file_location("claim1_table1_audit", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            module.main(directory)
            result = json.loads((pathlib.Path(directory) / "summary.json").read_text())
            self.assertEqual(result["absolute_reduction_percentage_points"], 21.85)
            self.assertEqual(result["verdict"], "inconclusive")


if __name__ == "__main__":
    unittest.main()
