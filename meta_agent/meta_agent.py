import docker
import requests

from config import Config


class MetaAgent:
    def __init__(self, api_key, model):
        self.client = docker.from_env()
        self.tools = {}
        self.api_key = api_key
        self.model = model
        self.system_prompt = """You are Meta-Expert, an advanced AI agent designed to process queries, solve complex problems, and continuously improve your capabilities. Your core functionalities include:

1. Query Processing: You can understand and process natural language queries from users.
2. Expert Collaboration: You have the unique ability to consult with multiple expert AIs to tackle any task.
3. Shell Interaction: You can execute shell commands and interpret their output.
4. Code Execution: You can write, save, and run code in various programming languages.
5. Tool Management: You can install and use necessary tools from the internet.
6. Self-Improvement: You reflect on task results and improve your strategies.
7. Dynamic Knowledge: You maintain and update your knowledge base, including available tools.

Your role is to oversee the entire problem-solving process, effectively using your skills and those of other experts to answer questions and solve problems. Apply critical thinking, verify information, and always strive for the most accurate and efficient solutions.

Remember to consider security implications and use only allowed commands and tools. If a task requires a tool that's not available, you can request its installation.

Your responses should be well-structured, detailing your thought process and the steps you're taking to solve the problem at hand."""
        self.update_system_prompt()

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
            elif step.startswith("Install"):
                _, tool = step.split(':', 1)
                install_result = self.install_tool(tool.strip())
                result.append(f"Tool installation: {install_result}")
                self.update_system_prompt()  # Update system prompt after tool installation
        return "\n".join(result)

    def execute_shell_command(self, command):
        # Implement a whitelist of allowed commands
        allowed_commands = ['ls', 'cat', 'echo', 'pwd']
        command_parts = command.split()
        if command_parts[0] not in allowed_commands:
            return f"Error: Command '{command_parts[0]}' is not allowed"

        container = self.client.containers.run(
            Config.DOCKER_IMAGE,
            command=command,
            remove=True
        )
        return container.decode('utf-8')

    def install_tool(self, tool_name):
        # Implementation of tool installation
        command = f"apt-get update && apt-get install -y {tool_name}"
        container = self.client.containers.run(
            Config.DOCKER_IMAGE,
            command=command,
            remove=True
        )
        result = container.decode('utf-8')
        if "Unable to locate package" in result:
            return f"Failed to install {tool_name}. Package not found."
        elif "0 newly installed" in result:
            return f"{tool_name} is already installed."
        else:
            self.tools[tool_name] = "Installed"
            return f"Successfully installed {tool_name}."

    def update_system_prompt(self, new_information=None):
        if new_information:
            self.system_prompt += f"\n\n{new_information}"

        # Update with available tools
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
