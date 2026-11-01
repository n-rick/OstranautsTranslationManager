import unittest

from src.translator.deepl_translator import DeepLTranslatorService
from src.translator.google_translator import GoogleTranslatorService


class TestGoogleTranslatorCompatibility(unittest.TestCase):
    def test_legacy_name_uses_deepl_service(self):
        self.assertIs(GoogleTranslatorService, DeepLTranslatorService)