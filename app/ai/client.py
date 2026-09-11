import os

from dotenv import load_dotenv
from openai import OpenAI


# =====================================================
# ENVIRONMENT
# =====================================================

load_dotenv()


# =====================================================
# OPENAI CLIENT
# =====================================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)