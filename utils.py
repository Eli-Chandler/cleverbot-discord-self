import requests
import json
from cleverbot import cleverbot
import time
import asyncio
import random
import re


token = ''

def get_context(channelID):
    url = f'https://discord.com/api/v9/channels/{channelID}/messages?limit=30'
    headers = {
        'authorization':token,
        'accept':'/',
        'authority':'discord.com',
        'content-type':'application/json'
    }

    r = requests.get(url, headers=headers)

    context = json.loads(r.content)
    context.reverse()
    return context

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def process_context(context):
    messages = []

    messageblock = []
    for message in context:
        if messageblock:
            if message['author']['id'] == messageblock[0]['author']['id']:
                messageblock.append(message)
            else:
                lst = []
                for m in messageblock:
                    lst.append(m['content'])
                messageblock = lst
                messages.append(messageblock)
                messageblock = [message]
        else:
            messageblock.append(message)

    lst = []
    for i in messageblock:
        lst.append(i['content'])
    messages.append(lst)

    lst = []
    for messageblock in messages:
        lst.append(', '.join(messageblock))
    messages = lst

    for i in range(len(messages)):
        messages[i] = deEmojify(messages[i])
    return messages




async def get_response(context):
    if context:
        if context[-1]['author']['id'] == '':
            print('self response')
            return
        messages = []
        for message in context:
            messages.append(message['content'])

        context = process_context(context)
        stimulus = context[-1]
        context.pop(-1)

        response = await cleverbot(stimulus, context)
        print('stimulus:', stimulus, 'response:', response)
        return response
