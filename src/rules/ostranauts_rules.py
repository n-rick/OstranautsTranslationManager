import hashlib

from models.text_unit import TextUnit
from rules.keys_terms import KeyTerms


class OstranautsRules:

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

        if key == KeyTerms.A_VALUES.value:
            units.extend(
                self._extract_aValues(
                    value,
                    path,
                    relative_path,
                )
            )

        elif key in (
            KeyTerms.A_OVERRIDE_VALUES.value,
            KeyTerms.A_OVERRIDE_TRIGGER_IA_VALUES.value,
        ):
            units.extend(
                self._extract_override_values(
                    value,
                    path,
                    relative_path,
                )
            )

        elif key == KeyTerms.A_PHASE_TITLES.value:
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

        return []
    
    
    def _extract_override_values(
        self,
        values: list,
        path: str,
        relative_path: str,
    ) -> list[TextUnit]:

        return []
    
    def _extract_phase_titles(
        self,
        values: list,
        path: str,
        relative_path: str,
    ) -> list[TextUnit]:

        return []