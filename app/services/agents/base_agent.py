from abc import ABC
from datetime import datetime


class BaseAgent(ABC):
    """
    Classe base para todos os agentes do TalentAI.
    """

    def __init__(self, nome):
        self.nome = nome

    def log(self, mensagem):
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"[{self.nome}] {mensagem}"
        )