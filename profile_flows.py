import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import utils, embeds
import iso8601
import match_flows


async def profile_search_flow(client,name,tag,message):
    reply = await message.channel.send("Searching for profile...")
    try:
        profile = await valapi.get_profile(name,tag)
    except api_exception as e:
        await reply.delete()
        embed = await embeds.build_error_embed(e.data[0],e.data[1],e.data[2])
        await message.channel.send(message.author.mention,embed=embed)
        return
    
    await profile_details_flow(client,name,tag,message,reply)


async def profile_details_flow(client,name,tag,message,reply,back_callback=None,args=None):
    mmr = await valapi.get_mmr(name,tag)
    profile = await valapi.get_profile(name,tag)
    embed = await embeds.build_profile_details(profile,mmr)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()

    reactions = ["🏅","🏆","🔙"]
    for i,v in enumerate(reactions):
        if i < 2:
            await reply.add_reaction(v)
        if not back_callback == None and i >= 2:
            await reply.add_reaction(v)
    def check(reaction,user):
        return user == message.author and str(reaction.emoji) in reactions and reaction.message == reply
    
    #TODO: USE utils.CHECK_REACTION THINGY TO CHECK IF REACTION IS ALREADY ON BEFORE GOING TO CLIENT.WAIT_FOR
    cache_rep = discord.utils.get(client.cached_messages, id=reply.id)
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
        if not option == 2:
            if option == 1:
                await match_flows.match_history_flow(client,name,tag,message,reply,profile_details_flow,(client,name,tag,message,reply,back_callback,args))
        else:
            await back_callback(*args)