class TalentAIKernel:

    VERSION = "2.1"

    def __init__(self):

        self.started_at = datetime.now()

        self.agents = {}

        self.engines = {}

        self.providers = {}

        self.memory = {}

        self.settings = {}

        print("🚀 TalentAI Kernel iniciado.")

    def status(self):

        return {

            "version": self.VERSION,

            "started_at": self.started_at.isoformat(),

            "agents": len(self.agents),

            "engines": len(self.engines),

            "providers": len(self.providers)

        }

    def register_agent(self, name, agent):

        self.agents[name] = agent

        print(f"✅ Agent registrado: {name}")

    def get_agent(self, name):

        return self.agents.get(name)

    def list_agents(self):

        return list(self.agents.keys())