from .pt_BR import translations as pt_BR
from .en_US import translations as en_US

LANGUAGES = {
    "pt-BR": pt_BR,
    "en-US": en_US,
}


def get_translations(language="pt-BR"):
    return LANGUAGES.get(language, pt_BR)