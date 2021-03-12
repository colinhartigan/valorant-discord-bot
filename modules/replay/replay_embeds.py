import asyncio
import modules.replay.replay_utils as replay_utils
import discord

#RED = ATTACK, BLUE = DEFEND

async def build_round_overview(data):

    embed = discord.Embed(
        title=f"ROUND // {data['round_id']}",
        description=f"**{data['winning_team_patched']}** won by **{data['end_type_converted']}**"
    )
    #add round k/d/a for each roster
    #maybe put footer with mode info/time
    return embed


async def build_timeline(data):
    round_data = data['round_data']
    timeline = data['timeline']['events']

    embed = discord.Embed(
        title=f"TIMELINE // {round_data['round_id']}",
        description="idk what to put here yet"
    )

    for event in timeline:
        if event['type'] == 'kill':
            embed.add_field(
                #[time] event
                #person -:skull:> otherPerson (:handshake: assist)
                name=f"[{event['time_in_round'][1:]}] :skull: "+(event['killer_team_patched'][:-1])+" Kill",
                value=f"[{replay_utils.shorten_team_name(event['killer_team_patched'])}] {event['killer_display_name_patched']} ► [{replay_utils.shorten_team_name(event['victim_team_patched'])}] {event['victim_display_name_patched']}" + ("".join(f"\n:wave: {i['assistant_display_name_patched']}" for i in event['assistants'] if len(event['assistants']) > 0)),
                inline=False
            )

        if event['type'] == 'plant' or event['type'] == 'defuse':
            embed.add_field(
                name=f"[{event['time_in_round'][1:]}] {':arrow_double_down: Spike Planted' if event['type'] == 'plant' else ':o: Spike Defused'}",
                value=f"[{replay_utils.shorten_team_name(event['planted_by']['team_patched'] if event['type'] == 'plant' else event['defused_by']['team'])}] {event['planted_by']['display_name_patched'] if event['type'] == 'plant' else event['defused_by']['display_name_patched']}"
            )

    return embed