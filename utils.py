from deep_translator import GoogleTranslator

def translate_ru_to_en(text: str) -> str:
    if not text:
        return text
    if any("а" <= ch <= "я" or "А" <= ch <= "Я" for ch in text):
        return GoogleTranslator(source="ru", target="en").translate(text)
    return text
