import discord
import iso8601
import modules.skins.content_utils as content_utils
import asyncio
import datetime

async def build_featured_cover(data):
    embed = discord.Embed(
        title=f"Collection - {data['bundle_assets']['displayName']}",
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
        #name=f"{emojis[emoji_index]} Flair (dont choose this one)",
        name="Flair",
        value=f"{', '.join((i['displayName']) for i in data['buddies'])}\n{', '.join(i['displayName'] for i in data['cards'])}\n{', '.join(i['displayName'] for i in data['sprays'])}"
    ) 

    return embed, emoji_index+1


async def build_skin_overview(data):
    tier = content_utils.get_content_tier(data['weapon']['contentTierUuid'])
    upgrade_levels = []
    chromas = []
    for i,v in enumerate(data['weapon']['levels']):
        if v['levelItem'] is not None:
            upgrade_levels.append((i+1," "+v['levelItem'].replace('EEquippableSkinLevelItem::','')))
        else:
            upgrade_levels.append((i+1,"Base"))

    for i,v in enumerate(data['weapon']['chromas']):
        if v['displayName'] != data['weapon']['displayName']:
            chromas.append(v['displayName'][v['displayName'].find('\n'):].strip().strip('()'))
        else:
            chromas.append("Base")

    embed = discord.Embed(
        title="",
        description=f"Price: **{data['bundle']['BasePrice']}{content_utils.get_currency_type(data['bundle']['CurrencyID'])['displayNameSingular']}**",
        color=tier['highlightColor']
    )
    embed.set_image(url=data['weapon']['chromas'][data['chromas']['index']]['fullRender'])
    embed.set_author(name=data['weapon']['displayName'],icon_url=tier['displayIcon'])
    embed.set_footer(text="Use the arrow reactions to select chroma" if data['chromas']['max_index'] != 0 else "")

    embed.add_field(
        name="Upgrades",
        value="\n".join(f"Level {i[0]}: {i[1]}" for i in upgrade_levels),
        inline=True
    )
    embed.add_field(
        name="Chromas",
        value="\n".join(("➡️ " if i == data['chromas']['index'] else '') + f"{v}" for i,v in enumerate(chromas)),
        inline=True
    )


    return embed

'''
async def build_flair_overview(data):
    embed = discord.Embed(
        title=f"Flair - {data['bundle_assets']['displayName']}",
        description=f"{len(data['buddies'])} BUDDIES/{len(data['cards'])} CARDS/{len(data['sprays'])} SPRAYS",
        color=data['bundle_assets']['highlightColor']
    )

    embed.set_thumbnail(url=data['bundle_assets']['verticalPromoImage'])
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    emoji_index = 0

    

    return embed
'''