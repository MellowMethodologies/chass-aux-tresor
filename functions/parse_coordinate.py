import re
import math

def find_closest_zaap(position_str):
    # Parse the position string to extract coordinates
    position = eval(position_str)  # Convert string to tuple (x, y)

    zaaps = """Amakna Castle[3,-5]
Amakna Village [-2,0]
Crackler Mountain [-5,-8]
Edge of the Evil Forest [-1,13]
Gobball Corner [5,7]
Madrestam Harbour [7,-4]
Scaraleaf Plain [-1,24] 
Snowbound Timberland[39,-82]
Astrub City[5,-18]
City Centre[-32,-56]
City Centre[-26,35]
Cania Lake[-3,-42]
Cania Massif[-13,-28]
Imp Village[-16,-24]
Kanig Village[0,-56]
Lousy Pig Plain[-5,-23]
Rocky Plains[-17,-47]
Rocky Roads[-20,-20]
The Cania Fields[-27,-36]
Arch of Vili[15,-20]
Dopple Village[-34,-8]
Entrance to Harebourg's Castle[-67,-75]
Frigost Village[-78,-41]
Snowbound Village[-77,-73]
Breeder Village[-16,1]
Turtle Beach[35,12]
Dunes of Bones[15,-58]
Canopy Village[-54,16]
Coastal Village[-46,18]
Pandala Village[20,-29]
Caravan Alley[-25,12]
Desecrated Highlands[-15,25]
Alliance Temple[13,35]
Sufokia[13,26]
Sufokian Shoreline[10,22]
The Cradle[1,-32]
Trool Fair[-11,-36]
"""

    # Corrected regex pattern
    pattern = r'([\w\s]+)\s*\[([-+]?\d+),\s*([-+]?\d+)\]'  
    matches = re.findall(pattern, zaaps)
    locations = {name.strip(): (int(x), int(y)) for name, x, y in matches}

    closest_zaap = None
    min_distance = float('inf')

    for name, (x, y) in locations.items():
        # Calculate Euclidean distance
        distance = math.sqrt((x - position[0]) ** 2 + (y - position[1]) ** 2)
        
        if distance < min_distance:
            min_distance = distance
            closest_zaap = name

    return closest_zaap
