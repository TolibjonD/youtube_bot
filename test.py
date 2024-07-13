from googletrans import Translator

async def translate(text, to_lang="en", from_lang="uz"):
    translator = Translator()
    translated_text = translator.translate(text=text, dest=to_lang)
    return translated_text.text