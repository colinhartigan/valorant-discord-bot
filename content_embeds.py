import discord
import iso8601
import content_utils
import asyncio
import datetime

async def build_featured_cover(data):
    embed = discord.Embed(
        title=data['bundle_assets']['displayName'],
        description="/".join(i['displayName'].replace(data['bundle_assets']['displayName'],"").strip(' ').upper() for i in data['weapons']),
        color=content_utils.get_content_tier(data['weapons'][0]['contentTierUuid'])['highlightColor']
    ) 
    embed.set_image(url=data['bundle_assets']['displayIcon'])

    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    emoji_index = 0

    for skin in data['weapons']:
        try:
            shop_data = content_utils.get_shop_item_from_id(skin['levels'][0]['uuid'],data['bundle'])
            embed.add_field(
                name=f"{emojis[emoji_index]} {skin['displayName']} **[{shop_data['BasePrice']}{content_utils.get_currency_type(shop_data['CurrencyID'])['displayNameSingular']}]**",
                value=f"{len(skin['levels'])} level"+("s" if len(skin['levels']) > 1 else "")+f"\n{len(skin['chromas'])} chroma"+("s" if len(skin['chromas']) > 1 else ""),
            )
            emoji_index += 1
        except Exception as e:
            print(e)
            continue
    
    embed.add_field(
        name=f"{emojis[emoji_index]} Flair",
        value=f"{', '.join((i['displayName']) for i in data['buddies'])}\n{', '.join(i['displayName'] for i in data['cards'])}\n{', '.join(i['displayName'] for i in data['sprays'])}"
    )


    return embed, emoji_index+1