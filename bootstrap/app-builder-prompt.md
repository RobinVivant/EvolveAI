# Meta-Agent Application Development

## Objective
Develop a meta-agent application that can interact with a human, perform tasks, and continuously improve its capabilities.

## Core Functionalities

1. **Query Processing**
   - Accept and process natural language queries (prompts) from a human user.

2. **Containerized Environment**
   - Run the agent inside a Docker container.
   - Provide access to a shell within the container.
   - Enable internet access through the shell.

3. **Shell Interaction**
   - Execute shell commands and capture their output.
   - Parse and interpret shell output for further processing.

4. **Code Execution**
   - Write code in various programming languages.
   - Save code to files within the container.
   - Compile and run code using appropriate tools.
   - Capture and analyze the output of code execution.

5. **Tool Management**
   - Download and install necessary tools from the internet.
   - Maintain a record of installed tools and their purposes.

6. **Self-Improvement**
   - Reflect on the results of executed tasks.
   - Iterate and improve strategies based on outcomes.
   - Build and maintain a library of reusable tools and functions.

7. **Dynamic System Prompt**
   - Generate and update a system prompt for each iteration.
   - Incorporate the growing library of tools into the system prompt.

## Technical Requirements

1. Use a suitable programming language for the main application (e.g., Python).
2. Implement a robust Docker configuration for the containerized environment.
3. Develop a secure method for executing shell commands and managing their output.
4. Create a flexible code execution engine that supports multiple programming languages.
5. Design a modular architecture to allow for easy expansion of capabilities.
6. Implement proper error handling and logging throughout the application.
7. Ensure efficient management of system resources within the container.

## Security Considerations

1. Implement safeguards to prevent unauthorized access or malicious use.
2. Sanitize user inputs to prevent injection attacks.
3. Limit the permissions and capabilities of the container to minimize potential risks.
4. Implement proper isolation between the meta-agent and the host system.

## Deliverables

1. Source code for the meta-agent application.
2. Dockerfile and any necessary configuration files.
3. Documentation on how to set up and run the application.
4. User guide explaining how to interact with the meta-agent.
5. Technical documentation detailing the architecture and key components.

## Evaluation Criteria

1. Functionality: Does the meta-agent successfully perform all required tasks?
2. Robustness: How well does it handle errors and unexpected situations?
3. Scalability: Can new capabilities be easily added to the system?
4. Security: Are proper security measures implemented throughout?
5. Performance: Does the meta-agent operate efficiently within resource constraints?
6. Code Quality: Is the code well-structured, documented, and maintainable?

Please proceed with the development of this meta-agent application, ensuring that all specified functionalities and requirements are met.