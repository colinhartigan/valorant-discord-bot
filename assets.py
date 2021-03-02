agent_icons = {
    'Jett':'https://titles.trackercdn.com/valorant-api/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png',
    'Raze':'https://titles.trackercdn.com/valorant-api/agents/f94c3b30-42be-e959-889c-5aa313dba261/displayicon.png',
    'Reyna':'https://titles.trackercdn.com/valorant-api/agents/a3bfb853-43b2-7238-a4f1-ad90e9e46bcc/displayicon.png',
    'Brimstone':'https://titles.trackercdn.com/valorant-api/agents/9f0d8ba9-4140-b941-57d3-a7ad57c6b417/displayicon.png',
    'Breach':'https://titles.trackercdn.com/valorant-api/agents/5f8d3a7f-467b-97f3-062c-13acf203c006/displayicon.png',
    'Viper':'https://titles.trackercdn.com/valorant-api/agents/707eab51-4836-f488-046a-cda6bf494859/displayicon.png',
    'Sage':'https://titles.trackercdn.com/valorant-api/agents/569fdd95-4d10-43ab-ca70-79becc718b46/displayicon.png',
    'Phoenix':'https://titles.trackercdn.com/valorant-api/agents/eb93336a-449b-9c1b-0a54-a891f7921d69/displayicon.png',
    'Sova':'https://titles.trackercdn.com/valorant-api/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/displayicon.png',
    'Killjoy':'https://titles.trackercdn.com/valorant-api/agents/1e58de9c-4950-5125-93e9-a0aee9f98746/displayicon.png',
    'Yoru':'https://titles.trackercdn.com/valorant-api/agents/7f94d92c-4234-0a36-9646-3a87eb8b5c89/displayicon.png',
    'Omen':'https://titles.trackercdn.com/valorant-api/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png',
    'Cypher':'https://titles.trackercdn.com/valorant-api/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png',
    'Skye':'https://titles.trackercdn.com/valorant-api/agents/6f2a04ca-43e0-be17-7f36-b3908627744d/displayicon.png',
}

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

def get_icon(agent):
    return agent_icons[agent]

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