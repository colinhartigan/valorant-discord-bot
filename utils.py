import valapi

rank_colors = {
    0: 0x2f3136,
    3: 0x333333,
    4: 0x333333,
    5: 0x333333,
    6: 0x68450d,
    7: 0x68450d,
    8: 0x68450d,
    9: 0xe5ece8,
    10: 0xe5ece8,
    11: 0xe5ece8,
    12:0xde9421,
    13:0xde9421,
    14:0xde9421,
    15:0x3ca9ba,
    16:0x3ca9ba,
    17:0x3ca9ba,
    18:0xf197f4,
    19:0xf197f4,
    20:0xf197f4,
    21:0xb02639,
    24:0xf2db99,
}

rank_ids = {
    'Unrated':0,
    'Iron 1':3,
    'Iron 2':4,
    'Iron 3':5,
    'Bronze 1':6,
    'Bronze 2':7,
    'Bronze 3':8,
    'Silver 1':9,
    'Silver 2':10,
    'Silver 3':11,
    'Gold 1':12,
    'Gold 2':13,
    'Gold 3':14,
    'Platinum 1':15,
    'Platinum 2':16,
    'Platinum 3':17,
    'Diamond 1':18,
    'Diamond 2':19,
    'Diamond 3':20,
    'Immortal':23,
    'Radiant':24,
}

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

def check_cached_reactions(msg,user):
    pass