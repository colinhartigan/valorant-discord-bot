import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import utils, embeds
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
        embed = await embeds.build_error_embed(e.data[0],e.data[1],e.data[2])
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
        embed = await embeds.build_error_embed(e.data[0],e.data[1],e.data[2])
        await message.channel.send(message.author.mention,embed=embed)
        return
    embed = await embeds.build_recent_matches(matches,profile)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()

    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]
    option = await utils.wait_for_reactions(client,message,reply,embed,reactions,back_callback)

    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if not option == -1:
            match = matches['matches'][option]
            await initial_player_summary_flow(client,match,profile,message,reply,match_history_flow,(client,name,tag,message,reply,back_callback,args))
        else:
            await back_callback(*args)
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)





async def match_details_flow(client,matchid,message,reply,back_callback=None,args=None):
    match = await valapi.get_match(matchid)
    embed = await embeds.build_match_summary(match)
    await reply.edit(embed=embed)
    await reply.clear_reactions()

    reactions = ["🟦","🟥"]
    option = await utils.wait_for_reactions(client,message,reply,embed,reactions,back_callback)        

    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if not option == 2:
            if option == 0:
                await team_summary_flow(client,matchid,"blue",message,reply,match_details_flow,(client,matchid,message,reply,back_callback,args)) 
            else:
                await team_summary_flow(client,matchid,"red",message,reply,match_details_flow,(client,matchid,message,reply,back_callback,args))
        else: 
            await back_callback(*args)
    else:
        await reply.clear_reactions()
        embed.description = ""
        await reply.edit(embed=embed)



async def team_summary_flow(client,matchid,team,message,reply,back_callback=None,args=None):
    match = await valapi.get_match(matchid)
    embed = await embeds.build_team_summary(match,team,"red" if team == "blue" else "blue")
    await reply.edit(embed=embed)
    await reply.clear_reactions()

    team_roster = [i['user'] for i in match['data']['player']['byteam'][team]]

    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
    option = await utils.wait_for_reactions(client,message,reply,embed,reactions,back_callback)  

    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if not option == 5:
            player = team_roster[option]
            player_dict = {}

            for i in match['data']['player']['byteam'][team]:
                if i['user'] == player:
                    player_dict = i

            await player_summary_flow(client,matchid,player_dict,team,message,reply,team_summary_flow,(client,matchid,team,message,reply,back_callback,args))
        else:
            await back_callback(*args)
    else:
        await reply.clear_reactions()
        embed.description = ""
        await reply.edit(embed=embed)



async def player_summary_flow(client,matchid,player,team,message,reply,back_callback=None,args=None):
    match = await valapi.get_match(matchid)
    embed = await embeds.build_player_details(match,player,team)
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
    option = await utils.wait_for_reactions(client,message,reply,embed,reactions,back_callback)  
        
    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if not option == 1:
            try:
                await profile_flows.profile_details_flow(client,name,tag,message,reply,player_summary_flow,(client,matchid,player,team,message,reply,back_callback,args))
            except api_exception as e:
                await player_summary_flow(client,matchid,player,team,message,reply,back_callback,args)
        else:
            await back_callback(*args)
    else:
        await reply.clear_reactions()
        embed.description = ""
        await reply.edit(embed=embed)
        


async def initial_player_summary_flow(client,match,profile,message,reply,back_callback=None,args=None):
    full_match = await valapi.get_match(match['metadata']['gameid'])
    embed = await embeds.build_personal_match_summary(match,full_match,profile)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()
    
    reactions = ["⬜","🔙"]
    option = await utils.wait_for_reactions(client,message,reply,embed,reactions,back_callback)     
    
    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if not option == 1:
            await match_details_flow(client,match['metadata']['gameid'],message,reply,initial_player_summary_flow,(client,match,profile,message,reply,back_callback,args))
        else:
            await back_callback(*args)
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)