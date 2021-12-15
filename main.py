import discord
from discord import client
from discord.ext import commands
import utils
import asyncio
import time

client = commands.Bot(command_prefix = '!', self_bot = True)

channels = []
blocked_words = ['<html><body>denied</body></html>', '<html>']

@client.event
async def on_ready():
    print('Ready')

task_list = []

@client.event
async def on_message(message):
    if message.author.id == 740787859509870692:
        return

    if message.channel in task_list:
        return


    if message.guild == None or message.channel.id in channels:
        while True:
            try:
                await reply(message)
                break
            except:
                await asyncio.sleep(15)
                continue


async def reply(message):
    task_list.append(message.channel)
    while True:
        await asyncio.sleep(15)
        context = utils.get_context(message.channel.id)
        context[-1]['content'] = context[-1]['content'].replace(',', '').replace("'", '').replace('"', '')
        response = await utils.get_response(context)

        if response == None:
            continue

        response = response.replace('.', '').replace("'", '').replace(',', '').lower()




        try:
            for word in blocked_words:
                if word in response:
                    print('Blocked word', response)
                    response = None
                    time.sleep(60)
        except:
            response = None
                
        if response:
            await message.channel.send(response)
            task_list.pop(task_list.index(message.channel))
            return
            
        
        

client.run('')
