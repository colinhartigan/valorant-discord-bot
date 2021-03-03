import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import utils, content_embeds
import iso8601
import match_flows

async def start_featured_collection_flow(client,message):
    reply = await message.channel.send("Loading featured collection...")

    collection_assets = await valapi.get_collection("3264e5b6-4bd2-213b-eeab-4d8525dd4ffb")
    
    for i in collection_assets:
        print(i["displayName"])


async def featured_collection_cover_flow(client,message,reply,assets,index):
    weapon = assets[index]
    #send image separate from embed