import valapi
from valapi import api_exception
import discord 
import asyncio
import utils, embeds

async def show_tyrandons_flow(client,message):
    reply = await message.channel.send("Gathering tyrandons...")

    tyrandons = []

    for i in range(1,10):
        tyrandons.append(valapi.get_mmr(f'tyrandon{i}','NA1'))