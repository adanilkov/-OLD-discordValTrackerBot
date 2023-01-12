import os
import discord
from bs4 import BeautifulSoup
import requests
import re


client = discord.Client()
command_list = {
  'help' : 'Displays commands',
  'history' : 'Displays the player\'s match history.',
  'rank' : 'Displays the player\'s current rank.',
  'peak' : 'Displays the player\'s peak rank.'
}


def linkconstruct(command):
  namelink = command[2:]
  temp = command.pop()
  region = temp.split('#')
  link = ['https://tracker.gg/valorant/profile/riot/']
  for i in range(len(namelink)-1):
    link.append(namelink[i])
    link.append('%20')
  link.append(region[0])
  link.append('%23')
  link.append(region[1])
  reallink = ''.join(link)
  return reallink

def linkconstructhist(command):
  
  
def getimmage(link, bool):
  results = []
  response = requests.get(link)
  html = response.text
  soup = BeautifulSoup(html, 'html5lib')
  for element in soup.findAll(attrs = {'class' : 'rating-entry__rank-icon'}):
    results.append(element)
  if bool == 'rank':
    try:
      res = results[0]
    except:
      return '```User is private```'
  elif bool == 'peak':
    try: 
      res = results[1]
    except:
      return '```User is private```'
  textresult = str(res)
  
  
  imlink = (re.search("(?P<url>https?://[^\s]+)", textresult).group("url"))
  imagelink = imlink[:-9]
  return imagelink

def gethistory(link):
  pass

@client.event
async def on_ready():
  print ('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return
  if message.content.startswith('##tracker'):
    command = msg.split()
    direct = command[1].lower()

    if direct in command_list:
      
      if direct == 'help':
        await message.channel.send('``` history : Displays the player\'s match history \n rank : Displays the player\'s current rank \n peak : Displays the player\'s peak rank```')

      if direct == 'rank':
        img = getimmage(linkconstruct(command), 'rank')
        await message.channel.send(img)

      if direct == 'peak':
        img = getimmage(linkconstruct(command), 'peak')
        await message.channel.send(img)

    else:
      await message.channel.send('```Not a valid command, type \'##tracker help\' or veiw the bot description to see a list of commands.```')
    

client.run(os.environ['TOKEN'])