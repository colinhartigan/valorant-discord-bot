import requests
import asyncio

base = 'https://api.henrikdev.xyz'


class api_exception(BaseException):
    def __init__(self,data):
        self.data = data 


async def get_profile(name,tag):
    try:
        data = requests.get(f'{base}/valorant/v1/profile/{name}/{tag}')
        print(data)
        profile = data.json() 
        print(profile)
        if profile['status'] == '200':
            return profile
        elif profile['status'] != '200':
            raise api_exception([profile['status'],profile['message'],'Make sure friend requests are enabled and your account is linked on https://tracker.gg/valorant!'])
    except Exception as e:
        raise api_exception(["404","Something went wrong... try again",""])


async def get_matches(name,tag):
    try:
        data = requests.get(f'{base}/valorant/v1/matches/{name}/{tag}')
        matches = data.json()
        if matches["status"] == "200":
            return matches
        elif matches['status'] != '200':
            raise api_exception([matches['status'],matches['message'],'Make sure friend requests are enabled and your account is linked on https://tracker.gg/valorant!'])
    except:
        raise api_exception(["404","Something went wrong... try again",""])

async def get_match(gameid):
    try:
        data = requests.get(f'{base}/valorant/v1/match/{gameid}')
        match = data.json()
        if match['metadata']['gameid'] == gameid:
            return match
        else:
            raise api_exception([match['status'],match['message'],'Invalid match ID'])
    except:
        raise api_exception(["404","Something went wrong... try again",""])

async def get_mmr(name,tag):
    try:
        data = requests.get(f'{base}/valorant/v1/mmr/NA/{name}/{tag}')
        mmr = data.json()
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
    except:
        mmr = {
            "status":"200",
            "data":{
                "currenttier":0,
                "currenttierpatched":"Unrated",
                "ranking_in_tier":0,
                "mmr_change_to_last_game":0,
                "elo":0
            }
        }
        return mmr