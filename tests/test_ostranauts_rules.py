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

    def test_extract_override_values_returns_expected_units(self):
        """Vérification de l'extraction des valeurs d'override."""
        rules = OstranautsRules()

        values = [
            "strTitle|Boop",
            "strDesc|[us] boops [them].",
            "strAnim|Use",
        ]

        units = rules._extract_override_values(values, "$.aOverrideValues", "sample.json")

        self.assertEqual(len(units), 2)
        self.assertEqual(
            [unit.field for unit in units],
            ["strTitle", "strDesc"],
        )
        self.assertEqual(
            [unit.source_text for unit in units],
            ["Boop", "[us] boops [them]."],
        )
