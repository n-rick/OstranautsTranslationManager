import unittest

from src.translator.placeholder_manager import PlaceholderManager


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

if __name__ == '__main__':
    unittest.main()