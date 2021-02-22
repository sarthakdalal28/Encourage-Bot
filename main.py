import discord
import os
import requests
import json
import random

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"] #list of sad words

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
] #list of motivation sentences

def get_quote():
  response = requests.get("https://zenquotes.io/api/random") #Return a random quote from this API
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
  

@client.event #register an event
async def on_ready():  #When bot is ready
  print('We have logged in as {0.user}'.format(client)) #0 gets replaced by client 

@client.event
async def on_message(message): #Trigger when a message is received
  if message.author == client.user:
    return

  msg = message.content  

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote) #Bot will respond to $hello
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

client.run(os.getenv('TOKEN')) #run the bot