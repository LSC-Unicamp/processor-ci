from ollama import Client

SERVER_URL = "http://enqii.lsc.ic.unicamp.br:11434"

client = Client(host=SERVER_URL)


def send_prompt(prompt: str, model: str = "qwen2.5:32b") -> tuple[bool, str]:

    response = client.generate(prompt=prompt, model=model)

    if not response or not "response" in response:
        return 0, ""

    return 1, response["response"]
