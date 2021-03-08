import valapi
import json
import discord
import asyncio

rank_colors = { 0: 0x2f3136, 3: 0x333333, 4: 0x333333, 5: 0x333333, 6: 0x68450d, 7: 0x68450d, 8: 0x68450d, 9: 0xe5ece8, 10: 0xe5ece8, 11: 0xe5ece8, 12:0xde9421, 13:0xde9421, 14:0xde9421, 15:0x3ca9ba, 16:0x3ca9ba, 17:0x3ca9ba, 18:0xf197f4, 19:0xf197f4, 20:0xf197f4, 21:0xb02639, 24:0xf2db99, }

rank_ids = { 'Unrated':0, 'Iron 1':3, 'Iron 2':4, 'Iron 3':5, 'Bronze 1':6, 'Bronze 2':7, 'Bronze 3':8, 'Silver 1':9, 'Silver 2':10, 'Silver 3':11, 'Gold 1':12, 'Gold 2':13, 'Gold 3':14, 'Platinum 1':15, 'Platinum 2':16, 'Platinum 3':17, 'Diamond 1':18, 'Diamond 2':19, 'Diamond 3':20, 'Immortal':23, 'Radiant':24, }

# ------------------------------------------------------------------------------------------
# content utilities
def fetch_config():
    with open('config.json') as fil:
        return json.load(fil)

async def get_agent_icon(agent):
    agents = await valapi.get_content('/v1/agents')
    for i in agents['data']:
        if i['displayName'] == agent:
            return i['displayIcon']

def get_ranked_icon(rank):
    return f'https://trackercdn.com/cdn/tracker.gg/valorant/icons/tiers/{rank}.png'

def get_rank_color(rank_id):
    return rank_colors[rank_id]

def shorten_rank(rank):
    return f'{rank[0]}{rank[-1]}'

def get_rank_id(rank):
    return rank_ids[rank]

def get_default_card():
    return "https://media.valorant-api.com/playercards/e6a07a97-4c48-421f-515e-288379f7a5be/smallart.png"

def get_tyrandon_tag(num):
    return ('NA1' if not num == 0 else '1549') #only tyrandon0 has a tag: 1549
# ------------------------------------------------------------------------------------------


async def build_error_embed(code,msg,note):
    embed = discord.Embed(
        title=str(code),
        description=msg,
        color=0xff6b6b,
    )
    embed.set_footer(text=note)
    return embed


async def wait_for_reactions(client,message,reply,reactions,back_callback=None):
    # returns -2 on TimeoutError
    # returns -1 for back_callback
    for i in reactions:
        if not i == "":
            await reply.add_reaction(i) 
    if back_callback is not None:
        reactions.append("🔙")
        await reply.add_reaction("🔙")
    

    # local utility functions
    async def check_reactions(reactions):
        for i in reactions:
            users = await i.users().flatten()
            for user in users:
                if check(i,user):
                    return return_selection(i)
        return None

    def check(reaction,user):
        return user == message.author and str(reaction.emoji) in reactions and reaction.message == reply

    def return_selection(reaction):
        ind = reactions.index(str(reaction.emoji))
        if ind == len(reactions) - 1 and back_callback:
            return -1
        else:
            return ind


    #check to see if any reactions were added while the bot was initializing them
    await asyncio.sleep(.2)
    cache_rep = discord.utils.get(client.cached_messages, id=reply.id) 
    early_react = await check_reactions(cache_rep.reactions)
    
    if early_react is None:
        try:
            reaction,user = await client.wait_for('reaction_add', timeout=45.0, check=check)
        except asyncio.TimeoutError:
            return -2
        else:
            return return_selection(reaction)
    else:
        return early_react