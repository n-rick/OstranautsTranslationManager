"""Règles spécifiques pour l'extraction des textes dans Ostranauts."""
import hashlib
from src.models.text_unit import TextUnit
from src.models.unit_type import UnitType
from src.rules.json_keys import JsonKeys

class OstranautsRules:
    """Contient les règles spécifiques pour identifier les textes traduisibles dans Ostranauts."""

    # Clés JSON qui sont TOUJOURS traduisibles
    TRANSLATABLE_KEYS = {
        "strTitle",
        "strDesc",
        "strTooltip",
        "strBody",
        "strMainText",
        "strMainFriendly",
        "strNameShort",
        "strFriendlyName",
        "strFriendlyDescription",
        "strNameFriendly",
        "strArticleTitle",
        "strArticleBody",
        "strNodeLabel",
        "strText",
        "strMessage",
        "strFluff",
        "strSuccess",
        "strFail",
        "strLog",
        "strNamePlural",
    }

    # Clés JSON qui sont traduisibles dans les structures de override
    TRANSLATABLE_OVERRIDE_KEYS = {
        "strTitle",
        "strDesc",
    }

    # Clés JSON qui NE DOIVENT JAMAIS être traduites
    NON_TRANSLATABLE_KEYS = {
        "mapModeSwitches",
        "mapGUIPropMaps",
        "strColor",
        "LootCondsUs",
        "LootCondsThem",
        "CTTestUs",
        "CTTestThem",
        "PSpecTestThem",
        "PSpecTest3rd",
        "strLootRELChangeUsSeesThem",
        "strLootRELChangeUsSees3rd",
        "aAModesAddedThem",
        "aInverse",
        "aSocketForbids",
        "strName",  # IMPORTANT: strName est un identifiant, NE PAS TRADUIRE
        "strID",
        "strType",
        "strPortraitImg",
        "strInternalName",
        "strTag",
        "strCategory",
        "strCondLoot",
        "strImgNorm",
        "strCOBase",
        "strPath",
        "strIcon",
        "strImg",
        "strImgDamaged",
        "strLootClientFaction",
        "strSound",
        "type",
        "subtype",
    }

    # Fichiers ou dossiers à exclure de la traduction
    EXCLUDED_FILES = {
        "ai_training/ai_training.json",
        "ai_training/robots.json",
        "ai_training/",
        "audioemitters/", # Émetteurs sonores (technique)
        "colors/",        # Couleurs (technique)
        "condowners/",      # template des objets
        "condtrigs/",
        "cooverlays/cooverlays_cargopods.json",
        "chargeprofiles/",
        "crewskins/",
        "crime/",
        "explosions/",
        "gasrespires/",   # Consommation de gaz (technique)
        "guipropmaps/",   # Mappings UI (technique)
        "jobs/",
        "lifeevents/",
        "lights/",
        "loot/",
        "music/",
        "music_stations/",
        "names_first/",   # Prénoms (ne pas traduire)
        "names_full/",    # Noms complets (ne pas traduire)
        "names_last/",    # Noms de famille (ne pas traduire)
        "names_robots/",
        "names_ship/",    # Noms de vaisseaux (ne pas traduire)
        "names_ship_adjectives/",
        "names_ship_nouns/",
        "parallax/",
        "personspecs/",
        "plot_beats/",
        "plot_manager/",
        "powerinfos/",    # Infos puissance (technique)
        "schemas/",
        "ships/",
        "shipspecs/",
        "slot_effects/",
        "starsystem/",    # Système stellaire (technique)
        "tickers/",       # Minutages (technique)
        "tokens/verbs.json",
        "tokens/names.json",
        "tokens/placeholders.json",
        "tokens/",       # Dictionnaires techniques (verbes, noms)
        "traitscores/",   # Scores de traits (technique)
        "transit/",
        "tsv/",
        "wounds/",
        "zone_triggers/",
    }

    def is_translatable(self, key: str, value) -> bool:
        """Vérifie si une clé JSON doit être traduite."""
        if not isinstance(value, str):
            return False
        # Vérifier si la clé est explicitement non traduisible
        if key in self.NON_TRANSLATABLE_KEYS:
            return False
        # Vérifier si la clé est dans les clés traduisibles
        return key in self.TRANSLATABLE_KEYS

    def should_exclude_file(self, relative_path: str) -> bool:
        """Vérifie si un fichier doit être exclu de la traduction."""
        for excluded in self.EXCLUDED_FILES:
            if excluded in relative_path or relative_path.startswith(excluded):
                return True
        return False

    def extract_special_units(
        self, key: str, value, path: str, relative_path: str
    ) -> list[TextUnit]:
        """Extrait les unités de texte des structures particulières d'Ostranauts."""
        units: list[TextUnit] = []

        # Exclure les fichiers qui ne doivent pas être traduits
        if self.should_exclude_file(relative_path):
            return units

        if key == JsonKeys.A_VALUES.value:
            units.extend(
                self._extract_aValues(value, path, relative_path)
            )
        elif key in (
            JsonKeys.A_OVERRIDE_VALUES.value,
            JsonKeys.A_OVERRIDE_TRIGGER_IA_VALUES.value,
        ):
            units.extend(
                self._extract_override_values(value, path, relative_path)
            )
        elif key == JsonKeys.A_PHASE_TITLES.value:
            units.extend(
                self._extract_phase_titles(value, path, relative_path)
            )
        return units

    def _extract_aValues(
        self, values: list, path: str, relative_path: str
    ) -> list[TextUnit]:
        units: list[TextUnit] = []
        for index in range(0, len(values) - 1, 2):
            key = values[index]
            value = values[index + 1]
            if not isinstance(key, str):
                continue
            if not isinstance(value, str):
                continue
            if not key.isupper():
                continue
            uid = hashlib.sha1(
                f"{relative_path}:{path}[{index + 1}]".encode("utf-8")
            ).hexdigest()
            units.append(
                TextUnit(
                    uid=uid,
                    relative_path=relative_path,
                    json_path=f"{path}[{index + 1}]",
                    field="aValues",
                    source_text=value,
                    type=UnitType.A_VALUES,
                )
            )
        return units

    def _extract_override_values(
        self, values: list, path: str, relative_path: str
    ) -> list[TextUnit]:
        units: list[TextUnit] = []
        for index, item in enumerate(values):
            if not isinstance(item, str):
                continue
            if "|" not in item:
                continue
            key, text = item.split("|", 1)
            if key not in self.TRANSLATABLE_OVERRIDE_KEYS:
                continue
            uid = hashlib.sha1(
                f"{relative_path}:{path}[{index}]".encode("utf-8")
            ).hexdigest()
            units.append(
                TextUnit(
                    uid=uid,
                    relative_path=relative_path,
                    json_path=f"{path}[{index}]",
                    field=key,
                    source_text=text,
                    type=UnitType.A_OVERRIDE_VALUES,
                )
            )
        return units

    def _extract_phase_titles(
        self, values: list, path: str, relative_path: str
    ) -> list[TextUnit]:
        units: list[TextUnit] = []
        for index, text in enumerate(values):
            if not isinstance(text, str):
                continue
            uid = hashlib.sha1(
                f"{relative_path}:{path}[{index}]".encode("utf-8")
            ).hexdigest()
            units.append(
                TextUnit(
                    uid=uid,
                    relative_path=relative_path,
                    json_path=f"{path}[{index}]",
                    field="aPhaseTitles",
                    source_text=text,
                    type=UnitType.A_PHASE_TITLES,
                )
            )
        return units
