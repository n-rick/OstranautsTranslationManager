import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import deepl

from src.config.config import Config
from src.models.text_unit import TextUnit
from src.translator.deepl_translator import DeepLTranslatorService
from src.translator.translator import (
    TranslationRateLimitError,
    TranslationServiceError,
)


class TestDeepLTranslatorService(unittest.TestCase):
    def setUp(self):
        self.key_patcher = patch.object(Config, "DEEPL_AUTH_KEY", "test-auth-key")
        self.key_patcher.start()
        self.addCleanup(self.key_patcher.stop)

        self.translator_patcher = patch(
            "src.translator.deepl_translator.deepl.Translator"
        )
        self.translator_factory = self.translator_patcher.start()
        self.addCleanup(self.translator_patcher.stop)
        self.translator = MagicMock()
        self.translator_factory.return_value = self.translator
        self.service = DeepLTranslatorService()

    def test_translate_uses_deepl_and_returns_translation(self):
        self.translator.translate_text.return_value = SimpleNamespace(
            text="Détruire Self __PH_0000__"
        )
        unit = TextUnit(
            uid="1",
            relative_path="interactions.json",
            json_path="$.strTitle",
            field="strTitle",
            source_text="Destroy Self Start",
        )

        result = self.service.translate(unit)

        self.assertIs(result, unit)
        self.assertEqual(unit.translated_text, "Détruire Self Start")
        self.translator.translate_text.assert_called_once_with(
            "Destroy Self __PH_0000__",
            source_lang="EN",
            target_lang="FR",
            preserve_formatting=True,
        )

    def test_translate_preserves_placeholders(self):
        self.translator.translate_text.side_effect = lambda text, **kwargs: (
            SimpleNamespace(text=text)
        )
        unit = TextUnit(
            uid="1",
            relative_path="interactions.json",
            json_path="$.strDesc",
            field="strDesc",
            source_text="[us] repairs [target].",
        )

        self.service.translate(unit)

        self.assertIn("[us]", unit.translated_text)
        self.assertIn("[target]", unit.translated_text)

    def test_translate_wraps_rate_limit_errors(self):
        self.translator.translate_text.side_effect = deepl.TooManyRequestsException(
            "Too many requests"
        )
        unit = TextUnit("1", "sample.json", "$.title", "strTitle", "Title")

        with self.assertRaises(TranslationRateLimitError):
            self.service.translate(unit)

    def test_translate_wraps_other_deepl_errors(self):
        self.translator.translate_text.side_effect = deepl.AuthorizationException(
            "Invalid authorization key"
        )
        unit = TextUnit("1", "sample.json", "$.title", "strTitle", "Title")

        with self.assertRaises(TranslationServiceError):
            self.service.translate(unit)

    def test_missing_auth_key_fails_before_network_request(self):
        with patch.object(Config, "DEEPL_AUTH_KEY", " "):
            with self.assertRaisesRegex(ValueError, "DEEPL_AUTH_KEY"):
                DeepLTranslatorService()


if __name__ == "__main__":
    unittest.main()