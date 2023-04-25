import discord
import responses
from config import TOKEN_DISCORD as TOKEN
# from config import TOKEN


# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print("Discord Message - Exception - " + str(e))
        response = 'Issue accured'
        await message.author.send(response) if is_private else await message.channel.send(response)


def convert_to_european_number(string):
    # Ersetzen des Kommas durch Punkte und Entfernen von Leerzeichen
    string = string.replace(',', '.').replace(' ', '')
    
    # Suchen nach dem Dezimalpunkt
    decimal_index = string.find('.')
    
    # Wenn kein Dezimalpunkt gefunden wurde, wird der String als Ganzzahl interpretiert
    if decimal_index == -1:
        number = int(string)
    else:
        # Extrahieren der Ganzzahl- und Nachkommastellen
        integer_part = int(string[:decimal_index])
        decimal_part = int(string[decimal_index+1:])
        
        # Kombinieren der Ganzzahl- und Nachkommastellen zur europäischen Zahl
        number = float(f"{integer_part}.{decimal_part}")
    
    # Rückgabe der europäischen Zahl
    return "{:,}".format(number).replace(',', '.')
    

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)    

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # If the user message contains a '?' in front of the text, it becomes a private message
        # if user_message[0] == '?':
        #     user_message = user_message[1:]  # [1:] Removes the '?'
        #     await send_message(message, user_message, is_private=True)
        # else:

        await send_message(message, user_message, is_private=False)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)