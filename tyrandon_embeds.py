import discord
import iso8601
import utils
import asyncio
import datetime

async def build_tyrandons(tyrandons):
    embed = discord.Embed(
        title="Tyrandons",
        description="",
        color=0xfa4454
    )
    embed.set_footer(text="react with a number to see more comp info")

    for i in tyrandons:
        embed.add_field(
            name=f'tyrandon{i[0]}{" "*10}',
            #what lies below is my least favorite line of code ive ever written
            value=f"**{i[2]['stats']['rank']}**"+(f" **({utils.shorten_rank(i[1]['data']['currenttierpatched'])})**" if i[2]['stats']['rank'] == "Unrated" else "")+"\n"+(f"{i[1]['data']['ranking_in_tier']}/100\n" if i[1]['status'] != '500' else "???\n")+((("+" if i[1]['data']['mmr_change_to_last_game'] > 0 else "")+(f"{i[1]['data']['mmr_change_to_last_game']}RR")) if i[1]['status'] != '500' else ""),
        )

    return embed
