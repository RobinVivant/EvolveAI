import logging
import os
import subprocess
import json

from config import Config
from llm_client import LLMClient
from command_history import CommandHistory

logging.basicConfig(level=logging.INFO)


class MetaAgent:
    def __init__(self, api_key, model):
        self.llm_client = LLMClient(api_key, model)
        self.command_history = CommandHistory(api_key)
        self.container_info = self.get_container_info()
        self.system_prompt = self.generate_system_prompt()

    def process_query(self, query):
        return self.feedback_loop(query, 0)

    def feedback_loop(self, query, depth):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query}
        ]
        response = self.llm_client.send_request(messages)
        result = self.execute_plan(response)

        if depth + 1 >= Config.MAX_RECURSION_DEPTH:
            return result
        elif "<FEEDBACK_COMPLETE>" in result:
            return result.replace("<FEEDBACK_COMPLETE>", "").strip()
        elif "<FEEDBACK_REQUIRED>" in result:
            return self.feedback_loop(result, depth + 1)
        else:
            return result

    def execute_plan(self, plan):
        result = []
        execute_tag_start = "<Execute>"
        execute_tag_end = "</Execute>"
        
        while execute_tag_start in plan:
            execute_start = plan.index(execute_tag_start)
            execute_end = plan.index(execute_tag_end)
            command = plan[execute_start + len(execute_tag_start):execute_end].strip()
            output = self.execute_shell_command(command)
            result.append(output)
            
            # Add command to history
            reasoning = plan[:execute_start].strip()  # Use the text before the command as reasoning
            self.command_history.add_command(command, output, reasoning)
            
            plan = plan[execute_end + len(execute_tag_end):]
        
        aggregated_result = self.aggregate_results(result)
        return aggregated_result if aggregated_result else plan

    def aggregate_results(self, results):
        if not results:
            return None
        
        prompt = f"Aggregate and summarize the following command outputs:\n\n{json.dumps(results, indent=2)}\n\nProvide a concise summary of the results."
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant that aggregates and summarizes command outputs."},
            {"role": "user", "content": prompt}
        ]
        
        summary_client = LLMClient(self.llm_client.api_key, Config.OPENROUTER_SUMMARY_MODEL)
        return summary_client.send_request(messages)

    @staticmethod
    def execute_shell_command(command):
        logging.info(f"Executing shell command: {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            logging.info(f"Shell command output: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command: {e.stderr}")
            return f"Error executing command: {e.stderr}"

    @staticmethod
    def get_container_info():
        logging.info("Getting container info")
        try:
            container_info = {'container_id': subprocess.check_output(['hostname']).decode('utf-8').strip()}

            with open('/etc/os-release', 'r') as f:
                os_release = dict(l.strip().split('=') for l in f if '=' in l)
            container_info['os'] = {
                'name': os_release.get('NAME', '').strip('"'),
                'version': os_release.get('VERSION', '').strip('"'),
                'id': os_release.get('ID', '').strip('"')
            }

            container_info['kernel'] = subprocess.check_output(['uname', '-r']).decode('utf-8').strip()
            container_info['environment'] = dict(os.environ)
            container_info['cwd'] = os.getcwd()
            container_info['available_shells'] = subprocess.check_output(['cat', '/etc/shells']).decode('utf-8').split('\n')

            logging.info("Container info retrieved successfully")
            return container_info
        except Exception as e:
            logging.error(f"Error getting container info: {str(e)}")
            return f"Error getting container info: {str(e)}"

    def generate_system_prompt(self):
        command_history = self.command_history.get_history()
        history_str = "\n".join(command_history) if command_history else "No command history available yet."

        prompt = f"""You are an advanced AI agent designed to process queries, solve complex problems, and operate within a containerized environment. Your core functionalities include:

1. Query Processing: Understand and process natural language queries from users.
2. Shell Interaction: Execute shell commands and interpret their output.
3. Problem Solving: Break down complex problems into manageable steps and provide solutions.
4. Self-Improvement: Reflect on task results and improve strategies.

When processing a query:
1. Analyze the query and break it down into steps if necessary.
2. Determine the best approach to solve the problem.
3. Execute shell commands when necessary, always considering security implications.
4. Synthesize the information gathered to formulate a comprehensive answer.
5. Reflect on the process and improve your problem-solving strategies.

To execute a shell command, use the following format:
<Execute>[Your shell command]</Execute>

For example:
<Execute>ls -la</Execute>

Security Considerations:
- You have full access to the shell, but remain at the user level to avoid admin password requests.
- Sanitize all inputs to prevent injection attacks.
- Be aware of the limitations and permissions of your containerized environment.

Your responses should be well-structured, detailing your thought process and the steps you're taking to solve the problem at hand. Always strive to provide the most efficient and accurate solution possible.

If you believe your response requires further processing or refinement, include the tag '<FEEDBACK_REQUIRED>' in your response. This will trigger another iteration of processing, allowing you to improve upon your initial answer.

If you are confident that your response is complete and no further processing is needed, include the tag '<FEEDBACK_COMPLETE>' in your response. This will signal that the feedback loop should end, and your response will be returned as the final answer.

Container Information:
- Container ID: {self.container_info['container_id']}
- Operating System: {self.container_info['os']['name']} {self.container_info['os']['version']}
- Kernel Version: {self.container_info['kernel']}
- Current Working Directory: {self.container_info['cwd']}
- Available Shells: {', '.join([shell for shell in self.container_info['available_shells'] if shell])}

You have access to the following environment variables:
{json.dumps(self.container_info['environment'], indent=2)}

Use this information to tailor your responses and commands to the specific environment you're operating in.

Command History:
{history_str}

Use the command history to inform your decisions and avoid repeating unnecessary commands.
"""
        return prompt
