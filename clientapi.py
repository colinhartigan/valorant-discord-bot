import re
import aiohttp
import asyncio
import json
import os


async def client_get(username,password,endpoint):
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

    async with session.get(f'https://pd.na.a.pvp.net{endpoint}', headers=headers) as r:
        final_data = json.loads(await r.text())

    await session.close()

    return final_data

async def get_matches(uuid):
    matches = await client_get(os.environ.get('USER'), os.environ.get('PASS'),f'/match-history/v1/history/{uuid}?startIndex=0&endIndex=10')
    print(matches)
    return matches