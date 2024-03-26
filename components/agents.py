import openai


def chatgpt_reply(conv: list[dict]) -> str:
    '''conversational agent for chatgpt

    Args:
        conv (list[str]): list of messages

    Returns:
        str: response from chatgpt
    '''
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conv, temperature=0.7
    )

    return completion["choices"][0]["message"]["content"]