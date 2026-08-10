import hashlib

from src.models.text_unit import TextUnit
from src.models.unit_type import UnitType
from src.rules.json_keys import JsonKeys


class OstranautsRules:

    TRANSLATABLE_KEYS = {
        "strArticleBody",
        "strArticleTitle",
        "strBody",
        "strDesc",
        "strFriendlyDescription",
        "strFriendlyName",
        "strMainFriendly",
        "strMainText",
        "strNameFriendly",
        "strNameShort",
        "strNodeLabel",
        "strTitle",
        "strTooltip",
    }
    
    TRANSLATABLE_OVERRIDE_KEYS = {
        "strDesc",
        "strTitle",
    }

    def is_translatable(
        self,
        key: str,
        value,
    ) -> bool:

        if not isinstance(value, str):
            return False

        return key in self.TRANSLATABLE_KEYS
    
    
    def extract_special_units(
        self,
        key: str,
        value,
        path: str,
        relative_path: str,
    ) -> list[TextUnit]:
        """Extrait les unités de texte des structures particulières d'Ostranauts."""
        
        units: list[TextUnit] = []

        if key == JsonKeys.A_VALUES.value:
            units.extend(
                self._extract_aValues(
                    value,
                    path,
                    relative_path,
                )
            )

        elif key in (
            JsonKeys.A_OVERRIDE_VALUES.value,
            JsonKeys.A_OVERRIDE_TRIGGER_IA_VALUES.value,
        ):
            units.extend(
                self._extract_override_values(
                    value,
                    path,
                    relative_path,
                )
            )

        elif key == JsonKeys.A_PHASE_TITLES.value:
            units.extend(
                self._extract_phase_titles(
                    value,
                    path,
                    relative_path,
                )
            )

        return units
    
    
    def _extract_aValues(
        self,
        values: list,
        path: str,
        relative_path: str,
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
        self,
        values: list,
        path: str,
        relative_path: str,
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
                    type=UnitType.A_OVERRIDE_VALUES
                )
            )

        return units
    
    def _extract_phase_titles(
        self,
        values: list,
        path: str,
        relative_path: str,
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
                    type=UnitType.A_PHASE_TITLES
                )
            )

        return units