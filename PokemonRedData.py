from pyboy import PyBoy
from pynput import keyboard
from collections import Counter
import threading
import time
import os
class PokemonRedData:
    def __init__(self, game_file='./PokemonRed.gb'):
        self.starting_states = ['states\\fast_text_start.state','states\init.state', 'states\has_pokedex.state', 'states\has_pokedex_nballs.state', 'PokemonRed.gb.state']
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.pyboy = PyBoy(game_file)
        self.frame_count = 0
        self.pressed_keys = set()
        self.state = {'running': True}
        self.tilemaps = {}
        self.screen = {}
        self.new_tm = {'addr': ''}
        self.new_item = {'addr': ''}
        self.map_headers = {
            'maps_tileset': 0, 'maps_height': 0, 'maps_width': 0,
            'maps_data': 0, 'maps_text_pointer_table': 0, 'maps_level_script_pointer': 0,
            'maps_connection_byte': 0, 'maps_1st_connection_data': 0, 'maps_2nd_connection_data': 0,
            'maps_3rd_connection_data': 0, 'maps_4th_connection_data': 0,
            'map_area': 0
        }
        self.tileset_headers = {
        'tileset bank': 0, 'pointer to blocks': 0, 'pointer to gfx': 0,
        'pointer to collision data': 0, 'talking-over tiles': 0, 'grass tile': 0,
        'collision_data': 0
        }
        
        def read_m(self, address, bank=0):
            return self.pyboy.memory[bank, address]

        def set_map_headers(self):
            self.map_headers.map_tileset = self.read_m(0xD367)
            self.map_headers.map_height = self.read_m(0xD368) * 2 # Converts tiles to blocks
            self.map_headers.map_width = self.read_m(0xD369) * 2 # Converts tiles to blocks
            self.map_headers.map_data = self.read_m(0xD36A) + 256 * self.read_m(0xD36B)
            self.map_headers['maps_text_pointer_table'] = self.read_m(0xD36C) + 256 * self.read_m(0xD36D)
            self.map_headers['maps_level_script_pointer'] = self.read_m(0xD36E) + 256 * self.read_m(0xD36F)
            self.map_headers['maps_connection_byte'] = self.read_m(0xD370)
            self.map_headers['maps_1st_connection_data'] = self.read_m(0xD371) + 256 * self.read_m(0xD372) + 256 * 256 * self.read_m(0xD373)
            self.map_headers['maps_2nd_connection_data'] = self.read_m(0xD374) + 256 * self.read_m(0xD375) + 256 * 256 * self.read_m(0xD376)
            self.map_headers['maps_3rd_connection_data'] = self.read_m(0xD377) + 256 * self.read_m(0xD378) + 256 * 256 * self.read_m(0xD379)
            self.map_headers['maps_4th_connection_data'] = self.read_m(0xD37A) + 256 * self.read_m(0xD37B) + 256 * 256 * self.read_m(0xD37C)
            self.map_headers['map_area'] = (self.map_headers['maps_height'] * self.map_headers['maps_width'])

        def set_tileset_headers(self):
            self.tileset_headers['tileset bank'] = self.read_m(0xD52B)
            self.tileset_headers['pointer to blocks'] = self.read_m(0xD52C) + 256 * self.read_m(0xD52D)
            self.tileset_headers['pointer to gfx'] = self.read_m(0xD52E) + 256 * self.read_m(0xD52F)
            self.tileset_headers['pointer to collision data'] = self.read_m(0xD530) + 256 * self.read_m(0xD531)
            self.tileset_headers['collision_data'] = self.read_collision_data(self.tileset_headers['pointer to collision data'])
            self.tileset_headers['talking-over tiles'] = self.read_m(0xD532) + 256 * self.read_m(0xD533) + 256 * 256 * self.read_m(0xD534)
            self.tileset_headers['grass tile'] = self.read_m(0xD535)
            self.tileset_headers['collision_tile_count'] = len(self.tileset_headers['collision_data'])
            
        def read_collision_data(self, start_pointer):
            walkable_tiles = []
            tile_id = self.read_m(start_pointer)
            while tile_id != 255:
                walkable_tiles.append(tile_id)
                start_pointer += 1
                tile_id = self.read_m(start_pointer)  # assuming read_m_bank is equivalent to read_m
            print(f'start_pointer: {start_pointer}')
            return walkable_tiles