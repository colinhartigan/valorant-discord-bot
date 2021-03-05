from dotenv import load_dotenv
import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import utils
import iso8601
import match_flows, profile_flows, content_flows, tyrandon_flows

load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

@client.event
async def on_ready():  
    print("Ready!") 

@client.event
async def on_message(message):
    loop = asyncio.get_event_loop()
    split = message.content.split(" ")
    command = split[0]
    #print(split)
    if command.startswith("/latest"):
        await message.channel.trigger_typing()
        user = split[1].split("#")
        name = user[0]
        tag = user[1]
        task = loop.create_task(match_flows.latest_match_flow(client,name,tag,message))
        await task


    if command.startswith("/profile"):
        await message.channel.trigger_typing()
        user = split[1].split("#")
        name = user[0]
        tag = user[1]
        task = loop.create_task(profile_flows.profile_search_flow(client,name,tag,message))
        await task


    if command.startswith("/history"):
        await message.channel.trigger_typing()
        user = split[1].split("#")
        name = user[0]
        tag = user[1]
        task = loop.create_task(match_flows.match_history_flow(client,name,tag,message))
        await task

    if command.startswith("/mmr"):
        await message.channel.trigger_typing()
        user = split[1].split("#")
        name = user[0]
        tag = user[1]
        task = loop.create_task(profile_flows.mmr_search_flow(client,name,tag,message))
        await task

    if command.startswith("/tyrandons"):
        await message.channel.trigger_typing()
        task = loop.create_task(tyrandon_flows.show_tyrandons_flow(client,message))
        await task

    if command.startswith("/skins"):
        await message.channel.trigger_typing()
        task = loop.create_task(content_flows.start_featured_collection_flow(client,message))
        await task



client.run(TOKEN)