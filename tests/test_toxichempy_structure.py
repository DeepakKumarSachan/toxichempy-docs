import importlib
import unittest

import toxichempy


class TestToxiChemPyPackageStructure(unittest.TestCase):
    def test_import_main_package(self):
        """Test if the main `toxichempy` package can be imported."""
        self.assertIsNotNone(toxichempy)

    def test_import_submodules(self):
        """Test if all submodules can be imported (even if empty)."""
        submodules = [
            "toxichempy.chemoinformatics",
            "toxichempy.computational_toxicology",
            "toxichempy.data_collection",
            "toxichempy.experimental_toxicology",
            "toxichempy.machine_learning",
            "toxichempy.risk_assessment",
            "toxichempy.statistical_analysis",
            "toxichempy.utils",
            "toxichempy.visualization",
            "toxichempy.pipeline_framework",
        ]

        for module in submodules:
            with self.subTest(module=module):
                try:
                    importlib.import_module(module)
                except ImportError as e:
                    self.fail(f"Failed to import {module}: {e}")


if __name__ == "__main__":
    unittest.main()
