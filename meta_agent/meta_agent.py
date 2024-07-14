import json
import logging
import subprocess

import docker
import requests

from config import Config

logging.basicConfig(level=logging.INFO)


class MetaAgent:
    def __init__(self, api_key, model):
        self.client = docker.from_env()
        self.api_key = api_key
        self.model = model
        self.container_info = self.get_container_info()
        self.system_prompt = self.generate_system_prompt()

    def process_query(self, query):
        return self.feedback_loop(query, 0)

    def feedback_loop(self, query, depth):
        if depth >= Config.MAX_RECURSION_DEPTH:
            return "Maximum recursion depth reached. Final response: " + query

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
        plan = response_json['choices'][0]['message']['content']
        result = self.execute_plan(plan)

        # Check if the result needs further processing
        if "<FEEDBACK_REQUIRED>" in result:
            return self.feedback_loop(result, depth + 1)
        else:
            return result

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
        logging.info(f"Executing shell command: {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            logging.info(f"Shell command output: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command: {e.stderr}")
            return f"Error executing command: {e.stderr}"

    def get_container_info(self):
        logging.info("Getting container info")
        try:
            container_info = {}
            
            # Get container ID
            container_info['container_id'] = subprocess.check_output(['hostname']).decode('utf-8').strip()
            
            # Get Linux distribution info
            with open('/etc/os-release', 'r') as f:
                os_release = dict(l.strip().split('=') for l in f if '=' in l)
            container_info['os'] = {
                'name': os_release.get('NAME', '').strip('"'),
                'version': os_release.get('VERSION', '').strip('"'),
                'id': os_release.get('ID', '').strip('"')
            }
            
            # Get kernel version
            container_info['kernel'] = subprocess.check_output(['uname', '-r']).decode('utf-8').strip()
            
            # Get installed packages
            if container_info['os']['id'] in ['ubuntu', 'debian']:
                packages = subprocess.check_output(['dpkg', '--get-selections']).decode('utf-8')
            elif container_info['os']['id'] in ['centos', 'rhel', 'fedora']:
                packages = subprocess.check_output(['rpm', '-qa']).decode('utf-8')
            else:
                packages = "Unable to determine package list for this OS"
            container_info['installed_packages'] = packages.split('\n')
            
            # Get environment variables
            container_info['environment'] = dict(os.environ)
            
            # Get current working directory
            container_info['cwd'] = os.getcwd()
            
            # Get available shells
            container_info['available_shells'] = subprocess.check_output(['cat', '/etc/shells']).decode('utf-8').split('\n')
            
            logging.info("Container info retrieved successfully")
            return container_info
        except Exception as e:
            logging.error(f"Error getting container info: {str(e)}")
            return f"Error getting container info: {str(e)}"

    def generate_system_prompt(self):
        prompt = """You are Meta-Expert, an advanced AI agent designed to process queries, solve complex problems, and continuously improve your capabilities within a containerized environment. Your core functionalities include:

1. Query Processing: Understand and process natural language queries from users.
2. Expert Collaboration: Consult with multiple expert AIs to tackle any task.
3. Shell Interaction: Execute shell commands and interpret their output.
4. Code Execution: Write, save, and run code in various programming languages within the container.
5. Self-Improvement: Reflect on task results, improve strategies, and build a library of reusable tools and functions.
6. Dynamic Knowledge: Maintain and update your knowledge base, including system capabilities.

Your role is to oversee the entire problem-solving process, effectively using your skills and those of other experts to answer questions and solve problems. Apply critical thinking, verify information, and always strive for the most accurate and efficient solutions.

When processing a query:
1. Analyze the query and break it down into steps if necessary.
2. Determine which experts or tools are needed to solve the problem.
3. Consult experts or use tools as required, interpreting their outputs.
4. Execute code or shell commands when necessary, always considering security implications.
5. Synthesize the information gathered to formulate a comprehensive answer.
6. Reflect on the process and update your knowledge base accordingly.

Security Considerations:
- You have full access to the shell, but remain at the user level to avoid admin password requests.
- Sanitize all inputs to prevent injection attacks.
- Be aware of the limitations and permissions of your containerized environment.

Your responses should be well-structured, detailing your thought process and the steps you're taking to solve the problem at hand. Always strive to provide the most efficient and accurate solution possible.

If you believe your response requires further processing or refinement, include the tag '<FEEDBACK_REQUIRED>' in your response. This will trigger another iteration of processing, allowing you to improve upon your initial answer.

Container Information:
- Container ID: {self.container_info['container_id']}
- Operating System: {self.container_info['os']['name']} {self.container_info['os']['version']}
- Kernel Version: {self.container_info['kernel']}
- Current Working Directory: {self.container_info['cwd']}
- Available Shells: {', '.join(filter(None, self.container_info['available_shells']))}

You have access to the following environment variables:
{json.dumps(self.container_info['environment'], indent=2)}

The container has the following packages installed:
{json.dumps(self.container_info['installed_packages'][:10], indent=2)}  # Showing only first 10 for brevity

Use this information to tailor your responses and commands to the specific environment you're operating in.
"""
        return prompt

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
