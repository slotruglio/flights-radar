from googletrans import Translator

def get_translated_city(city):
    translator = Translator()

    translated_text = translator.translate(city, src='it', dest='en')
    print("translated name")
    return translated_text.text.upper()

def get_italian_name(name):
    translator = Translator()

    translated_text= translator.translate(name, src='en', dest='it')
    return translated_text.text