"""Compatibilité des anciens imports : le service utilise désormais DeepL."""

from src.translator.deepl_translator import DeepLTranslatorService

GoogleTranslatorService = DeepLTranslatorService
