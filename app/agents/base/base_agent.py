from abc import ABC
from datetime import datetime


class BaseAgent(ABC):
    """
    Classe base para todos os agentes do TalentAI.
    """

    NAME = "Base Agent"
    VERSION = "1.0"

    def metadata(self):
        return {
            "agent": self.NAME,
            "version": self.VERSION,
            "executed_at": datetime.now().isoformat()
        }

    def success(self, data=None):
        return {
            "success": True,
            **self.metadata(),
            "data": data
        }

    def error(self, message):
        return {
            "success": False,
            **self.metadata(),
            "error": message
        }