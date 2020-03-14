import os
import random
import string
import discord
from discord.utils import get
from datetime import datetime
from py_dotenv import read_dotenv

def randomStringDigits(stringLength=6):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def newBot(token, connection, mysql, activation_channel, domain):
    client = discord.Client()

    def getPrefix():
        return "{0} [VEEN]".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

    async def sendVerification(member, channel=None):
        dm_channel = member.dm_channel
        if dm_channel == None:
            dm_channel = await member.create_dm()
        connection.execute('SELECT activation_id FROM activation WHERE discord_id = %s', (member.id,))
        result = connection.fetchone()
        mysql.commit()
        if result == None:
            print('{0} Created verification for {1.name}'.format(getPrefix(), member))
            random_string = randomStringDigits(12)
            try:
                await dm_channel.send("Heya, **{1}**!\n\nTof dat je ervoor kiest om onze discord te joinen!\nOm toegang te krijgen tot alle kanalen zul je eerst moeten inloggen via onze site. \n\n**Zorg ervoor dat je deze link met __NIEMAND__ deelt**\n{2}{0}".format(random_string, member.name, domain))
                connection.execute('INSERT INTO activation (activation_id, discord_id, discord_name) VALUES (%s, %s, %s)', (random_string, member.id, member.name))
                mysql.commit()
            except Exception:
                if channel != None:
                    await channel.send('Het is helaas niet mogelijk om een prive bericht naar jou te sturen! Je zult dit aan moeten zetten om jezelf te kunnen verifiëren.')
        else:
            try:
                print('{0} Resend verification for {1.name}'.format(getPrefix(), member))
                random_string = result[0]
                await dm_channel.send("Heya, **{1}**!\n\nTof dat je ervoor kiest om onze discord te joinen!\nOm toegang te krijgen tot alle kanalen zul je eerst moeten inloggen via onze site. \n\n**Zorg ervoor dat je deze link met __NIEMAND__ deelt**\n{2}{0}".format(random_string, member.name, domain))
            except Exception:
                if channel != None:
                    await channel.send('Het is helaas niet mogelijk om een prive bericht naar jou te sturen! Je zult dit aan moeten zetten om jezelf te kunnen verifiëren.')    
    @client.event
    async def on_ready():
        print('{0} Bot is now ready and running!'.format(getPrefix()))
        await client.change_presence(activity=discord.Activity(name=".verificatie.", type=discord.ActivityType.listening))

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