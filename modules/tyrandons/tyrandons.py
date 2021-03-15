import valapi
from valapi import api_exception
import discord 
import asyncio
import utils 
import modules.tyrandons.tyrandon_embeds as tyrandon_embeds

async def show_tyrandons_flow(client,message,reply=None):
    if reply is None:
        reply = await message.channel.send("Gathering tyrandons...")
    else:
        await reply.edit(content="Gathering tyrandons...",embed=None)
        await reply.clear_reactions()

    tyrandons = []
    gathered = 0

    async def incriment_gathered():
        nonlocal gathered
        gathered += 1
        await reply.edit(content=f"Gathering tyrandons... ({gathered}/10)")

    async def get_tyrandon(num):
        nonlocal gathered,tyrandons
        timeout_counter = 0
        mmr = {'status':'500'}
        while (mmr['status'] == '500' or mmr['status'] == '501'):
            if timeout_counter > 5:
                break
            try:
                mmr = await valapi.get_mmr(f'tyrandon{num}',utils.get_tyrandon_tag(num))
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
            timeout_counter += 1
            await asyncio.sleep(1)

        await incriment_gathered()
        tyrandons.append((num,mmr))


    await asyncio.gather(get_tyrandon(0),get_tyrandon(1),get_tyrandon(2),get_tyrandon(3),get_tyrandon(4),get_tyrandon(5),get_tyrandon(6),get_tyrandon(7),get_tyrandon(8),get_tyrandon(9))
    tyrandons = sorted(tyrandons,key=lambda i: i[0])
    
    embed = await tyrandon_embeds.build_tyrandons(tyrandons)
    await reply.edit(content=message.author.mention,embed=embed)

    #uncomment once mmr history and stuff is fixed
    '''
    reactions = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

    option = await utils.wait_for_reactions(client,message,reply,reactions)
    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if option != -1:
            tyrandon = tyrandons[option]
            #load competitive info
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)
    '''