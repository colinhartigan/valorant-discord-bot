import re
import aiohttp
import asyncio
import json
import os


async def auth(username,password):
    session = aiohttp.ClientSession() 
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    #print(data)
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]
    #print('Access Token: ' + access_token)
    id_token = data[1]
    expires_in = data[2]

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    #print('Entitlements Token: ' + entitlements_token)

    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    #print('User ID: ' + user_id)
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    await session.close()
    return user_id, headers


async def get_auth(user, passw):
    loop = asyncio.get_event_loop()
    user_id,headers = await auth(user, passw)
    return user_id,headers

async def get_glz(endpoint,headers):
    session = aiohttp.ClientSession()
    async with session.get(f'https://glz-na-1.na.a.pvp.net{endpoint}', headers=headers) as r:
        data = json.loads(await r.text())
        await session.close()
    return data

async def get_pd(endpoint,headers):
    session = aiohttp.ClientSession()
    async with session.get(f'https://pd.na.a.pvp.net{endpoint}', headers=headers) as r:
        data = json.loads(await r.text())
        await session.close()
    return data

async def post_glz(endpoint,headers):
    session = aiohttp.ClientSession()
    async with session.post(f'https://glz-na-1.na.a.pvp.net{endpoint}', headers=headers) as r:
        data = json.loads(await r.text())
        await session.close()
    return data



async def get_matches(id):
    uuid,headers = await get_auth(os.environ.get('USER'), os.environ.get('PASS'))

    #match = await get_glz(f'/session/v1/sessions/{uuid}',headers)
    #matches = await get_glz('/match-history/v1/history/eaa0d224-61bc-593a-a083-d6e18161e4c5?startIndex=0&endIndex=10',headers)
    #print(matches)
    match = await get_glz(f'/core-game/v1/matches/{id}',headers)
    print(f"{match}\n")
    match1 = await get_pd(f'/match-details/v1/matches/{id}',headers)
    print(match1)
    with open('match_response_reference.json','w') as file:
        json.dump(match,file)
    #print(matches)