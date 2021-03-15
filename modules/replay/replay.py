import asyncio
import aiohttp
import valapi
import modules.replay.replay_embeds as replay_embeds
import modules.replay.replay_utils as replay_utils
import time 
import json

async def init_replay(client,message,reply=None,**kwargs):
    if reply is None:
        reply = await message.channel.send("Loading match...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.henrikdev.xyz/valorant/v2/match/{kwargs['match_id']}") as data:
            match = await data.json()
            replay = Replay(client,reply,match)
            await session.close()
            await replay.run_replay()
 

class Replay:
    def __init__(self,client,reply,match):
        #print(match)
        self.client = client
        self.reply = reply
        self.channel = reply.channel
        self.match = match
        self.metadata = match['data']['metadata']
        self.players = match['data']['players']
        self.teams = match['data']['teams']
        self.rounds = match['data']['rounds']



    async def run_replay(self):
        await self.reply.delete()
        self.reply_1 = await self.channel.send("...")
        self.reply_2 = await self.channel.send("...") 
        #self.reply_3 = await self.channel.send("...")

        

        for id,match_round in enumerate(self.rounds):
            match_round['round_id'] = id+1
            #print(match_round)
            match_round = await self.clean_round(match_round)
            timeline = await self.build_round_timeline(match_round)
            payload = {
                'round_data':match_round,
                'timeline':timeline
            }
            await self.round_replay(payload)
            await asyncio.sleep(5)
        #make a separate reply for round metadata, red team, blue team embeds
        #reply with most recent kill data (hits/dmg per bullet)
        #have running event log for each round





    async def round_replay(self,data):
        round_data = data['round_data']
        timeline = data['timeline']
        overview_embed = await replay_embeds.build_round_overview(round_data)
        timeline_embed = await replay_embeds.build_timeline(data)

        await self.reply_1.edit(content='',embed=overview_embed)
        await self.reply_2.edit(content='',embed=timeline_embed)
 
        for i in timeline:
            pass



    async def clean_round(self,match_round):
        match_round = await self.convert_items(match_round) #convert ms times to s
        match_round['end_type_converted'] = replay_utils.convert_result(match_round['end_type'])

        return match_round


    async def convert_items(self,data):
        #somehow strip the name here
        def check(item):
            for k in list(item):
                if 'time' in k.lower():
                    if item[k] is not None:
                        item[k] = time.strftime("%M:%S", time.gmtime(round(item[k]/1000)))
                if 'team' in k.lower():
                    if item[k] is not None:
                        item[f'{k}_patched'] = replay_utils.get_team_name(self.metadata['mode'],data['round_id'],item[k])
                if 'display_name' in k.lower():
                    if type(item[k]) is str:
                        item[f'{k}_patched'] = replay_utils.strip_tag(item[k])
                elif type(item[k]) is list:
                    for j in item[k]:
                        if type(j) is dict:
                            check(j)
                elif type(item[k]) is dict:
                    check(item[k])
        check(data)
        return data


    async def build_round_timeline(self,round_data):
        timeline = {
            'events':[],
            'round_id':round_data['round_id']
        }

        # build round timeline
        for player in round_data['player_stats']:
            for event in player['kill_events']:
                event['type'] = 'kill'
                event['time_in_round'] = event['kill_time_in_round']
                if not "Ability" in event['damage_weapon_id'] and not "Ultimate" in event['damage_weapon_id']:
                    try:
                        weapon = await valapi.get_content(f"/v1/weapons/{event['damage_weapon_id']}")
                        event['weapon_name'] = weapon['data']['displayName']
                        event['weapon_icon'] = weapon['data']['killStreamIcon']
                    except:
                        event['weapon_name'] = '?'
                        event['weapon_icon'] = 'https://media.valorant-api.com/weapons/9c82e19d-4575-0200-1a81-3eacf00cf872/killstreamicon.png'
                timeline['events'].append(event) 
        
        if round_data['bomb_planted']:
            round_data['plant_events']['type'] = 'plant'
            round_data['plant_events']['time_in_round'] = round_data['plant_events']['plant_time_in_round']
            timeline['events'].append(round_data['plant_events'])
            if round_data['bomb_defused']:
                round_data['defuse_events']['type'] = 'defuse'
                round_data['defuse_events']['time_in_round'] = round_data['defuse_events']['defuse_time_in_round']
                timeline['events'].append(round_data['defuse_events'])
        #print(timeline)
        timeline['events'] = sorted(timeline['events'], key=lambda i: get_sec(i['time_in_round'])) # sort timeline

        return timeline

def get_sec(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)