from pathlib import Path
import pdfplumber
from docx import Document
import re


def extrair_texto_pdf(caminho_arquivo: str) -> str:
    texto = ""

    try:
        with pdfplumber.open(caminho_arquivo) as pdf:
            for pagina in pdf.pages:
                conteudo = pagina.extract_text()
                if conteudo:
                    texto += conteudo + "\n"

        print("📄 TEXTO EXTRAÍDO:", texto[:500])  # 🔥 DEBUG

        # 🚨 NOVO: validação
        if not texto.strip():
            print("⚠️ PDF sem texto extraível")
            return "CV não legível"

        return texto.strip()
        print("📊 TAMANHO TEXTO:", len(texto) if texto else 0)

    except Exception as e:
        print("🔥 ERRO AO LER PDF:", e)
        return "CV não legível"


def extrair_texto_docx(caminho_arquivo: str) -> str:
    try:
        doc = Document(caminho_arquivo)
        textos = [p.text for p in doc.paragraphs if p.text.strip()]

        texto_final = "\n".join(textos)

        print("📄 DOCX TEXTO:", texto_final[:500])  # DEBUG

        if not texto_final.strip():
            return "CV não legível"

        return texto_final

    except Exception as e:
        print("🔥 ERRO DOCX:", e)
        return "CV não legível"


def extrair_texto_cv(caminho_arquivo: str) -> str:
    extensao = Path(caminho_arquivo).suffix.lower()

    if extensao == ".pdf":
        return extrair_texto_pdf(caminho_arquivo)

    elif extensao == ".docx":
        return extrair_texto_docx(caminho_arquivo)

    elif extensao == ".doc":
        return "Formato .doc não suportado"

    else:
        return "Formato não suportado"
    
 