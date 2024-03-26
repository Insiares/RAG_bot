import openai


def chatgpt_reply(mode: str, conv: list[dict], temp: float = 0.7) -> str:
    '''conversational agent for chatgpt

    Args:
        mode (str): gpt-3.5-turbo or gpt-4
        temp (float): temperature
        conv (list[str]): list of messages

    Returns:
        str: response from chatgpt
    '''
    completion = openai.ChatCompletion.create(
        model=mode, messages=conv, temperature=temp
    )

    return completion["choices"][0]["message"]["content"]
