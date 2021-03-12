import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import modules.skins.content_utils as content_utils
import modules.skins.content_embeds as content_embeds
import utils
import iso8601

async def featured_collection_cover_flow(client,message,reply=None):
    if reply is None:
        reply = await message.channel.send("Loading featured collection...")

    collection = await valapi.get_game_api('/valorant/v1/store-featured')
    bundle = collection['data']['FeaturedBundle']['Bundle']
    bundle_items = [i for i in bundle['Items']]
    bundle_overview = await valapi.get_content(f"/v1/bundles/{bundle['DataAssetID']}")
    data = await content_utils.get_collection(bundle_items,bundle_overview['data'])

    data['bundle'] = bundle
    data['bundle_assets'] = bundle_overview['data']

    #print(data)

    embed,section_count = await content_embeds.build_featured_cover(data)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()

    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    reactions = reactions[0:section_count]
    
    option = await utils.wait_for_reactions(client,message,reply,reactions)
    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if option < len(data['weapons']):
            payload = {
                'weapon':data['weapons'][option],
                'bundle':content_utils.get_shop_item_from_id(data['weapons'][option]['levels'][0]['uuid'],data['bundle']),
                'chromas':{
                    'index':0,
                    'max_index':len(data['weapons'][option]['chromas'])-1
                }
            }
            #print(payload)
            await weapon_skin_page_flow(client,message,reply,payload,featured_collection_cover_flow,(client,message,reply))
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)


async def weapon_skin_page_flow(client,message,reply,data,back_callback=None,args=None):
    embed = await content_embeds.build_skin_overview(data)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()

    reactions = ["⬅️","➡️"] if data['chromas']['max_index'] != 0 else []
    option = await utils.wait_for_reactions(client,message,reply,reactions,back_callback)
    if option != -2:
        await reply.clear_reactions()
        if option == 0 or option == 1:
            if option == 0:
                data['chromas']['index'] -= 1
                if data['chromas']['index'] < 0:
                    data['chromas']['index'] = data['chromas']['max_index']
            elif option == 1:
                data['chromas']['index'] += 1
                if data['chromas']['index'] > data['chromas']['max_index']:
                    data['chromas']['index'] = 0
            await weapon_skin_page_flow(client,message,reply,data,back_callback,args)

        elif option == -1:
            await reply.add_reaction("⏳")
            await back_callback(*args)
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)