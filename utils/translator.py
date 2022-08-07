from googletrans import Translator

def get_translated_city(city):
    translator = Translator()

    translated_text = translator.translate(city, src='it', dest='en')
    return translated_text.text.upper()