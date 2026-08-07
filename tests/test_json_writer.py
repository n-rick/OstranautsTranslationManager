import json
import shutil
import unittest
from pathlib import Path

from src.models.text_unit import TextUnit
from src.models.translation_project import TranslationProject
from src.writer.json_writer import JsonWriter


class TestJsonWriter(unittest.TestCase):

    def setUp(self):
        self.writer = JsonWriter()

        self.input_dir = Path("tests/input")
        self.output_dir = Path("tests/output")

        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.input_dir, ignore_errors=True)
        shutil.rmtree(self.output_dir, ignore_errors=True)
        
    
    def test_write_simple_field(self):
        """Écriture d'un champ JSON simple à la racine"""
        data = {
            "strTitle": "Repair"
        }

        with open(self.input_dir / "sample.json", "w", encoding="utf-8-sig") as file:
            json.dump(data, file)

        project = TranslationProject()
        project.root_directory = str(self.input_dir)

        project.files["sample.json"] = [
            TextUnit(
                uid="1",
                relative_path="sample.json",
                json_path="$.strTitle",
                field="strTitle",
                source_text="Repair",
                translated_text="Réparer"
            )
        ]

        self.writer.write(project, str(self.output_dir))

        with open(self.output_dir / "sample.json", encoding="utf-8-sig") as file:
            result = json.load(file)

        self.assertEqual(result["strTitle"], "Réparer", "test avec chaîne simple")
        

    def test_write_nested_field(self):
        """Écriture d'un champ JSON imbriqué dans une liste/objet"""
        data = {
            "children": [
                {
                    "strDesc": "Repair engine."
                }
            ]
        }

        with open(self.input_dir / "sample.json", "w", encoding="utf-8-sig") as file:
            json.dump(data, file)

        project = TranslationProject()
        project.root_directory = str(self.input_dir)

        project.files["sample.json"] = [
            TextUnit(
                uid="1",
                relative_path="sample.json",
                json_path="$.children[0].strDesc",
                field="strDesc",
                source_text="Repair engine.",
                translated_text="Réparer le moteur."
            )
        ]

        self.writer.write(project, str(self.output_dir))

        with open(self.output_dir / "sample.json", encoding="utf-8-sig") as file:
            result = json.load(file)

        self.assertEqual(
            result["children"][0]["strDesc"],
            "Réparer le moteur.",
            "test avec champ imbriqué"
        )


    def test_write_array_value(self):
        """Écriture d'une valeur spécifique par son index dans un tableau"""
        data = {
            "aValues": [
                "ENGINE",
                "Engine"
            ]
        }

        with open(self.input_dir / "sample.json", "w", encoding="utf-8-sig") as file:
            json.dump(data, file)

        project = TranslationProject()
        project.root_directory = str(self.input_dir)

        project.files["sample.json"] = [
            TextUnit(
                uid="1",
                relative_path="sample.json",
                json_path="$.aValues[1]",
                field="aValues",
                source_text="Engine",
                translated_text="Moteur"
            )
        ]

        self.writer.write(project, str(self.output_dir))

        with open(self.output_dir / "sample.json", encoding="utf-8-sig") as file:
            result = json.load(file)

        self.assertEqual(result["aValues"][1], "Moteur", "test avec valeur de tableau")


    def test_write_preserves_untranslated_fields(self):
        """Vérification que les champs non traduits sont préservés dans le fichier de sortie"""
        data = {
            "strTitle": "Repair",
            "untranslated_key": "Keep Me Unchanged",
            "other_data": {"nested_key": 42}
        }

        with open(self.input_dir / "sample.json", "w", encoding="utf-8-sig") as file:
            json.dump(data, file)

        project = TranslationProject()
        project.root_directory = str(self.input_dir)
        project.files["sample.json"] = [
            TextUnit(
                uid="1",
                relative_path="sample.json",
                json_path="$.strTitle",
                field="strTitle",
                source_text="Repair",
                translated_text="Réparer"
            )
        ]

        self.writer.write(project, str(self.output_dir))

        with open(self.output_dir / "sample.json", encoding="utf-8-sig") as file:
            result = json.load(file)

        # On valide la traduction
        self.assertEqual(result["strTitle"], "Réparer")
        # On valide que le reste n'a pas bougé
        self.assertEqual(result["untranslated_key"], "Keep Me Unchanged")
        self.assertEqual(result["other_data"]["nested_key"], 42)
        
        
    def test_write_multiple_translations(self):
        """Écriture de plusieurs traductions dans le même fichier JSON"""
        data = {
            "strTitle": "Repair",
            "strDesc": "Repair the engine."
        }
        
        with open(self.input_dir / "sample.json", "w", encoding="utf-8-sig") as file:
            json.dump(data, file)
        
        project = TranslationProject()
        project.root_directory = str(self.input_dir)
        project.files["sample.json"] = [
            TextUnit(
                uid="1",
                relative_path="sample.json",
                json_path="$.strTitle",
                field="strTitle",
                source_text="Repair",
                translated_text="Réparer"
            ),
            TextUnit(
                uid="2",
                relative_path="sample.json",
                json_path="$.strDesc",
                field="strDesc",
                source_text="Repair the engine.",
                translated_text="Réparer le moteur."
            )
        ]
        
        self.writer.write(project, str(self.output_dir))
        
        with open(self.output_dir / "sample.json", encoding="utf-8-sig") as file:
            result = json.load(file)
        
        self.assertEqual(result["strTitle"], "Réparer")
        self.assertEqual(result["strDesc"], "Réparer le moteur.")
        

    def test_write_keeps_placeholder_tokens(self):
        """Vérification que les tokens de remplacement sont conservés dans le texte traduit"""
        data = {
            "children": [
                {
                    "strDesc": "[us] repairs the engine."
                }
            ]
        }
        
        with open(self.input_dir / "sample.json", "w", encoding="utf-8-sig") as file:
            json.dump(data, file)
        
        project = TranslationProject()
        project.root_directory = str(self.input_dir)
        project.files["sample.json"] = [
            TextUnit(
                uid="1",
                relative_path="sample.json",
                json_path="$.children[0].strDesc",
                field="strDesc",
                source_text="[us] repairs the engine.",
                translated_text="[us] répare le moteur."
            )
        ]
        
        self.writer.write(project, str(self.output_dir))
        
        with open(self.output_dir / "sample.json", encoding="utf-8-sig") as file:
            result = json.load(file)
        
        
        self.assertIn("[us]", result["children"][0]["strDesc"])