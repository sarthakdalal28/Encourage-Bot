import discord
import os

client = discord.Client()

@client.event #register an event
async def on_ready():  #When bot is ready
  print('We have logged in as {0.user}.format(client)') #0 gets replaced by client 

@client.event
async def on_message(message): #Trigger when a message is received
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!') #Bot will respond to $hello

client.run(os.getenv('TOKEN')) #run the bot