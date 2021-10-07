import discord
import requests
import json
import random
import pandas as pd

bot = discord.Client()

# Dad's replies to your yes/no question 
conch_words = [
  'Have you tried asking your mom?',
  'Is the Pope Catholic?',
  'Have you tried google?',
  'Whatever makes you happy kid',
  'Ask me later, the neighbors dog pooped on our lawn again',
  'If you can do it for free, why not?',
  'Nah, probably not',
  'Just make sure you dont get caught',
  'I dont tell you how to live your life',
  'No, your mom would get mad if I let you do that',
  'Sure, just bring some back for me',
  'Go ahead, but dont tell your mother :shushing_face:',
  'Sure, only if you can find me some headlight fluid first',
  'Sure, knock yourself out',
  'Yes.'
]

#Lists the word in which Dad will scold you
with open('badwords.txt', 'r') as f:
  bad_words = [line.strip() for line in f]
  bad_words = set(bad_words)
  f.close()
  
pronouns = [
  'im',
  'i am',
  "i'm"
]

#scraping a random joke from an API
def make_joke():
  url = "https://icanhazdadjoke.com/"
  headers = {'Accept':'application/json'}
  req = requests.get(url, headers=headers)
  file = req.json()
  return(file['joke'])

#WORK IN PROGRESS will return a GIF whenever a User
# mentions another user with the pat command
#def anime_pats():
  #apikey = gif_token
  #lmt = 8
  #search_term = "anime patting"

  # get random results using default locale of EN_US
  #r = requests.get(
      #"https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
  #if r.status_code == 200:
      #gifs = json.loads(r.content)
      #msg = gifs[random.randint(0, 12)]
      #return(msg)
  #else:
      #gifs = None

#need to make a textfile that can store a dictionary
# name: count of bad words
# dad bot needs to be able to read the file, and store it on a dictionary
# Anytime someone curses, he can check the dictionary of the author of the messge
# and see the counter tied to it. Then he can tell them how many times they have cursed.


#on startup
@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
  try: 
    bad_word_data = json.load("data.json")
  except FileNotFoundError:
    print("Data file not found.")
    bad_word_data = {} 

#whenever a message is sent
@bot.event
async def on_message(message):
  msg_author = f'{message.author.name}#{message.author.discriminator}'
  if message.author == bot.user:
    return
  #if message.author.id == 'Pupper#1652':
    #if message.content
  #will return a dad joke when 'dad joke' is detected
  if 'dad' in message.content.lower() and 'joke' in message.content.lower():
    joke = make_joke()
    await message.channel.send(joke)
    return
  # Dad will reply to the user's new identity
  for pronoun in pronouns:
    if len(message.content) > 80:
      return
    if message.content.lower().startswith(pronoun):
      msg = message.content.lower().replace('im', '',1)
      msg = msg.lower().replace("i'm",'',1)
      msg = msg.lower().replace('i am', '',1)
      msg = msg.lower().replace('@','')
      await message.channel.send('Hello'+ msg + ", I'm Dad!")
      return
  #tells the user that a bad word has been detected 
  for badword in bad_words:
    if badword in message.content.lower():
      if(msg_author in bad_word_data.keys()):
        bad_word_data[msg_author]["badWords"] += 1
      else:
        bad_word_data[msg_author] = 1

      await message.channel.send(f'Uh oh, {message.author.mention} said a bad word!')
      return
  #This will detect whether a user wants to ask dad a question
  # to which Dad will reply something from his conch_list
  if message.content.lower().startswith('hey dad') and not message.content == 'hey dad' and not message.content == 'hey dad ':
    msg = conch_words[random.randint(0, 14)]
    await message.channel.send(msg)
    return

  #bully kazu and argo kekw
  #done by richard
  if(msg_author == "NJV#6329" or msg_author == "Gooby#5933"):
    emotes = ['<:loser:845866953797009408>', '<:pepeStare:753282276871241839>', 
    '<:SIMP:753122463365464124>', '<:WeirdChamp:753114155942150224>']
    #every time they msg, have a 8% chance of emoting
    roll = random.random()
    print(roll)
    if(roll > .93):
      await message.channel.send(emotes[random.randint(0, len(emotes)-1)]) 
      await message.channel.send(message.author.mention)
    return
    #need something to further troll kazu
    
  #Dad will say hi to the user
  if ('hey' in message.content or 'hi' in message.content or 'hello' in message.content) and 'dad' in message.content:
    await message.channel.send(f'Hello {message.author.mention}!')
    return

  #if '!pat' in message.content:
   # print('yup')
    #patted = message.content.replace('!pat',"")
    #await message.channel.send(f'{message.author.mention} pats{patted}')
    #await message.channel.send(anime_pats())

#implement pat command

bot.run()
