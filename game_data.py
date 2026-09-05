from addresses import *
import random

class GameData:
    def __init__(self, game):
        self.game = game
        self.char_map = {0x4F: ' ', 0x57: '#', 0x51: '*', 0x52: 'A1', 0x53: 'A2', 0x54: 'POKé', 0x55: '+',
        0x58: '$', 0x75: '…', 0x7F: ' ', 0x80: 'A', 0x81: 'B', 0x82: 'C', 0x83: 'D', 0x84: 'E', 0x85: 'F',
        0x86: 'G', 0x87: 'H', 0x88: 'I', 0x89: 'J', 0x8A: 'K', 0x8B: 'L', 0x8C: 'M', 0x8D: 'N', 0x8E: 'O',
        0x8F: 'P', 0x90: 'Q', 0x91: 'R', 0x92: 'S', 0x93: 'T', 0x94: 'U', 0x95: 'V', 0x96: 'W', 0x97: 'X',
        0x98: 'Y',0x99: 'Z', 0x9A: '(',
    }
        self.map_headers = {
            'maps_tileset': 0, 'maps_height': 0, 'maps_width': 0,
            'maps_data': 0, 'maps_text_pointer_table': 0, 'maps_level_script_pointer': 0,
            'maps_connection_byte': 0, 'maps_1st_connection_data': 0, 'maps_2nd_connection_data': 0,
            'maps_3rd_connection_data': 0, 'maps_4th_connection_data': 0, 'map_area': 0
        }
        self.tileset_headers = {
            'tileset bank': 0, 'pointer to blocks': 0, 'pointer to gfx': 0, 'pointer to collision data': 0,
            'talking-over tiles': 0, 'grass tile': 0, 'collision_data': 0
        }
        self.pos = {'x': 0, 'y' : 0, 'map': 0}
        self.tilemap = []
        
    def read_m(self, address):
        return self.game.memory[address]
    
    def get_data(self, start_pointer, end_pointer=0):
        data = []
        addr = start_pointer
        value = self.read_m(addr)
        if end_pointer == 0:
            while value != 255:
                addr += 1
                value = self.read_m(addr)
                data.append(value)
        elif end_pointer != 0 and addr < end_pointer:
            while addr < end_pointer:
                addr += 1
                value = self.read_m(addr)
                data.append(value)
        # Break the tiles list into 18 rows of 20 tiles each
        rows = [data[i:i+20] for i in range(0, len(data), 20)]
        self.tilemap = rows
        
    def set_tilemap(self):
        self.get_data(tilemap_start_address, tilemap_end_address+1)
        
    def get_tilemap(self):
        return self.tilemap
    
    def print_tilemap(self):
        for row in self.tilemap:
            print(row)
            
    def set_map_headers(self):
        self.map_headers['maps_tileset'] = self.read_m(map_headers[0])
        self.map_headers['maps_height'] = self.read_m(map_headers[1]) * 2
        self.map_headers['maps_width'] = self.read_m(map_headers[2]) * 2
        self.map_headers['maps_data'] = self.read_m(map_headers[3]) + 256 * self.read_m(map_headers[4])
        self.map_headers['maps_text_pointer_table'] = self.read_m(map_headers[5]) + 256 * self.read_m(map_headers[6])
        self.map_headers['maps_level_script_pointer'] = self.read_m(map_headers[7]) + 256 * self.read_m(map_headers[8])
        self.map_headers['maps_connection_byte'] = self.read_m(map_headers[9])
        self.map_headers['maps_1st_connection_data'] = self.read_m(map_headers[10]) + 256 * self.read_m(map_headers[11]) + 256 * 256 * self.read_m(map_headers[12])
        self.map_headers['maps_2nd_connection_data'] = self.read_m(map_headers[13]) + 256 * self.read_m(map_headers[14]) + 256 * 256 * self.read_m(map_headers[15])
        self.map_headers['maps_3rd_connection_data'] = self.read_m(map_headers[16]) + 256 * self.read_m(map_headers[17]) + 256 * 256 * self.read_m(map_headers[18])
        self.map_headers['maps_4th_connection_data'] = self.read_m(map_headers[19]) + 256 * self.read_m(map_headers[20]) + 256 * 256 * self.read_m(map_headers[21])
        self.map_headers['area'] = self.map_headers['maps_height'] * self.map_headers['maps_width']
        
    def get_map_headers(self):
        return self.map_headers
    
    def print_map_headers(self):
        for i in self.map_headers:
            print(f'{i}: {self.map_headers[i]}')
        
    def set_pos(self):
        self.pos['x'] = self.read_m(char_x)
        self.pos['y'] = self.read_m(char_y)
        self.pos['map'] = self.read_m(map_n)
        
    def get_pos(self):
        return self.pos
    
    def print_pos(self):
        print(f'x: {self.pos["x"]}, y: {self.pos["y"]}, map_n: {self.pos["map"]}')
        
    def read_collision_data(self, start_pointer):
        walkable_tiles = []
        tile_id = self.read_m(start_pointer)
        while tile_id != 255:
            walkable_tiles.append(tile_id)
            start_pointer += 1
            tile_id = self.read_m(start_pointer)
        return walkable_tiles
        
    def set_tileset_headers(self):
        self.tileset_headers['tileset bank'] = self.read_m(tileset_headers[0])
        self.tileset_headers['pointer to blocks'] = self.read_m(tileset_headers[1]) + 256 * self.read_m(tileset_headers[2])
        self.tileset_headers['pointer to gfx'] = self.read_m(tileset_headers[3]) + 256 * self.read_m(tileset_headers[4])
        self.tileset_headers['pointer to collision data'] = self.read_m(tileset_headers[5]) + 256 * self.read_m(tileset_headers[6])
        self.tileset_headers['collision_data'] = self.read_collision_data(self.tileset_headers['pointer to collision data'])
        self.tileset_headers['talking-over tiles'] = self.read_m(tileset_headers[7]) + 256 * self.read_m(tileset_headers[8]) + 256 * 256 * self.read_m(tileset_headers[9])
        self.tileset_headers['grass tile'] = self.read_m(tileset_headers[10])
        # self.tileset_headers['collision_tile_count'] = len(self.tileset_headers['collision_data'])
        
    def get_tileset_headers(self):
        return self.tileset_headers
    
    def print_tileset_headers(self):
        for i in self.tileset_headers:
            print(f'{i}: {self.tileset_headers[i]}')
            
    def set_encounter_data(self):
        self.encounter_data = {
            'encounter_rate': self.read_m(wild_pokemon_encounter_rate),
            'encounter_1_level': self.read_m(encounter_1_level),
            'encounter_2_level': self.read_m(encounter_2_level),
            'encounter_3_level': self.read_m(encounter_3_level),
            'encounter_4_level': self.read_m(encounter_4_level),
            'encounter_1_pokemon': self.read_m(encounter_1_pokemon),
            'encounter_2_pokemon': self.read_m(encounter_2_pokemon),
            'encounter_3_pokemon': self.read_m(encounter_3_pokemon),
            'encounter_4_pokemon': self.read_m(encounter_4_pokemon)
        }
        
    def get_encounter_data(self):
        return self.encounter_data
    
    def print_encounter_data(self):
        for i in self.encounter_data:
            print(f'{i}: {self.encounter_data[i]}')
            
    def write_m(self, address, value):
        self.game.memory[address] = value
    
    def get_random_pokemon(self):
        return random.choice(list(pokemon_data.keys()))
    
    def change_encounter_data(self):
        pokemon_num = self.get_random_pokemon()
        encounter_rate = self.read_m(wild_pokemon_encounter_rate)
        print(f'Encounter_rate: {encounter_rate}')
        print(f'Setting encounter Pokemon: {pokemon_data[pokemon_num]}')
        self.write_m(wild_pokemon_encounter_rate, 50)
        self.write_m(encounter_1_pokemon, pokemon_num)
        self.write_m(encounter_2_pokemon, pokemon_num)
        self.write_m(encounter_3_pokemon, pokemon_num)
        self.write_m(encounter_4_pokemon, pokemon_num)
        self.write_m(encounter_1_level, 40)
        self.write_m(encounter_2_level, 40)
        self.write_m(encounter_3_level, 40)
        self.write_m(encounter_4_level, 40)
        
    