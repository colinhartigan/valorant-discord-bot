import discord
import iso8601
import utils
import asyncio
import datetime



# ------------------------------------------------------------------------------------------
async def build_mmr_history(mmr,profile,initial=False):
    stats = profile['stats']
    rank_id = utils.get_rank_id(stats['rank'])

    embed = discord.Embed(
        title="Competitive Profile",
        description="",
        color=utils.get_rank_color(rank_id),
    )
    embed.set_author(name=profile['user'],icon_url=stats['playercard'] if stats['playercard'] is not None else utils.get_default_card())

    if mmr["status"] == "501":
        embed.description = "Unable to fetch competitive profile"
        embed.set_footer(text=("React with ⬜ to see profile details" if initial else ""))

    else:
        history = mmr['data']
        embed.description = f"{stats['rank']}" + f" ({history[0]['ranking_in_tier']}/100)"
        embed.set_thumbnail(url=utils.get_ranked_icon(rank_id))

        embed.set_footer(text=("React with ⬜ to see profile details" if initial else ""))

        for i,v in enumerate(history):
            if i == 6:
                break
            block = v
            movement = int(block['mmr_change_to_last_game'])
            timestamp = datetime.datetime.fromtimestamp(block['date_raw']/1000).strftime('%m/%d/%Y')

            embed.add_field(
                name=("⬆️ " if movement > 0 else "⬇️ " if movement < 0 else "= ")+timestamp,
                value=("**")+("+" if movement > 0 else "" if movement < 0 else "=")+(f"{block['mmr_change_to_last_game']}RR**")+(f"\n{block['currenttierpatched']}")+(f"\n{block['ranking_in_tier']}/100"),
                inline=True
            )

    return embed


async def build_profile_details(profile,mmr):
    stats = profile['stats']
    mmr_data = mmr['data']
    rank_id = utils.get_rank_id(stats['rank'])

    if mmr_data['currenttier'] == -1:
        rank_id = utils.get_rank_id(stats['rank'])

    embed = discord.Embed(
        title="Player Profile",
        description=(f"{stats['rank']}") + (f" ({mmr_data['ranking_in_tier']}/100)" if mmr['status'] != "501" else " (elo unavailable)" if mmr['status'] == "501" else ""),
        color=utils.get_rank_color(rank_id)
    )

    #change desc for immortal+
    if mmr_data['currenttier'] >= 21:
        embed.description = f"{stats['rank']}" + (f" ({mmr_data['elo']} elo)" if mmr['status'] != "500" else "")


    embed.set_author(name=profile['user'],icon_url=(stats['playercard'] if stats['playercard'] is not None else utils.get_default_card()))
    embed.set_thumbnail(url=utils.get_ranked_icon(rank_id))
    embed.set_footer(text="React with 🏅 to see competitive info\nReact with 🏆 to see recent matches")
    embed.add_field(
        name="KDA",
        value=f"{stats['kills']}/{stats['deaths']}/{stats['assists']} ({stats['kdratio']})",
        inline=True,
    )
    embed.add_field(
        name="Total Headshots",
        value=f"{stats['headshots']} ({stats['headshotpercentage']}%)",
        inline=True,
    )
    embed.add_field(
        name="Wins",
        value=stats['wins'],
        inline=True,
    )
    embed.add_field(
        name="Playtime",
        value=stats['playtime']['playtimepatched'],
        inline=True,
    )
    embed.add_field(
        name="Matches Played",
        value=stats['matches'],
        inline=True,
    )
    return embed
# ------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------
