#from random import randrange
import asyncio
import requests
import os
import discord
import time

#time.sleep(20)
while True:
    if True:
        #load_dotenv()
        token = 'XXX'
        client = discord.Client()
        
        @client.event
        async def on_ready():
            await client.change_presence(status=discord.Status.online, activity=discord.Game('pictortelescope.com'))
            print(f'{client.user.name} has connected to Discord!')
        
        observing = False
        @client.event
        async def on_message(message):
            global observing
            print(message.content)
            #if randrange(10) > 2:
            #    response = requests.get('https://pictortelescope.com/last_obs_duration.txt')
            #    if response.status_code == 200:
            #        exec(response.content)
            #        if int(time.time()) <= int(obs_time)+int(duration):
            #            observing = True
            #            client.change_presence(status=discord.Status.idle, activity=discord.Game('Observing...'))
            #        else:
            #            observing = False
            #            client.change_presence(status=discord.Status.online, activity=discord.Game('pictortelescope.com'))
            if message.author == client.user:
                return
            if 'restart_pictor' in message.content:
                os.system("sudo /bin/systemctl restart pictor.service")
                os.system("sudo /bin/systemctl restart disc_bot.service")
            if '639462705723605013>' in message.content and observing and 'observe' in message.content:
                await message.add_reaction('❌')
                await message.channel.send('The telescope is currently observing. Please wait until it\'s done before submitting your observation...')
                return
            elif '639462705723605013>' in message.content and observing:
                print(3)
                await message.channel.send('**PICTOR** is an open-source radio telescope that allows anyone to observe the radio sky using its convenient web platform for **free**! This bot allows you to submit observations directly from Discord. For more info, visit <https://www.pictortelescope.com> or ping <@!234246004424179712> for help!\n\n**Usage:**\n```@PICTOR observe <duration (in seconds)>```\n**Example:**\n```@PICTOR observe 60```\n**Default observation parameters:**\n```\nCenter frequency: 1420 MHz\nBandwidth: 2.4 MHz\nNumber of channels: 2048\nNumber of bins: 100```')
                return
            print(2)
            if not observing and '639462705723605013>' in message.content and len(message.content.split()) == 3 and message.content.split()[1].lower() == 'observe':
                if  message.content.split()[2].isdigit() and int(message.content.split()[2]) >= 10 and int(message.content.split()[2]) <= 600:
                    duration = message.content.split()[2]
                    try:
                        os.remove('/home/pi/Desktop/pictortelescope/observation.dat')
                        os.remove('/home/pi/Desktop/pictortelescope/plot.png')
                        os.remove('/home/pi/Desktop/pictortelescope/spectrum.csv')
                        os.remove('/home/pi/Desktop/pictortelescope/time_series.csv')
                    except OSError:
                        pass
                    await message.add_reaction('✅')
                    await message.channel.send('Observing for **'+duration+' seconds** with PICTOR. Please wait...')
                    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Observing...'))
                    observing = True
                    myobj = {'obs_name': 'discord_obs', 'f_center': '1420', 'bandwidth': '2.4mhz', 'channels': '2048', 'nbins': '100', 'duration': duration, 'email': 'coto_dup@hotmail.com', 'submit_btn': '1'}
                    requests.post('https://pictortelescope.com/observe.php', data = myobj)
                    try:
                        os.remove('/home/pi/Desktop/pictortelescope/observation.dat')
                        os.remove('/home/pi/Desktop/pictortelescope/plot.png')
                        print(8)
                    except OSError:
                        pass
                    
                    time.sleep(5)
                    while not os.path.exists('/home/pi/Desktop/pictortelescope/plot.png'):
                        print('doesnt exist')
                        await asyncio.sleep(1)
                    time.sleep(4)
                    print('out')
                    await message.channel.send('<@!'+str(message.author.id)+ '> **Your observation has been carried out by PICTOR successfully!**\nHere is your observation\'s data:', file=discord.File('/home/pi/Desktop/pictortelescope/plot.png'))
                    await client.change_presence(status=discord.Status.online, activity=discord.Game('pictortelescope.com'))
                    observing = False
                else:
                    await message.add_reaction('❌')
                    await message.channel.send('Please ensure the given observation duration is greater than 10 and less than 600 seconds.')
            
            elif '639462705723605013>' in message.content:
                await message.channel.send('**PICTOR** is an open-source radio telescope that allows anyone to observe the radio sky using its convenient web platform for **free**! This bot allows you to submit observations directly from Discord. For more info, visit <https://www.pictortelescope.com> or ping <@!234246004424179712> for help!\n\n**Usage:**\n```@PICTOR observe <duration (in seconds)>```\n**Example:**\n```@PICTOR observe 60```\n**Default observation parameters:**\n```\nCenter frequency: 1420 MHz\nBandwidth: 2.4 MHz\nNumber of channels: 2048\nNumber of bins: 100```')
        client.run(token)
    #except Exception as e:
    #    print(e)
    #    time.sleep(10)
    #    os.system("sudo /bin/systemctl restart disc_bot.service")
