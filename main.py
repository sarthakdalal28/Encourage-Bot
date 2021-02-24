import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"] #list of sad words

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
] #list of motivation sentences

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random") #Return a random quote from this API
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
  
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

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

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New Encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN')) #run the bot