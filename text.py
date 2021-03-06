import discord
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ['triste', 'cansado', 'acabado', 'destruido', 'raiva', ':(', 'depressão', 'matar']
starter_encouragements = [
    'Vai dar certo!',
    'Levanta a cabeça meu irmão!!!',
    'Rum, cunversa besta é essa?',
    'Vai sair pra jogar um vôlei que a tristeza passa',
    'Aguenta firme, você consegue',
    'Você é especial!'
]
   
if "responding" not in db.keys():
    db["responding"] = True

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    data = json.loads(response.text)
    quote = "\"" + data[0]['q'] + "\"" + " -" + data[0]['a']
    return quote

def update_encouragements(message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [message]

def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    msg = message.content

    if msg.startswith('-inspire'):
        await message.channel.send(get_quote())

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"].value

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))
            await message.channel.send(':grin:')
    
    if msg.startswith('-new'):
        encouraging_message = msg.split("-new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send('Mensagem de amor adicionada!')

    if msg.startswith('-del'):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("-del ", 1)[1])
            delete_encouragements(index)
            encouragements = db["encouragements"].value
        await message.channel.send(encouragements)

    if msg.startswith('-show'):
        if "encouragements" in db.keys() and len(db["encouragements"].value) > 0:
            await message.channel.send(db["encouragements"].value)
        else:
            await message.channel.send('Sem novas mensagens adicionadas.')
    
    if msg.startswith('-responding'):
        db["responding"] = not db["responding"]
        if db["responding"]:
            await message.channel.send('Bot agora está lhe animando!')
        else:
            await message.channel.send('Mensagens de amor desativadas.')
    
    if msg.lower().find('salve') is not -1:
        await message.channel.send('Salve {.author.name}!'.format(message))

def run(loop, bot_token):
    loop.create_task(client.start(bot_token))