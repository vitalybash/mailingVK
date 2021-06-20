import asyncio
import aiohttp
import random
import requests
import time
from settings import string, TOKEN

ID = []

# with open('message.txt', mode='r', encoding='utf8'):


async def main():
    params = {'access_token': TOKEN,
              'v': '5.103'}
    async with aiohttp.ClientSession() as session:
        usersCount = (await (await session.get(
            'https://api.vk.com/method/messages.getConversations',
            params=params)).json())['response']['count']
    offset = 0
    while offset <= usersCount:
        get_conversation(offset)
        offset += 100

    tasks = [asyncio.create_task(send_message(entities)) for entities in ID]
    time1 = time.time()
    await asyncio.gather(*tasks)
    print(time.time() - time1)


async def send_message(entities: list, message=string):
    params = {'access_token': TOKEN,
              'v': '5.103',
              'user_ids': ','.join([str(x) for x in entities]),
              'random_id': str(random.randint(0, 2 ** 64)),
              'attachment': 'wall-149574746_89835',
              'message': message}

    async with aiohttp.ClientSession() as session:
        await session.post('https://api.vk.com/method/messages.send',
                           params=params)


def get_conversation(offset=0):
    params = {'access_token': TOKEN,
              'v': '5.103',
              'offset': offset,
              'count': 100}
    response = requests.get('https://api.vk.com/method/messages.getConversations',
                            params=params).json()
    waitID = []
    print(offset)
    for item in response['response']['items']:
        waitID.append(item['conversation']['peer']['id'])
    ID.append(waitID)


asyncio.run(main())
