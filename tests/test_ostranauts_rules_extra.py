import json
import unittest
from pathlib import Path

from src.rules.ostranauts_rules import OstranautsRules
from src.scanner.json_extractor import JsonExtractor


class TestOstranautsRulesExtra(unittest.TestCase):

    def test_is_translatable_excludes_strName(self):
        rules = OstranautsRules()
        self.assertFalse(rules.is_translatable("strName", "SomeName"))
        self.assertTrue(rules.is_translatable("strTitle", "Title"))

    def test_excluded_file_is_skipped_by_extractor(self):
        extractor = JsonExtractor()
        result = extractor.extract("/tmp/ai_training/ai_training.json", "ai_training/ai_training.json")
        self.assertEqual(result, [])

    def test_excluded_folder_is_skipped_by_extractor(self):
        extractor = JsonExtractor()
        result = extractor.extract("/tmp/audioemitters/test.json", "audioemitters/test.json")
        self.assertEqual(result, [])
