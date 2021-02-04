import discord
import iso8601
import assets
import valapi
import asyncio


def build_error_embed(code,msg,note):
    embed = discord.Embed(
        title=str(code),
        description=f"**API says:** '{msg}'",
        color=0xff6b6b,
    )
    embed.set_footer(text=note)
    return embed


def build_recent_matches(matches,profile):
    numbers = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
    user = matches['user']

    embed = discord.Embed(
        title="Recent Matches",
        description="",
        color=0x5cee49 if matches['matches'][0]['metadata']['playerhaswon'] else 0xee4949,
    )
    embed.set_author(name=user,icon_url=profile['stats']['playercard'])
    for i,v in enumerate(matches['matches']):
        if i >= 6:
            break
        if v['isAvailable']:
            metadata = v['metadata']
            gamedata = v['game']
            embed.add_field(
                name=f"{numbers[i]} {metadata['modename']} [{gamedata['roundswon']}-{gamedata['roundslost']}]",
                value=f"**KDA**: {gamedata['kda']['kda']}\n**Agent**: {metadata['agentplayed']}\n**Map**: {metadata['map']}",
                inline=True,
            )
        else:
            embed.add_field(
                name="Match Unavailable",
                value="",
                inline=True
            )
    return embed



def build_profile_details(profile,mmr):
    stats = profile['stats']
    mmr_data = mmr['data']

    if mmr_data['currenttier'] == -1:
        mmr_data['currenttier'] = assets.get_rank_id(stats['rank'])

    embed = discord.Embed(
        title="Player Profile",
        description=(f"{stats['rank']}") + (f" ({mmr_data['ranking_in_tier']}/100)" if mmr['status'] != "500" else ""),
        color=assets.get_rank_color(mmr_data['currenttier'])
    )

    #change desc for immortal+
    if mmr_data['currenttier'] >= 21:
        embed.description = f"{stats['rank']}" + (f" ({mmr_data['elo']} elo)" if mmr['status'] != "500" else "")


    embed.set_author(name=profile['user'],icon_url=stats['playercard'])
    embed.set_thumbnail(url=assets.get_ranked_icon(mmr_data['currenttier']))
    embed.set_footer(text="*ACES/CLUTCHES/FLAWLESS COUNTS MIGHT BE WRONG*\nReact with 🏅 to see competitive info\nReact with 🏆 to see recent matches")
    embed.add_field(
        name="KDA",
        value=f"{stats['kills']}/{stats['deaths']}/{stats['assists']} ({stats['kdratio']})",
        inline=True,
    )
    embed.add_field(
        name="Total Headshots",
        value=f"{stats['headshots']} ({stats['headshotpercentage']}%)",
        inline=True,
    )
    embed.add_field(
        name="Wins",
        value=stats['wins'],
        inline=True,
    )
    embed.add_field(
        name="Playtime",
        value=stats['playtime']['playtimepatched'],
        inline=True,
    )
    embed.add_field(
        name="Matches Played",
        value=stats['matches'],
        inline=True,
    )
    embed.add_field(
        name="Aces",
        value=stats['aces'],
        inline=True,
    )
    embed.add_field(
        name="Clutches",
        value=stats['clutches'],
        inline=True,
    )
    embed.add_field(
        name="Flawless",
        value=stats['flawless'],
        inline=True,
    )
    return embed
    


def build_player_details(match,player,team):
    metadata = match['metadata']

    embed = discord.Embed(
        title="Player Details",
        description="",
        timestamp=iso8601.parse_date(metadata['timestamp']),
        color=0xee4949 if team == "red" else 0x53b9f9,
    )
    embed.set_author(name=player['user'],icon_url=assets.get_icon(player['agentused']))
    embed.set_footer(text=f"{metadata['modename']} on {metadata['map']} as {player['agentused']}")
    embed.add_field(
        name="KDA",
        value=f"{player['kda']['kda']} ({player['kda']['kdratio']})",
        inline=True
    )
    embed.add_field(
        name="Avg. Combat Score",
        value=player['scoreaverage'],
        inline=True
    )
    embed.add_field(
        name="Kills per Round",
        value=player['killsperround'],
        inline=True
    )
    embed.add_field(
        name="Damage Dealt",
        value=player['damage'],
        inline=True
    )
    
    if player['multiplekills']['triple'] > 0:
        embed.add_field(
            name="Triple Kills",
            value=player['multiplekills']['triple']
        )
    if player['multiplekills']['quadra'] > 0:
        embed.add_field(
            name="Quadra Kills",
            value=player['multiplekills']['quadra']
        )
    if player['multiplekills']['penta'] > 0:
        embed.add_field(
            name="Penta Kills",
            value=player['multiplekills']['penta']
        )
    
    return embed



