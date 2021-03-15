import asyncio
 
converted_results = {
    'Eliminated':'elimination',
    'Bomb defused':'defusal',
    'Bomb detonated':'detonation',
    'Round timer expired':'time-out',
    'Surrendered':'surrender',
}

def get_team_name(mode,round,id):
    if mode == "Spike Rush":
        if round <= 3:
            if id == "Red":
                return "Attackers"
            else:
                return "Defenders"
        else:
            if id == "Red":
                return "Defenders"
            else:
                return "Attackers"
    elif mode == "Normal":
        if round <= 12:
            if id == "Red":
                return "Attackers"
            else:
                return "Defenders"
        else:
            if id == "Red":
                return "Defenders"
            else:
                return "Attackers"
            

def shorten_team_name(name):
    if name == "Attackers":
        return "ATK"
    else:
        return "DEF"


def strip_tag(name):
    return name[:name.find('#')]


def convert_result(result):
    return converted_results[result]