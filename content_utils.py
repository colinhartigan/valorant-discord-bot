import asyncio
import valapi
import aiohttp


content_types = {
    'e7c63390-eda7-46e0-bb7a-a6abdacd2433':'weapon',
    '3f296c07-64c3-494c-923b-fe692a4fa1bd':'card',
    'd5f120f8-ff8c-4aac-92ea-f2b5acbe9475':'spray',
    'dd3bf334-87f3-40bd-b043-682a57a8dc3a':'buddy',
}

content_tiers = {
    "0cebb8be-46d7-c12a-d306-e9907bfc5a25":{
      "devName": "Deluxe",
      "highlightColor": 0x004c3d,
      "displayIcon": "https://media.valorant-api.com/contenttiers/0cebb8be-46d7-c12a-d306-e9907bfc5a25/displayicon.png",
      "assetPath": "ShooterGame/Content/ContentTiers/Deluxe_PrimaryAsset"
    },
    "e046854e-406c-37f4-6607-19a9ba8426fc":{
      "devName": "Exclusive",
      "highlightColor": 0xe07a06,
      "displayIcon": "https://media.valorant-api.com/contenttiers/e046854e-406c-37f4-6607-19a9ba8426fc/displayicon.png",
      "assetPath": "ShooterGame/Content/ContentTiers/Exclusive_PrimaryAsset"
    },
    "60bca009-4182-7998-dee7-b8a2558dc369":{
      "devName": "Premium",
      "highlightColor": 0xa21643,
      "displayIcon": "https://media.valorant-api.com/contenttiers/60bca009-4182-7998-dee7-b8a2558dc369/displayicon.png",
      "assetPath": "ShooterGame/Content/ContentTiers/Premium_PrimaryAsset"
    },
    "12683d76-48d7-84a3-4e09-6985794f0445":{
      "devName": "Select",
      "highlightColor": 0x1a58c1,
      "displayIcon": "https://media.valorant-api.com/contenttiers/12683d76-48d7-84a3-4e09-6985794f0445/displayicon.png",
      "assetPath": "ShooterGame/Content/ContentTiers/Select_PrimaryAsset"
    },
    "411e4a55-4e59-7757-41f0-86a53f101bb5":{
      "devName": "Ultra",
      "highlightColor": 0xdcd321,
      "displayIcon": "https://media.valorant-api.com/contenttiers/411e4a55-4e59-7757-41f0-86a53f101bb5/displayicon.png",
      "assetPath": "ShooterGame/Content/ContentTiers/Ultra_PrimaryAsset"
    }
}

currency_types = {
    "85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741":{
      "displayName": "Valorant Points",
      "displayNameSingular": "VP",
      "displayIcon": "https://media.valorant-api.com/currencies/85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741/displayicon.png",
      "assetPath": "ShooterGame/Content/Currencies/Currency_AresPoints_DataAsset"
    },
    "f08d4ae3-939c-4576-ab26-09ce1f23bb37":{
      "displayName": "Free Agents",
      "displayNameSingular": "Free Agent",
      "displayIcon": "https://media.valorant-api.com/currencies/f08d4ae3-939c-4576-ab26-09ce1f23bb37/displayicon.png",
      "assetPath": "ShooterGame/Content/Currencies/Currency_RecruitmentToken_DataAsset"
    },
    "e59aa87c-4cbf-517a-5983-6e81511be9b7":{
      "displayName": "Radianite",
      "displayNameSingular": "Radianite",
      "displayIcon": "https://media.valorant-api.com/currencies/e59aa87c-4cbf-517a-5983-6e81511be9b7/displayicon.png",
      "assetPath": "ShooterGame/Content/Currencies/Currency_UpgradeToken_DataAsset"
    }
}

content_base = 'https://valorant-api.com'

def get_content_type(uuid):
    return content_types[uuid]

async def get_theme_from_bundle_id(bundle_id):
    bundle = await valapi.get_content(f'/v1/bundles/{bundle_id}')
    themes = await valapi.get_content('/v1/themes')
    for i in themes['data']:
        if i['displayName'] == bundle['data']['displayName']:
            return i['uuid']

def get_content_tier(uuid):
    return content_tiers[uuid]

def get_currency_type(uuid):
    return currency_types[uuid]

def get_shop_item_from_id(uuid,bundle):
    for i in bundle['Items']:
        if i['Item']['ItemID'] == uuid:
            return i


# GET COLLECTION
async def get_collection(bundle_items,bundle):
    theme_weapons = []
    theme_sprays = []
    theme_buddies = []
    theme_cards = []
    async with aiohttp.ClientSession() as session:
        for i in bundle_items:
            item_type = get_content_type(i['Item']['ItemTypeID'])
            if item_type == 'weapon':
                async with session.get(f"{content_base}/v1/weapons") as data:
                    weapons = await data.json()
                    for j in weapons['data']:
                        for k in j['skins']:
                            if k['levels'][0]['uuid'] == i['Item']['ItemID']:
                                theme_weapons.append(k)
            elif item_type == 'card':
                async with session.get(f"{content_base}/v1/playercards/{i['Item']['ItemID']}") as data:
                    card = await data.json()
                    theme_cards.append(card['data'])
            elif item_type == 'spray':
                async with session.get(f"{content_base}/v1/sprays/{i['Item']['ItemID']}") as data:
                    spray = await data.json()
                    theme_sprays.append(spray['data'])
            elif item_type == 'buddy':
                async with session.get(f"{content_base}/v1/buddies") as data:
                    buddies = await data.json()
                    for j in buddies['data']:
                        if bundle['displayName'] in j['displayName']:
                            theme_buddies.append(j)
    return {
        'weapons':theme_weapons,
        'cards':theme_cards,
        'sprays':theme_sprays,
        'buddies':theme_buddies,
    }