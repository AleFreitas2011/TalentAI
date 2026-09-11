from app.locales import get_translations


class I18N:

    def __init__(self, language="pt-BR"):

        self.language = language
        self.translations = get_translations(language)

    def t(self, key):

        return self.translations.get(key, key)

    def __call__(self, key):

        return self.t(key)