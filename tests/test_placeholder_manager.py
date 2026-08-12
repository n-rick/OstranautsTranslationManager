import unittest

from src.models.text_unit import TextUnit
from src.translator.placeholder_manager import PlaceholderManager
from src.translator.google_translator import GoogleTranslatorService


class TestPlaceholderManager(unittest.TestCase):
    def setUp(self):
        self.manager = PlaceholderManager()

    def test_protect_and_restore(self):
        text = "[us] repairs [target]."
        protected = self.manager.protect(text)
        restored = self.manager.restore(protected)
        
        print("\n" + "=" * 70)
        print("test_protect_and_restore")
        print(f"Original: {text}")
        print(f"Protected: {protected}")
        print(f"Restored: {restored}")
        print("=" * 70)
        
        self.assertEqual(restored, text)
    
    def test_protect(self):
        text = "[us] repairs [target]."

        protected = self.manager.protect(text)
        print("\n" + "=" * 70)
        print("test_protect")
        print(f"Original: {text}")
        print(f"Protected: {protected}")
        print("=" * 70)

        self.assertNotIn("[us]", protected)
        self.assertNotIn("[target]", protected)
    
    def test_without_placeholder(self):
        text = "Repair engine."

        protected = self.manager.protect(text)
        restored = self.manager.restore(protected)
        print("\n" + "=" * 70)
        print("test_without_placeholder")
        print(f"Original: {text}")
        print(f"Protected: {protected}")
        print(f"Restored: {restored}")
        print("=" * 70)

        self.assertEqual(text, protected)
        self.assertEqual(text, restored)

    def test_protects_multiple_placeholders(self):
        text = "[us] tells [them] about [target]."

        protected = self.manager.protect(text)
        restored = self.manager.restore(
            protected
        )

        self.assertNotEqual(protected, text)
        self.assertEqual(restored, text)

    def test_translate_preserves_placeholders(self):
        unit = TextUnit(
            uid="1",
            relative_path="test.json",
            json_path="$.strDesc",
            field="strDesc",
            source_text="[us] repairs [target].",
        )

        translator = GoogleTranslatorService()
        translator.translate(unit)

        self.assertIn("[us]", unit.translated_text)
        self.assertIn("[target]", unit.translated_text)


    def test_protects_tags(self):
        text = (
            "Welcome <color=#FF0000>player</color> "
            "<b>to Ostranauts</b>."
        )

        protected = self.manager.protect(text)
        restored = self.manager.restore(protected)

        self.assertNotEqual(protected, text)
        self.assertEqual(restored, text)

    def test_protects_tags_and_placeholders(self):
        text = (
            "[us] tells [them] "
            "<color=#FF0000>something</color>."
        )

        protected = self.manager.protect(text)
        restored = self.manager.restore(protected)

        self.assertNotEqual(protected, text)
        self.assertEqual(restored, text)

    def test_protects_starting_and_return_tokens(self):
        text = "STARTING: Return to [contact] with [target]."

        protected = self.manager.protect(text)
        restored = self.manager.restore(protected)

        self.assertNotIn("STARTING", protected)
        self.assertNotIn("Return", protected)
        self.assertNotIn("Return to", protected)
        self.assertNotIn(" to ", protected)
        self.assertNotIn("[contact]", protected)
        self.assertNotIn("[target]", protected)
        self.assertEqual(restored, text)

if __name__ == '__main__':
    unittest.main()