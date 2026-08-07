import unittest

from src.rules.ostranauts_rules import OstranautsRules
from src.rules.json_keys import JsonKeys


class TestOstranautsRules(unittest.TestCase):

    def test_extract_aValues_returns_expected_values(self):
        '''Vérification de retour des valeurs avec aValues'''
        rules = OstranautsRules()

        values = [
            "ENGINE",
            "Engine",
            "REACTOR",
            "Reactor",
        ]

        units = rules._extract_aValues(values, "$.aValues", "sample.json")

        self.assertEqual(
            [unit.source_text for unit in units],
            ["Engine", "Reactor"],
        )
