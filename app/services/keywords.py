import re
from collections import Counter

STOPWORDS = {
    "a","o","as","os","um","uma","uns","umas",
    "de","da","do","das","dos","para","por","com","sem",
    "em","no","na","nos","nas",
    "e","ou","que","se","como",
    "the","and","or","for","with","in","on","at",
    "to","from","of","is","are","be",
    "vaga","cargo","perfil","experiencia","experiência",
    "projeto","projetos","atividade","atividades"
}

TERMOS_PRIORITARIOS = {
    "sap":5,
    "abap":5,
    "java":4,
    "python":4,
    "aws":4,
    "azure":4,
    "react":4,
    "node":4,
    "sql":4,
    "oracle":4,
    "ingles":3,
    "inglês":3,
    "english":3,
    "fluente":3,
    "senior":3,
    "sênior":3,
    "pleno":2,
    "junior":2,
    "s/4hana":5,
    "hana":4,
    "cpi":4,
    "pi/po":4,
    "sd":4,
    "mm":4,
    "fico":4,
    "docker":3,
    "kubernetes":3,
    "api":3,
    "rest":3,
    "soap":3,
    "odata":3,
    "idoc":4
}

def extrair_palavras_chave(descricao: str, top_n: int = 5):

    if not descricao:
        return []

    texto = descricao.lower()

    texto = texto.replace("s/4 hana","s/4hana")
    texto = texto.replace("s4 hana","s/4hana")
    texto = texto.replace("pi po","pi/po")

    texto = re.sub(r"[^a-zà-ú0-9\s\/\+\#\-]", " ", texto)

    tokens = texto.split()

    scores = Counter()

    for token in tokens:

        if len(token) < 2:
            continue

        if token in STOPWORDS:
            continue

        peso = 1 + TERMOS_PRIORITARIOS.get(token,0)

        scores[token] += peso

    resultado = [palavra for palavra,_ in scores.most_common(top_n)]

    return resultado