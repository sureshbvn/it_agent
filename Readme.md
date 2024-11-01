# Project Title

This project is a Python-based agent that utilizes OpenAI's GPT-3.5-turbo model to interact with users and perform specific tasks using predefined tools. The agent can handle various prompts and execute corresponding tools to provide responses.

## Features

- **Tool Integration**: The agent can integrate multiple tools such as `laptop_issuance` and `documentation_checklist`.
- **OpenAI Model**: Utilizes OpenAI's GPT-3.5-turbo model for generating responses.
- **Interactive CLI**: Provides an interactive command-line interface for user interaction.

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `config.yaml` file in the `configs` directory with the necessary API keys and configurations.
    - Example `config.yaml`:
        ```yaml
        OPENAI_API_KEY: 'your_openai_api_key'
        ```

## Usage

1. **Run the agent**:
    ```bash
    python agents/agent.py
    ```

2. **Interact with the agent**:
    - The agent will prompt you to "Ask me anything".
    - Type your query and press Enter.
    - To exit, type `exit` and press Enter.

## Example

```python
# Example usage
if __name__ == "__main__":

    tools = [laptop_issuance, documentation_checklist]

    # Uncomment below to run with OpenAI
    model_service = OpenAIModel
    model_name = 'gpt-3.5-turbo'
    stop = None

    agent = Agent(tools=tools, model_service=model_service, model_name=model_name, stop=stop)

    while True:
        prompt = input("Ask me anything: ")
        if prompt.lower() == "exit":
            break
    
        agent.work(prompt)
```

### Sample Interaction

```
Ask me anything: i am rohit. will i get a laptop
Response from OpenAI model: {'tool_choice': 'laptop_issuance', 'tool_input': '{"new_hire_name": "Rohit"}'}
Hi Rohit, your laptop issuance is currently in progress. We’ll notify you once it ships!
Ask me anything:
```

## Contributing

1. **Fork the repository**.
2. **Create a new branch**.
3. **Make your changes**.
4. **Submit a pull request**.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.