import docker
import subprocess
import requests

class MetaAgent:
    def __init__(self, api_key, model):
        self.client = docker.from_env()
        self.container = self.create_container()
        self.tools = {}
        self.system_prompt = self.generate_system_prompt()
        self.api_key = api_key
        self.model = model

    def create_container(self):
        return self.client.containers.run(
            "meta-agent-env",
            detach=True,
            tty=True,
            remove=True
        )

    def generate_system_prompt(self):
        return """You are Meta-Expert, an extremely clever expert with the unique ability to collaborate with multiple experts to tackle any task and solve complex problems. Your role is to oversee the communication between experts, effectively using their skills to answer given questions while applying your own critical thinking and verification abilities."""

    def process_query(self, query):
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": query}
                ]
            }
        )
        response_json = response.json()
        return self.execute_plan(response_json['choices'][0]['message']['content'])

    def execute_plan(self, plan):
        # Implementation of plan execution
        steps = plan.split('\n')
        result = []
        for step in steps:
            if step.startswith("Expert"):
                expert_name, instruction = step.split(':', 1)
                expert_response = self.consult_expert(expert_name.strip(), instruction.strip())
                result.append(f"{expert_name}: {expert_response}")
            elif step.startswith("Execute"):
                _, command = step.split(':', 1)
                output = self.execute_shell_command(command.strip())
                result.append(f"Command output: {output}")
        return "\n".join(result)

    def execute_shell_command(self, command):
        result = self.container.exec_run(command)
        return result.output.decode('utf-8')

    def install_tool(self, tool_name):
        # Implementation of tool installation
        command = f"apt-get update && apt-get install -y {tool_name}"
        result = self.execute_shell_command(command)
        if "Unable to locate package" in result:
            return f"Failed to install {tool_name}. Package not found."
        elif "0 newly installed" in result:
            return f"{tool_name} is already installed."
        else:
            self.tools[tool_name] = "Installed"
            return f"Successfully installed {tool_name}."

    def update_system_prompt(self):
        # Implementation of system prompt update
        tools_info = ", ".join([f"{tool}: {status}" for tool, status in self.tools.items()])
        self.system_prompt += f"\n\nAvailable tools: {tools_info}"

    def consult_expert(self, expert_name, instruction):
        # Consult an expert (which is actually the same LM with a different prompt)
        expert_prompt = f"You are {expert_name}. {instruction}"
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": expert_prompt},
                    {"role": "user", "content": instruction}
                ]
            }
        )
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
