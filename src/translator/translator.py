from models.text_unit import TextUnit


class Translator:

    def translate(self, unit: TextUnit) -> TextUnit:
        raise NotImplementedError