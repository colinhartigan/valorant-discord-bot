import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import content_utils, content_embeds, utils
import iso8601

async def start_featured_collection_flow(client,message):
    reply = await message.channel.send("Loading featured collection...")

    collection = await valapi.get_game_api('/valorant/v1/store-featured')
    bundle = collection['data']['FeaturedBundle']['Bundle']
    bundle_items = [i for i in bundle['Items']]
    bundle_overview = await valapi.get_content(f"/v1/bundles/{bundle['DataAssetID']}")
    collection_assets = await content_utils.get_collection(bundle_items,bundle_overview['data'])

    collection_assets['bundle'] = bundle
    collection_assets['bundle_assets'] = bundle_overview['data']

    #print(collection_assets)

    embed,section_count = await content_embeds.build_featured_cover(collection_assets)
    await reply.edit(content=message.author.mention,embed=embed)

    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    reactions = reactions[0:section_count]
    
    option = await utils.wait_for_reactions(client,message,reply,reactions)
    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)


async def featured_collection_cover_flow(client,message,reply,assets,index):
    weapon = assets[index]
    #send image separate from embed