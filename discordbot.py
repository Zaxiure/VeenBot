import os
import random
import string
import discord
from discord.utils import get
from datetime import datetime
from py_dotenv import read_dotenv
import requests

def randomStringDigits(stringLength=6):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def newBot(token, activation_channel, domain, api):
    client = discord.Client()

    def getPrefix():
        return "{0} [VEEN]".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

    async def sendVerification(member, channel=None):
        dm_channel = member.dm_channel
        if dm_channel == None:
            dm_channel = await member.create_dm()
        
        response = requests.get(url = api + str(member.id) + "/" + member.name)
        data = response.json()
        try:
            await dm_channel.send(data["message"])
            print('{0} Send verification to {1.name}'.format(getPrefix(), member))
        except Exception:
            if channel != None:
                await channel.send('Het is helaas niet mogelijk om een prive bericht naar jou te sturen! Je zult dit aan moeten zetten om jezelf te kunnen verifiëren.')
                print('{0} Unable to send verification to {1.name}'.format(getPrefix(), member))
    @client.event
    async def on_ready():
        print('{0} Bot is now ready and running!'.format(getPrefix()))
        await client.change_presence(activity=discord.Activity(name=".zvxiure.", type=discord.ActivityType.listening))

    @client.event
    async def on_member_join(member):
        await sendVerification(member)

    @client.event
    async def on_message(message):
        actualMessage = message.content
        args = actualMessage.split()
        channel = message.channel
        member = message.author

        if channel.id == int(activation_channel):
            if len(message.mentions) == 1:
                role = get(message.guild.roles, name='Bewoner')
                await message.mentions[0].add_roles(role)
                print('{0} Discord user {1} has been verified!'.format(getPrefix(), message.mentions[0].name))
        if message.channel.type == discord.ChannelType.private:
            return
        if actualMessage.lower().startswith('!verificatie'):
            await sendVerification(member, channel)
            return
            
    client.run(token)