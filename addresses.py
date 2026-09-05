tilemap_start_address = 0xC3A0
tilemap_end_address = 0xC507

pos = [0xD361, 0xD362, 0xD35E]
char_x = 0xD361
char_y = 0xD362
map_n = 0xD35E

total_items = 0xD31D

map_headers = [0xD367, 0xD368, 0xD369, 0xD36A, 0xD36B, 0xD36C, 0xD36D, 0xD36E, 0xD36F, 0xD370, 0xD371, 0xD372, 0xD373, 0xD374, 0xD375, 0xD376, 0xD377, 0xD378, 0xD379, 0xD37A, 0xD37B, 0xD37C]

tileset_headers = [0xD52B, 0xD52C, 0xD52D, 0xD52E, 0xD52F, 0xD530, 0xD531, 0xD532, 0xD533, 0xD534, 0xD535]

wild_pokemon_encounter_rate = 0xD887

encounter_1_level = 0xD888
encounter_2_level = 0xD88A
encounter_3_level = 0xD88C
encounter_4_level = 0xD88E
encounter_1_pokemon = 0xD889
encounter_2_pokemon = 0xD88B
encounter_3_pokemon = 0xD88D
encounter_4_pokemon = 0xD88F

pokemon_data = {
    1: 'rhydon', 2: 'kangaskhan', 3: 'nidoranb', 4: 'clefairy', 5: 'spearow', 6: 'voltorb',
    7: 'nidoking', 8: 'slowbro', 9: 'ivysaur', 10: 'executor', 11: 'lickitung', 12: 'exeggcute', 13: 'grimer',
    14: 'gengar', 15: 'nidorang', 16: 'nidoqueen', 17: 'cubone', 18: 'rhyhorn', 19: 'lapras', 20: 'arcanine',
    21: 'mew', 22: 'garados', 23: 'shelder', 24: 'tentacool', 25: 'gastly', 26: 'scyther', 27: 'staryu',
    28: 'blastoise', 29: 'pinsir', 30: 'tangela', 31: 'missingno', 32: 'missingno', 33: 'growlithe', 34: 'onix',
    35: 'fearow', 36: 'pidgey', 37: 'slowpoke', 38: 'kadabra', 39: 'graveler', 40: 'chansey', 41: 'machoke',
    42: 'mr. mime', 43: 'hitmonlee', 44: 'hitmonchan', 45: 'arbok', 46: 'parasect', 47: 'psyduck', 48: 'drowzee',
    49: 'golem', 50: 'missingno', 51: 'magmar', 52: 'missingno', 53: 'electabuzz', 54: 'magneton', 55: 'koffing',
    56: 'missingno', 57: 'mankey', 58: 'seel', 59: 'diglett', 60: 'tauros', 61: 'missingno', 62: 'farfetchd',
    63: 'venonat', 64: 'dragonite', 65: 'missingno', 66: 'missingno', 67: 'missingno', 68: 'missingno', 69: 'missingno',
    70: 'doduo', 71: 'poliwag', 72: 'jynx', 73: 'moltres', 74: 'articuno', 75: 'zapdos', 76: 'ditto', 77: 'meowth',
    78: 'krabby', 79: 'missingno', 80: 'missingno', 81: 'missingno', 82: 'missingno', 83: 'missingno', 84: 'vulpix',
    85: 'ninetales', 86: 'pikachu', 87: 'raichu', 88: 'dratini', 89: 'dragonair', 90: 'kabuto', 91: 'kabutops',
    92: 'missingno', 93: 'missingno', 94: 'missingno', 95: 'missingno', 96: 'sandshrew', 97: 'sandslash', 98: 'omanyte',
    99: 'omastar', 100: 'jigglypuff', 101: 'wigglytuff', 102: 'eevee', 103: 'flareon', 104: 'jolteon', 105: 'vaporeon',
    106: 'machop', 107: 'zubat', 108: 'ekans', 109: 'paras', 110: 'poliwhirl', 111: 'poliwrath', 112: 'weedle',
    113: 'kakuna', 114: 'beedrill', 115: 'missingno', 116: 'dodrio', 117: 'primeape', 118: 'dugtrio', 119: 'venomoth',
    120: 'dewgong', 121: 'missingno', 122: 'missingno', 123: 'caterpie', 124: 'metapod', 125: 'butterfree', 126: 'missingno',
    127: 'missingno', 128: 'golduck', 129: 'magikarp', 130: 'missingno', 131: 'missingno', 132: 'missingno', 133: 'missingno',
    134: 'missingno', 135: 'missingno', 136: 'missingno', 137: 'missingno', 138: 'kingler', 139: 'cloyster', 140: 'missingno',
    141: 'electrode', 142: 'clefable', 143: 'weezing', 144: 'persian', 145: 'marowak', 146: 'missingno', 147: 'haunter',
    148: 'abra', 149: 'alakazam', 150: 'pidgeotto', 151: 'pidgeot', 152: 'starmie', 153: 'bulbasaur', 154: 'venusaur',
    155: 'tentacruel', 156: 'missingno', 157: 'golduck', 158: 'seaking', 159: 'missingno', 160: 'missingno', 161: 'missingno',
    162: 'missingno', 163: 'ponyta', 164: 'rapidash', 165: 'rattata', 166: 'raticate', 167: 'nidorino', 168: 'nidorina',
    169: 'geodude', 170: 'porygon', 171: 'aerodactyl', 172: 'missingno', 173: 'magnemite', 174: 'missingno', 175: 'missingno',
    176: 'charmander', 177: 'squirtle', 178: 'charmeleon', 179: 'wartortle', 180: 'charizard', 181: 'missingno', 182: 'missingno',
    183: 'missingno', 184: 'missingno', 185: 'missingno', 186: 'oddish', 187: 'gloom', 188: 'vileplume', 189: 'bellsprout',
    190: 'weepinbell', 191: 'victreebel'
}

type_of_battle = 0xD057
battle_type = 0xD05A
slot_1_pokemon_number = 0xD014
enemy_pokemon_id = 0xCFD8
player_pokemon_id = 0xCFD9