def build_team_summary(match,team,otherteam):
    #team = "blue" or "red"/attackers or defenders
    metadata = match['metadata']
    team_meta = match['data']['teams'][team]
    team_data = match['data']['player']['byteam'][team]

    team_roster = [(i['user'],i['agentused'],assets.shorten_rank(i['rank'])) for i in team_data]
    mvp = ("",0)
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]

    for i in team_data: 
        if int(i['scoreaverage']) > int(mvp[1]):
            mvp = (i['user'],i['scoreaverage'])

    embed = discord.Embed(
        title=("Defenders" if team == "red" else "Attackers") + (f" [{team_meta['roundswon']}-{match['data']['teams'][otherteam]['roundswon']}]"),
        description="React with a player's number for more player data",
        color=0xee4949 if team == "red" else 0x53b9f9,
        timestamp=iso8601.parse_date(metadata['timestamp'])
    )
    embed.set_thumbnail(url=metadata['modeimage'])
    embed.set_footer(text=f"{metadata['modename']} on {metadata['map']}")
    embed.add_field(
        name="Team MVP (Avg. Combat Score)",
        value=f"{mvp[0]} ({mvp[1]})",
        inline=True
    )
    embed.add_field(
        name="Team KDA",
        value=f"{team_meta['teamkills']}/{team_meta['teamdeaths']}/{team_meta['teamassists']}",
        inline=True,
    )
    embed.add_field(
        name="Team Damage Dealt",
        value=f"{team_meta['teamdamage']}",
        inline=True
    )
    embed.add_field( 
        name="Roster",
        value="\n".join(f'{emojis[i]} **[{v[2]}]** {v[0]} ({v[1]})' for i,v in enumerate(team_roster)) if metadata['modename'] == "Competitive" else "\n".join(f'{emojis[i]} {v[0]} ({v[1]})' for i,v in enumerate(team_roster)),
        inline=False,
    )

    return embed



def build_match_summary(match):
    metadata = match['metadata']
    teamsdata = match['data']['teams']
    blue_meta = teamsdata['blue']
    red_meta = teamsdata['red']

    blue_team = match['data']['player']['byteam']['blue']
    red_team = match['data']['player']['byteam']['red']

    blue_roster = []
    red_roster = []

    for i in blue_team:
        blue_roster.append((i['user'],i['agentused'],assets.shorten_rank(i['rank'])))
    for i in red_team:
        red_roster.append((i['user'],i['agentused'],assets.shorten_rank(i['rank'])))

    embed = discord.Embed(
        title=("🟥 Defenders Won" if red_meta['haswon'] else "🟦 Attackers Won") + (f" [{blue_meta['roundswon']}-{red_meta['roundswon']}]" if blue_meta['haswon'] else f" [{red_meta['roundswon']}-{blue_meta['roundswon']}]"),
        description="React with a team's color for more team details",
        color=0xee4949 if red_meta['haswon'] else 0x53b9f9,
        timestamp=iso8601.parse_date(metadata['timestamp'])
    )
    embed.set_footer(text=f"{metadata['modename']} on {metadata['map']}")
    embed.set_thumbnail(url=metadata['modeimage'])
    embed.add_field(
        name="🟦 Attackers",
        value="\n".join(f'**[{i[2]}]** {i[0]} ({i[1]})' for i in blue_roster) if metadata['modename'] == "Competitive" else "\n".join(f'{i[0]} ({i[1]})' for i in blue_roster),
        inline=False,
    )
    embed.add_field(
        name="🟥 Defenders",
        value="\n".join(f'**[{i[2]}]** {i[0]} ({i[1]})' for i in red_roster) if metadata['modename'] == "Competitive" else "\n".join(f'{i[0]} ({i[1]})' for i in red_roster),
        inline=False,
    )
    return embed



def build_personal_match_summary(match,full_match,profile):
    gamedata = match['game']
    metadata = match['metadata']
    player_match_data = {}

    for _,i in full_match['data']['player']['byteam'].items():
        for j in i:
            if j['user'] == profile['user']:
                player_match_data = j

    embed = discord.Embed(
        title=f"Match Summary [{gamedata['roundswon']}-{gamedata['roundslost']}]",
        description='React with ⬜ to view more match data',
        color=0x5cee49 if metadata['playerhaswon'] else 0xee4949,
        timestamp=iso8601.parse_date(metadata['timestamp'])
    )
    embed.set_author(name=profile['user'],icon_url=assets.get_icon(metadata['agentplayed']))
    embed.set_thumbnail(url=full_match['metadata']['modeimage'])
    embed.set_footer(text=f"{metadata['modename']} on {metadata['map']} as {metadata['agentplayed']}")

    embed.add_field(
        name="KDA",
        value=gamedata['kda']['kda'],
        inline=False
    )
    embed.add_field(
        name="Avg. Combat Score", 
        value=player_match_data['scoreaverage'], 
        inline=False
    )
    embed.add_field(
        name="Headshot Percentage", 
        value=f"{gamedata['headshotspercentage']}%",
        inline=False
    )
    embed.add_field(
        name="Econ Rating", 
        value=gamedata['econrating'], 
        inline=False
    )
    return embed