import discord
import asyncio
import random
import os

global banlist #Setting up the ban list.
banlist = []
for x in open('banlist.dat', 'r+'): #Calls the file, if it's not there it will create it.
    if x == "":
        pass
    elif x == None:
        pass
    else:
        x = x.replace("\n", "")
        banlist.append(x)

global restricted_chats #Setting up the restricted chats list.
restricted_chats = []
for x in open('restrictedchats.dat', 'r+'): #Calls the file, if it's not there it will create it.
    if x == "":
        pass
    elif x == None:
        pass
    else:
        x = x.replace("\n", "")
        restricted_chats.append(x)
        
global jokes #Setting up the restricted chats list.
jokes = []
for x in open('jokes.dat', 'r+'): #Calls the file, if it's not there it will create it.
    x = x.replace("\n", "")
    if x == "":
        pass
    elif x == None:
        pass
    else:
        jokes.append(x)

def main_check(check): #Defines a command to check if the message requires a comment or not.
    check = check.lower()
    triggers = ["i'm", "im", "i am"]
    if check.startswith(tuple(triggers)):
        return True
    else:
        return False

def shortener(text):
    text = text.lower()
    if text.startswith("i am"):
        text = text.replace("i am", "", 1)
    elif text.startswith("i'm"):
        text = text.replace("i'm", "", 1)
    elif text.startswith("im"):
        text = text.replace("im", "", 1)
    return text

client = discord.Client() #Setting up general info.

@client.event            #Setting up the bot.
async def on_ready():
    os.system('cls')
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-----")

@client.event    #Awaiting commands
async def on_message(message):
    content = message.content
    if message.author.id in banlist: #Checks for ban list status
        if content.startswith("-dadbot:unrestrict:user"):
            await client.send_message(message.channel, "You are about to unrestrict yourself from using DadBot! Type ```-yes``` to confirm.")
            reply = await client.wait_for_message(author=message.author, timeout=30)
            reply = reply.content
            reply = reply.lower()
            if reply == "-yes":
                await client.send_message(message.channel, "You have unrestricted yourself from using DadBot! To undo this, type ```-dadbot:restrict:user```")
                f = open("banlist.dat", "r")
                lines = f.readlines()
                f.close()
                f = open("banlist.dat", "w")
                for x in lines:
                    if x != "\n" + message.author.id:
                        f.write(x)
                f.close()
                banlist.remove(message.author.id)
            else:
                await client.send_message(message.channel, 'Action canceled.')

        elif content.startswith("-dad"):
            await client.send_message(message.author, "You're currently restricted from using the bot! Please use ```-dadbot:unrestrict:user``` to unrestrict yourself!")
        else:
            pass
    else:
        if message.channel.id in restricted_chats: #Checks for chat status
            if content.startswith("-dadbot:unrestrict:chat"):
                if message.author.server_permissions.administrator == True:
                    await client.send_message(message.channel, "You are about to unrestrict this channel from using DadBot! Type ```-yes``` to confirm.")
                    reply = await client.wait_for_message(author=message.author, timeout=30)
                    id = reply.channel.id
                    reply = reply.content
                    reply = reply.lower()
                    if reply == "-yes":
                        await client.send_message(message.channel, "You have unrestricted this channel from using DadBot! To undo this, type ```-dadbot:restrict:chat```")
                        f = open("restrictedchats.dat", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("restrictedchats.dat", "w")
                        for x in lines:
                            if x !=  message.channel.id + "\n":
                                f.write(x)
                        f.close()
                        restricted_chats.remove(message.channel.id)
                    else:
                        await client.send_message(message.channel, 'Action canceled.')
                else:
                    await client.send_message(message.author, "I'm sorry, you do not have the correct permissions to preform this command!")
            elif content.startswith("-dad"):
                await client.send_message(message.author, "This chat is currently restricted! Please contact an admin if you think this isn't right, or if you're an admin refer to the manual!")
            else:
                pass
        else:
            if main_check(content) == True: #Checks to see if the message requires a comment
                if len(content) > 100:
                    content = "spammer"
                content = shortener(content)
                await client.send_message(message.channel, "Hi" + content + ", I'm dad.")
            else:
                if content.startswith("-dad"):
                    if content.startswith("-dadbot"):
                        if content.startswith("-dadbot:restrict:user"):
                            await client.send_message(message.channel, "You are about to restrict yourself from using DadBot! Type ```-yes``` to confirm.")
                            reply = await client.wait_for_message(author=message.author, timeout=30)
                            reply = reply.content
                            reply = reply.lower()
                            if reply == "-yes":
                                await client.send_message(message.channel, "You have restricted yourself from using DadBot! To undo this, type ```-dadbot:unrestricted:user```")
                                f = open("banlist.dat", "a")
                                f.write("\n" + message.author.id)
                                f.close()
                                banlist.append(message.author.id)
                            else:
                                await client.send_message(message.channel, 'Action canceled.')
                                
                        elif content.startswith("-dadbot:restrict:chat"):
                            if message.author.server_permissions.administrator == True:
                                await client.send_message(message.channel, "You are about to restrict this chat from using DadBot! Type ```-yes``` to confirm.")
                                reply = await client.wait_for_message(author=message.author, timeout=30)
                                reply = reply.content
                                reply = reply.lower()
                                if reply == "-yes":
                                    await client.send_message(message.channel, "You have restricted this chat from using DadBot! To undo this, type ```-dadbot:unrestrict:chat```")
                                    f = open("restrictedchats.dat", "a")
                                    f.write("\n" + message.channel.id)
                                    f.close()
                                    restricted_chats.append(message.channel.id)
                                else:
                                    await client.send_message(message.channel, 'Action canceled.')
                            else:
                                await client.send_message(message.author, "I'm sorry, you do not have the correct permissions to preform this command!")
                    elif content.startswith("-dadjoke"):
                        await client.send_message(message.channel, random.choice(jokes))
                else:
                    pass

client.run('')
