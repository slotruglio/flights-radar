from googletrans import Translator

def get_translated_city(city):
    translator = Translator()

    translated_text = translator.translate(city, src='it', dest='en')
    print(f"{city} -> {translated_text.text}")
    return translated_text.text.upper()

def get_italian_name(name):
    translator = Translator()

    translated_text= translator.translate(name, src='en', dest='it')
    print(f"{name} -> {translated_text.text}")
    return translated_text.text