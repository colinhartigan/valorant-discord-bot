from dotenv import load_dotenv
import os
import datetime
import valapi,clientapi
from valapi import api_exception
import discord 
import asyncio
import utils
import iso8601

# module imports
import modules.replay.replay as replay
import modules.skins.featured_collection as featured_collection
import modules.tyrandons.tyrandons as tyrandons

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
    '''
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
    '''

    if command.startswith("/tyrandons"):
        await message.channel.trigger_typing()
        task = loop.create_task(tyrandons.show_tyrandons_flow(client,message))
        await task

    if command.startswith("/skins"):
        await message.channel.trigger_typing()
        task = loop.create_task(featured_collection.featured_collection_cover_flow(client,message))
        await task

    if command.startswith("/replay"):
        await message.channel.trigger_typing()
        task = loop.create_task(replay.init_replay(client,message,match_id='c704de7f-d9ba-466c-a3fd-8765111a1ba5'))
        await task

    if command.startswith("/test"):
        await message.channel.trigger_typing()
        task = loop.create_task(clientapi.get_matches('eaa0d224-61bc-593a-a083-d6e18161e4c5'))
        await task


if __name__ == '__main__':
    client.run(TOKEN)