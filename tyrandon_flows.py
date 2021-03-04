import valapi
from valapi import api_exception
import discord 
import asyncio
import utils, tyrandon_embeds
import profile_flows

async def show_tyrandons_flow(client,message,reply=None,tyrandons=None):
    if reply is None:
        reply = await message.channel.send("Gathering tyrandons...")
    
    if tyrandons is not None:
        await asyncio.sleep(.5)

    if tyrandons is None:
        tyrandons = []
        gathered = 0

        async def incriment_gathered():
            nonlocal gathered
            gathered += 1
            await reply.edit(content=f"Gathering tyrandons... ({gathered}/10)")

        async def get_tyrandon(num):
            nonlocal gathered
            timeout_counter = 0
            mmr = {'status':'500'}
            profile = {'status':'500'}
            while (mmr['status'] == '500' or profile['status'] == '500') or (mmr['status'] == '501' or profile['status'] == '501'):
                if timeout_counter > 5:
                    tyrandons.append((num,mmr,profile))
                    break
                try:
                    mmr = await valapi.get_mmr(f'tyrandon{num}',utils.get_tyrandon_tag(num))
                    profile = await valapi.get_profile(f'tyrandon{num}',utils.get_tyrandon_tag(num))
                except api_exception as e:
                    print(e)
                    mmr = {
                        'status': '500',
                        'data': {
                            'currenttier': -1,
                            'currenttierpatched': 'unable to access rank',
                            'ranking_in_tier': 0,
                            'mmr_change_to_last_game': 0,
                            'elo': 0
                        }
                    }
                    profile = {
                        'stats':{
                            'rank':'unable to access rank'
                        }
                    }
                timeout_counter += 1
                await asyncio.sleep(1)

            await incriment_gathered()
            tyrandons.append((num,mmr,profile))
            

        await asyncio.gather(get_tyrandon(0),get_tyrandon(1),get_tyrandon(2),get_tyrandon(3),get_tyrandon(4),get_tyrandon(5),get_tyrandon(6),get_tyrandon(7),get_tyrandon(8),get_tyrandon(9))
        tyrandons = sorted(tyrandons,key=lambda i: i[0])
    
    embed = await tyrandon_embeds.build_tyrandons(tyrandons)
    await reply.edit(content="",embed=embed)

    reactions = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

    option = await utils.wait_for_reactions(client,message,reply,reactions)
    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if option != -1:
            tyrandon = tyrandons[option]
            await profile_flows.competitive_info_flow(client,f"tyrandon{option}",utils.get_tyrandon_tag(option),message,reply,show_tyrandons_flow,(client,message,reply,tyrandons))
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)