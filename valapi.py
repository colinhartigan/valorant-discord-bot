import requests
import asyncio
import aiohttp

game_base = 'https://api.henrikdev.xyz'
content_base = 'https://valorant-api.com'


class api_exception(BaseException):
    def __init__(self,data):
        self.data = data 

# game apis
async def get_profile(name,tag):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v1/profile/{name}/{tag}') as data:
                profile = await data.json() 
                if profile['status'] == '200':
                    return profile
                elif profile['status'] != '200':
                    raise api_exception([profile['status'],profile['message'],'Make sure friend requests are enabled and your account is linked on https://tracker.gg/valorant!'])
    except Exception as e:
        raise api_exception(["404","Something went wrong... try again",""])

async def get_matches(name,tag):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v1/matches/{name}/{tag}') as data:
                matches = await data.json()
                print(matches)
                if matches["status"] == "200":
                    return matches
                elif matches['status'] != '200':
                    raise api_exception([matches['status'],matches['message'],'Make sure friend requests are enabled and your account is linked on https://tracker.gg/valorant!'])
    except:
        raise api_exception(["404","Something went wrong... try again",""])

async def get_match(gameid):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v1/match/{gameid}') as data:
                match = await data.json()
                if match['metadata']['gameid'] == gameid:
                    return match
                else:
                    raise api_exception([match['status'],match['message'],'Invalid match ID'])
    except:
        raise api_exception(["404","Something went wrong... try again",""])

async def get_mmr(name,tag):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{game_base}/valorant/v1/mmr/NA/{name}/{tag}') as data:
                mmr = await data.json()
                print(f"mmr: {mmr}")
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
        print(e)
        mmr = {
            "status":"501",
            "data":{
                "currenttier":0,
                "currenttierpatched":"Unrated",
                "ranking_in_tier":0,
                "mmr_change_to_last_game":0,
                "elo":0
            }
        }
        return mmr


# content apis
async def get_content(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.get(content_base+endpoint) as data:
            payload = await data.json()
            return payload
