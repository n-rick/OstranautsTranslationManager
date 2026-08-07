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