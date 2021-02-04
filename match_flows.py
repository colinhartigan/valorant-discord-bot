import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import assets, embeds
import iso8601
import profile_flows


# these bad boys go first



async def latest_match_flow(client,name,tag,message):
    reply = await message.channel.send("Searching for latest available match...")
    try:
        matches = await valapi.get_matches(name,tag)
        profile = await valapi.get_profile(name,tag)
    except api_exception as e:
        await reply.delete()
        embed = embeds.build_error_embed(e.data[0],e.data[1],e.data[2])
        await message.channel.send(message.author.mention,embed=embed)
        return
    latest = {}
    for i in matches['matches']:
        if i['isAvailable']:
            latest = i
            break
    await initial_player_summary_flow(client,latest,profile,message,reply)




# these bad boys are the menus
async def match_history_flow(client,name,tag,message,reply=None,back_callback=None,args=None):
    if reply == None:
        reply = await message.channel.send("Gathering matches...")
    try:
        profile = await valapi.get_profile(name,tag)
        matches = await valapi.get_matches(name,tag)
    except api_exception as e:
        await reply.delete()
        embed = embeds.build_error_embed(e.data[0],e.data[1],e.data[2])
        await message.channel.send(message.author.mention,embed=embed)
        return
    embed = embeds.build_recent_matches(matches,profile)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()

    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","🔙"]
    for i,v in enumerate(reactions):
        if i < 6:
            await reply.add_reaction(v)
        if not back_callback == None and i >= 6:
            await reply.add_reaction(v)
    def check(reaction,user):
        return user == message.author and str(reaction.emoji) in reactions and reaction.message == reply
    try:
        reaction,user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)

    else:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        option = reactions.index(str(reaction.emoji))
        if not option == 6:
            match = matches['matches'][option]
            await initial_player_summary_flow(client,match,profile,message,reply,match_history_flow,(client,name,tag,message,reply,back_callback,args))
        else:
            await back_callback(*args)






async def match_details_flow(client,matchid,message,reply,back_callback=None,args=None):
    match = await valapi.get_match(matchid)
    embed = embeds.build_match_summary(match)
    await reply.edit(embed=embed)
    await reply.clear_reactions()

    reactions = ["🟦","🟥","🔙"]
    for i,v in enumerate(reactions):
        if i < 2:
            await reply.add_reaction(v)
        if not back_callback == None and i >= 2:
            await reply.add_reaction(v)
    def check(reaction,user):
        return user == message.author and str(reaction.emoji) in reactions and reaction.message == reply
    try:
        reaction,user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await reply.clear_reactions()
        embed.description = ""
        await reply.edit(embed=embed)

    else:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        option = reactions.index(str(reaction.emoji))
        if not option == 2:
            if option == 0:
                await team_summary_flow(client,matchid,"blue",message,reply,match_details_flow,(client,matchid,message,reply,back_callback,args)) 
            else:
                await team_summary_flow(client,matchid,"red",message,reply,match_details_flow,(client,matchid,message,reply,back_callback,args))
        else: 
            await back_callback(*args)


async def team_summary_flow(client,matchid,team,message,reply,back_callback=None,args=None):
    match = await valapi.get_match(matchid)
    embed = embeds.build_team_summary(match,team,"red" if team == "blue" else "blue")
    await reply.edit(embed=embed)
    await reply.clear_reactions()

    team_roster = [i['user'] for i in match['data']['player']['byteam'][team]]

    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","🔙"]
    for i in reactions:
        await reply.add_reaction(i)
    def check(reaction,user):
        return user == message.author and str(reaction.emoji) in reactions and reaction.message == reply
    try:
        reaction,user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await reply.clear_reactions()
        embed.description = ""
        await reply.edit(embed=embed)

    else:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        option = reactions.index(str(reaction.emoji))
        if not option == 5:
            player = team_roster[option]
            player_dict = {}

            for i in match['data']['player']['byteam'][team]:
                if i['user'] == player:
                    player_dict = i

            await player_summary_flow(client,matchid,player_dict,team,message,reply,team_summary_flow,(client,matchid,team,message,reply,back_callback,args))
        else:
            await back_callback(*args)


async def player_summary_flow(client,matchid,player,team,message,reply,back_callback=None,args=None):
    match = await valapi.get_match(matchid)
    embed = embeds.build_player_details(match,player,team)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()

    user = player['user'].split("#")
    name = user[0]
    tag = user[1]

    has_profile = True 
    try:
        await valapi.get_profile(name,tag)
        has_profile = True
        embed.description = "React with ⬜ for player's profile"
        await reply.edit(embed=embed)
    except api_exception as e:
        has_profile = False

    reactions = ["⬜","🔙"]
    for i,v in enumerate(reactions):
        if i == 0 and has_profile:
            await reply.add_reaction(v)
        elif i == 1:
            await reply.add_reaction(v)
    def check(reaction,user):
        return user == message.author and str(reaction.emoji) in reactions and reaction.message == reply
    try:
        reaction,user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await reply.clear_reactions()
        embed.description = ""
        await reply.edit(embed=embed)

    else:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        option = reactions.index(str(reaction.emoji))
        if not option == 1:
            try:
                await profile_flows.profile_details_flow(client,name,tag,message,reply,player_summary_flow,(client,matchid,player,team,message,reply,back_callback,args))
            except api_exception as e:
                await player_summary_flow(client,matchid,player,team,message,reply,back_callback,args)
        else:
            await back_callback(*args)
        

async def initial_player_summary_flow(client,match,profile,message,reply,back_callback=None,args=None):
    full_match = await valapi.get_match(match['metadata']['gameid'])
    embed = embeds.build_personal_match_summary(match,full_match,profile)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()
    
    reactions = ["⬜","🔙"]
    for i,v in enumerate(reactions):
        if i < 1:
            await reply.add_reaction(v)
        if not back_callback == None and i >= 1:
            await reply.add_reaction(v)
    def check(reaction,user):
        return user == message.author and str(reaction.emoji) in reactions and reaction.message == reply
    try:
        reaction,user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)
    
    else:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        option = reactions.index(str(reaction.emoji))
        if not option == 1:
            await match_details_flow(client,match['metadata']['gameid'],message,reply,initial_player_summary_flow,(client,match,profile,message,reply,back_callback,args))
        else:
            await back_callback(*args)