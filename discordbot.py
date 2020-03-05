import random
import string
import discord
from datetime import datetime

def randomStringDigits(stringLength=6):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def newBot(token, connection, mysql):
    client = discord.Client()

    def getPrefix():
        return "{0} [VEEN]".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

    async def sendVerification(member):
        print('{0} Created verification for {1.name}'.format(getPrefix(), member))
        dm_channel = member.dm_channel
        if dm_channel == None:
            dm_channel = await member.create_dm()

        random_string = randomStringDigits(12)
        await dm_channel.send("Heya, **{1}**!\n\nTof dat je ervoor kiest om onze discord te joinen!\nOm toegang te krijgen tot alle kanalen zul je eerst moeten inloggen via onze site. \n\n**Zorg ervoor dat je deze link met __NIEMAND__ deelt**\nhttps://veenstad.com/verificatie?key={0}".format(random_string, member.name))

    @client.event
    async def on_ready():
        print('{0} Bot is now ready and running!'.format(getPrefix()))
        await client.change_presence(activity=discord.Activity(name="with myself", type=0))

    @client.event
    async def on_member_join(member):
        await sendVerification(member)

    @client.event
    async def on_message(message):
        actualMessage = message.content
        args = actualMessage.split()
        channel = message.channel
        member = message.author
        if message.channel.type == discord.ChannelType.private:
            return
        if actualMessage.lower().startswith('!verificatie'):
            await sendVerification(member)
            return
        if actualMessage.lower().startswith("!removecommand"):
            if len(args) == 2:
                command = args[1]
                connection.execute('SELECT response FROM commands WHERE command = %s', (command,))
                result = connection.fetchone()
                if result != None:
                    connection.execute('DELETE FROM commands WHERE command = %s', (command,))
                    mysql.commit()
                    await channel.send("Removed command!")
                else:
                    await channel.send("Could not find that command!")
            else:
                await channel.send("Right usage: !removecommand [command]")
        if actualMessage.lower().startswith("!editcommand"):
            if len(args) >=3:
                command = args[1]
                connection.execute('SELECT response FROM commands WHERE command = %s', (command,))
                result = connection.fetchone()
                if result != None:
                    response = " ".join(args[2:])
                    connection.execute('UPDATE commands SET response = %s WHERE command = %s', (response, command))
                    mysql.commit()
                    await channel.send("Changed command!")
                else:
                    await channel.send("Could not find that command!")
            else:
                await channel.send("Right usage: !addcommand [command] [response]")
            return
        if actualMessage.lower().startswith("!addcommand"):
            if len(args) >=3:
                command = args[1]
                connection.execute('SELECT response FROM commands WHERE command = %s', (command,))
                result = connection.fetchone()
                if result == None:
                    response = " ".join(args[2:])
                    connection.execute('INSERT INTO commands (command, response) VALUES (%s, %s)', (command, response))
                    mysql.commit()
                    await channel.send("Added command!")
                else:
                    await channel.send("This command already exists!")
            else:
                await channel.send("Right usage: !addcommand [command] [response]")
            return
        if actualMessage.startswith('!'):
            command = args[0].replace('!', '')
            connection.execute('SELECT response FROM commands WHERE command = %s', (command,))
            result = connection.fetchone()
            mysql.commit()
            if result != None:
                await message.channel.send(result[0])
            return

            


    client.run(token)