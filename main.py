import openai
import discord
import os
from components.Brave import brave_api, extract_descriptions_and_urls_to_json
from components.agents import chatgpt_reply

# Load credentials from .cred.yml
# resorting to yml file because dotenv is not working ATM

# Extraction of credentials from env variables

cred = {
    "BOT_TOKEN": os.environ.get("BOT_TOKEN"),
    "OPENAI_API_TOKEN": os.environ.get("OPENAI_API_TOKEN"),
    "BRAVE_TOKEN": os.environ.get("BRAVE_TOKEN"),
}
print(cred)
token = cred["BOT_TOKEN"]
openai.api_key = cred["OPENAI_API_TOKEN"]
brave = cred["BRAVE_TOKEN"]


# set up agents persona and role
RAG_msg_system = """Tu es LacDuSchultz,
tu es un cygne majestueux qui navigue sur l'océan
 infini de notre discord.
Tu finiras toutes tes réponses par 'Couack!' précédé d'un emoji canard.
Tu es là pour répondre du mieux possible aux questions des gens.
Si tu n'as pas la réponse, tu peux synthétiser les resultats sérialisés
 qui te seront fournis pour répondre aux questions.
Cite les sources et les liens dès que possible.
Limite tes réponses à 2000 caractères maximum.
"""

RAG_conv = [{"role": "system", "content": RAG_msg_system}]

casual_msg_system = """
Tu es LacDuSchultz, tu es un cygne majestueux qui navigue sur l'océan
 infini de notre discord.
Tu es là pour interagir et badinet avec les utilisateurs du discord.
Tu finiras toutes tes réponses par 'Couack!' précédé d'un emoji canard.
Limite tes réponses à 2000 caractères maximum.
"""

casual_conv = [{"role": "system", "content": casual_msg_system}]

oracle_msg_system = """
Tu vas classifier les questions que l'ont te pose en deux categories:
- Recherche d'informations:
L'utilisateur te pose une question très précise et/ou technique qui nécessite
des informations en plus de tes connaissances actuelles.
- Discussions et instructions:
L'utilisateur cherche seulement à converser avec toi et te demande de générer
des textes ou autres.
Tu ne peux répondre que par '0' ou '1'. rien d'autres.
Si la catégorie est Recherche d'informations,
alors tu réponds 0 sinon tu réponds 1.
"""

oracle_conv = [{"role": "system", "content": oracle_msg_system}]

history = [{"role": "system",
            "content": "voici l'historique de la conversion:"}]
# connect to discord
intents = discord.Intents.all()
client = discord.Client(intents=intents)


# log
@client.event
async def on_ready() -> None:
    print("Logged as {0.user}".format(client))


# answerer
@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    if (
        message.channel.name == "général"
        and client.user.mentioned_in(message)
        and message.mention_everyone is False
    ):
        async with message.channel.typing():
            # image route
            conv = []
            if message.attachments:
                vision_input = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": message.content},
                            {
                                "image_url": message.attachments[0].url,
                                "type": "image_url",
                            },
                        ],
                    }
                ]
                reply = chatgpt_reply(
                    mode="gpt-4-vision-preview", conv=vision_input, temp=0.7
                )
            # text route
            else:
                msg = message.content
                oracle_prompt = oracle_conv.copy()
                oracle_prompt.append({"role": "user", "content": msg})
                response_oracle = chatgpt_reply(
                    mode="gpt-3.5-turbo", conv=oracle_prompt, temp=0
                )
                # TODO :limit tokens
                print(response_oracle)
                # RAG route
                if response_oracle == "0":
                    resultat_api = extract_descriptions_and_urls_to_json(
                        brave_api(msg, brave)
                    )
                    history.append({"role": "user", "content": msg})
                    history.append(
                        {"role": "system",
                         "content": str(resultat_api["results"][:5])}
                    )
                    conv = RAG_conv.copy()
                    conv.extend(history)
                    reply = chatgpt_reply(mode="gpt-4", conv=conv)
                    history.append({"role": "assistant", "content": reply})
                # Conversation route
                else:
                    history.append({"role": "user", "content": msg})
                    conv = casual_conv.copy()
                    conv.extend(history)
                    reply = chatgpt_reply(mode="gpt-4", conv=conv)
                    history.append({"role": "assistant", "content": reply})
        if len(reply) > 2000:
            reply = reply[:1995] + "..."
        await message.reply(reply, mention_author=True)
        # if the history contains more than 10 messages, pop 2 messages
        print(history)
        if len(history) > 10:
            history.pop(1)
            history.pop(1)


# lancement de l'appli
client.run(token)
