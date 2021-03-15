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

async def init_session(client,message,reply=None,**kwargs):
    if reply is None:
        reply = await message.channel.send("Loading featured collection...")
    session = FeaturedCollection(client,message,reply)
    await session.featured_collection_cover_flow()


class FeaturedCollection:

    def __init__(self,client,message,reply):
        self.client = client
        self.message = message
        if reply is not None:
            self.reply = reply 
        self.collection_data = {}


    async def featured_collection_cover_flow(self):
        if self.collection_data == {}:
            collection = await valapi.get_game_api('/valorant/v1/store-featured')
            bundle = collection['data']['FeaturedBundle']['Bundle']
            bundle_items = [i for i in bundle['Items']]
            bundle_overview = await valapi.get_content(f"/v1/bundles/{bundle['DataAssetID']}")
            self.collection_data = await content_utils.get_collection(bundle_items,bundle_overview['data'])
            self.collection_data['bundle'] = bundle
            self.collection_data['bundle_assets'] = bundle_overview['data']
            self.collection_data['bundle_assets']['highlightColor'] = content_utils.get_content_tier(self.collection_data['weapons'][0]['contentTierUuid'])['highlightColor']

        print(self.collection_data)

        embed,section_count = await content_embeds.build_featured_cover(self.collection_data)
        await self.reply.edit(content=self.message.author.mention,embed=embed)
        await self.reply.clear_reactions()

        reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
        reactions = reactions[0:section_count-1]
        
        option = await utils.wait_for_reactions(self.client,self.message,self.reply,reactions)
        if option != -2:
            await self.reply.clear_reactions()
            await self.reply.add_reaction("⏳")
            if option < len(self.collection_data['weapons']):
                payload = {
                    'weapon':self.collection_data['weapons'][option],
                    'bundle':content_utils.get_shop_item_from_id(self.collection_data['weapons'][option]['levels'][0]['uuid'],self.collection_data['bundle']),
                    'chromas':{
                        'index':0,
                        'max_index':len(self.collection_data['weapons'][option]['chromas'])-1
                    }
                }
                await self.weapon_skin_page_flow(payload,self.featured_collection_cover_flow)
            else:
                payload = {
                    'cards':self.collection_data['cards'],
                    'sprays':self.collection_data['sprays'],
                    'buddies':self.collection_data['buddies'],
                    'bundle_assets':self.collection_data['bundle_assets']
                }
                await self.flair_overview_flow(payload,self.featured_collection_cover_flow)
        else:
            await self.reply.clear_reactions()
            embed.set_footer(text="")
            await self.reply.edit(embed=embed)

    
    async def weapon_skin_page_flow(self,skin_data,back_callback):
        embed = await content_embeds.build_skin_overview(skin_data)
        await self.reply.edit(content=self.message.author.mention,embed=embed)
        await self.reply.clear_reactions()

        reactions = ["⬅️","➡️"] if skin_data['chromas']['max_index'] != 0 else []
        option = await utils.wait_for_reactions(self.client,self.message,self.reply,reactions,back_callback)
        if option != -2:
            await self.reply.clear_reactions()
            if option == 0 or option == 1:
                if option == 0:
                    skin_data['chromas']['index'] -= 1
                    if skin_data['chromas']['index'] < 0:
                        skin_data['chromas']['index'] = skin_data['chromas']['max_index']
                elif option == 1:
                    skin_data['chromas']['index'] += 1
                    if skin_data['chromas']['index'] > skin_data['chromas']['max_index']:
                        skin_data['chromas']['index'] = 0
                await self.weapon_skin_page_flow(skin_data,back_callback)

            elif option == -1:
                await self.reply.add_reaction("⏳")
                await back_callback()
        else:
            await self.reply.clear_reactions()
            embed.set_footer(text="")
            await self.reply.edit(embed=embed)


    '''
    async def flair_overview_flow(self,flair_data,back_callback):
        embed = await content_embeds.build_flair_overview(flair_data)
        await self.reply.edit(content=self.message.author.mention,embed=embed)
        await self.reply.clear_reactions()
    '''