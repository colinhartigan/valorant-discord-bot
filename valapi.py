import requests
import asyncio
import aiohttp
import utils

game_base = 'https://api.henrikdev.xyz'
content_base = 'https://valorant-api.com'


class api_exception(BaseException):
    def __init__(self,data):
        self.data = data 

# game apis
async def get_match(gameid):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v2/match/{gameid}') as data:
                match = await data.json()
                if match['metadata']['gameid'] == gameid:
                    return match
                else:
                    raise api_exception([match['status'],match['message'],'Invalid match ID'])
    except Exception as e:
        raise api_exception(["404",e,"try again /shrug"])


async def get_mmr(name,tag):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v1/mmr/NA/{name}/{tag}') as data:
                mmr = await data.json()
                if mmr["status"] == "200":
                    return mmr
                elif mmr['status'] == "500":
                    mmr = {
                        "status":"500",
                        "data":{
                            "currenttier":-1,
                            "currenttierpatched":"Unable to access rank, make sure friend requests are enabled!",
                            "ranking_in_tier":0,
                            "mmr_change_to_last_game":0,
                            "elo":0
                        }
                    } 
                    return mmr
                else:
                    raise api_exception([mmr['status'],mmr['data']['message'],'Make sure friend requests are enabled and your account is linked on https://tracker.gg/valorant!'])
    except Exception as e:
        mmr = {
            "status":"501", #501 status = not able to fetch MMR
            "data":{
                "currenttier":0,
                "currenttierpatched":"Unrated",
                "ranking_in_tier":0,
                "mmr_change_to_last_game":0,
                "elo":0
            }
        }
        return mmr

async def get_mmr_history(name,tag):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v1/mmr-history/na/{name}/{tag}') as data:
                mmr = await data.json()
                if mmr['status'] == "200":
                    return mmr
                elif mmr['status'] == "500":
                    mmr = {
                        "status":"501", #501 status = not able to fetch MMR
                        "data":"unable to fetch MMR data"
                    }
                    return mmr
        return mmr
    except Exception as e:
        mmr = {
            "status":"501", #501 status = not able to fetch MMR
            "data":"unable to fetch MMR data"
        }
        return mmr

async def get_uuid_from_name(name,tag):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v1/puuid/{name}/{tag}') as data:
                data = await data.json()
                if data['status'] == "200":
                    return data['data']['puuid']
    except Exception as e:
        data = {
            "status":"501", #501 status = not able to fetch MMR
            "data":"unable to fetch"
        }
        return data


# template for other less-used game apis
async def get_game_api(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.get(game_base+endpoint) as data:
            payload = await data.json()
            return payload


# content apis
async def get_content(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.get(content_base+endpoint) as data:
            payload = await data.json()
            return payload