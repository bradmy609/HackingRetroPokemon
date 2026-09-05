from pyboy import PyBoy
from pynput import keyboard
from collections import Counter
from game_data import *
import threading
import time
import os

starting_states = ['states\\fast_text_start.state','states\init.state', 'states\has_pokedex.state', 'states\has_pokedex_nballs.state', 'PokemonRed.gb.state']

# Initialize the emulator
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pyboy = PyBoy('./PokemonRed.gb')

game_data = GameData(pyboy)

frame_count = 0
pressed_keys = set()
state = {'running': True}
tilemaps = {}
screen = {}
total_items = {'quantity': 0}
new_tm = {'addr': ''}
new_item = {'addr': ''}
    
def on_press(key):
    try:
        if "`" in pressed_keys and key.char == '`':
            pressed_keys.clear()
        if '/' not in pressed_keys:
            pressed_keys.add(key.char)
        elif key.char == '/':
            pressed_keys.clear()
    except AttributeError:
       pass

def on_release(key):
    try:
        if key.char == '0':
            print('listener stopped.')
            return False
    except:
        if key == keyboard.Key.esc:
            print('Escape key released.')

def check_data(start_pointer):
    tile_ids = []
    start_pointer = start_pointer
    print(start_pointer)
    tile_id = read_m(start_pointer)
    while tile_id != 255:
        tile_ids.append(tile_id)
        start_pointer += 1
        tile_id = read_m(start_pointer)
    print(f'tile_ids: {tile_ids}')
    return tile_ids

# Use the function

def load_state(state):
    with open(state, "rb") as f:
        pyboy.load_state(f)

def read_m(addr):
    return pyboy.memory[addr]

def read_m_bank(addr, bank=0):
    return pyboy.memory[bank, addr]

def write_m(addr, new_value=0, bank=0):
    pyboy.memory[addr] = int(new_value)

def change_memory_values(start_byte, num_bytes, new_values, bank=0):
    print('start_byte: ', start_byte)
    print('num_bytes: ', num_bytes)
    print('new_values: ', new_values)
    print('bank: ', bank)
    if len(num_bytes != len(new_values)):
        raise ValueError('num_bytes and new_values must be the same length')
    for i in range(num_bytes):
        new_value = new_values[i]
        write_m(start_byte + i, new_value=new_value, bank=bank)

def read_hp(start):
    hp = 256 * read_m(start) + read_m(start+1)
    return hp

def read_hp_fraction():
    hp_sum = sum([read_hp(add) for add in [0xD16C, 0xD198, 0xD1C4, 0xD1F0, 0xD21C, 0xD248]])
    max_hp_sum = sum([read_hp(add) for add in [0xD18D, 0xD1B9, 0xD1E5, 0xD211, 0xD23D, 0xD269]])
    max_hp_sum = max(max_hp_sum, 1)
    return hp_sum / max_hp_sum

# Keybuttons

# ex. for Pokemon Red: 0xD163 - 0xD16A
def check_memory(start, end):
    for i in range(start, end+1):
        print(f'{hex(i)}: {read_m(i)}')
    
def get_pos():
    y_pos = read_m(0xD361)
    x_pos = read_m(0xD362)
    map_n = read_m(0xD35E)
    print(x_pos, y_pos, map_n)

def get_hp_fraction():
    hp_fraction = read_hp_fraction()
    print(f'HP fraction: {hp_fraction}')

def increment_x_pos(e):
    pyboy.set_memory_value(0xD362, (read_m(0xD362) + 1) % 256)

def change_health_value(e):
    high_byte = 400 // 256  # Integer division to get the high byte
    low_byte = 400 % 256  # Modulo operation to get the low byte
    # pyboy.set_memory_value(0xD16C, 0)
    # pyboy.set_memory_value(0xD16D, 25)
    pyboy.set_memory_value(0xD18D, int(high_byte))
    pyboy.set_memory_value(0xD18E, int(low_byte))
    
enemy_pkmon1_trainer_name = [0xd9ac,0xd9ad,0xd9ae,0xd9af,0xd9b0,0xd9b1,0xd9b2,0xd9b3,0xd9b4,0xd9b5,0xd9b6]
pkmon1_trainer_ids = [0xd8b0,0xd8b1]
pkmon1_trainer_id = [0xD177, 0xD178]
pkmon1_id = [0xD16B]
trainer_pkmon1 = [0xD164]
pkmon1_trainer_name = [0xd273,0xd274,0xd275]
# 0xd276,0xd277,0xd278,0xd279,0xd27a,0xd27b,0xd27c,0xd27d other trainer name byte locations

load_state('./PokemonRed.gb.state')

def increment_memory_values(mem_vals, increment):
    for address in mem_vals:
        memory_value = read_m(address)
        print(f'{hex(address)}: {memory_value} = {chr(memory_value)}')
        pyboy.set_memory_value(address, memory_value+increment)

incrementer = -10
# increment_memory_values(pkmon1_trainer_name, incrementer)
# increment_memory_values(pkmon1_trainer_ids, incrementer)
# increment_memory_values(pkmon1_trainer_id, incrementer)
# increment_memory_values(pkmon1_id, incrementer)
# increment_memory_values(trainer_pkmon1, incrementer)

start_time = time.time()
    
def press_key(key):
    cmd = "osascript -e 'tell application \"System Events\" to keystroke \"" + key + "\"'"
    os.system(cmd)
        
def convert_bytes_to_binary(data):
        all_flags = []
        for byte in data:
            flags = [bit for bit in format(byte, '08b')]
            print(f'flags: {flags}')
            all_flags.append(flags)
        count_ones = sum(sublist.count('1') for sublist in all_flags)
        count_zeros = sum(sublist.count('0') for sublist in all_flags)
        print(f'Number of 1s: {count_ones}')
        print(f'Number of 0s: {count_zeros}')
        return all_flags
    
def retrieve_items_and_quantities():
    items = {}
    total_items = read_m(0xD31D)

    for i in range(total_items):
        item_address = 0xD31E + i * 2
        quantity_address = item_address + 1
        item_index = i +1
        item = read_m(item_address)
        quantity = read_m(quantity_address)
        items[item_index] = {'item_id': item, 'item_quantity': quantity}
    for key, value in items.items():
        print(f'Item: {key}, ItemId: {value["item_id"]}, Quantity: {value["item_quantity"]}')
    return items

def create_tm(num=1):
    total_items = read_m(0xD31D)
    if new_tm['addr'] != '':
        last_item_address = new_tm['addr']
    elif new_tm['addr'] == '' and total_items <20:
        last_item_address = 0xD31E + (total_items) * 2
        new_tm['addr'] = last_item_address
        write_m(0xD31D, total_items + 1)
    else:
        return
    last_item_quantity_address = last_item_address + 1
    last_item_id = read_m(last_item_address)
    if last_item_id < 200 or last_item_id == 255:
        last_item_id = 200
    last_item_id += 1
    write_m(last_item_address, last_item_id)
    write_m(last_item_quantity_address, num)

def create_item(num):
    total_items = read_m(0xD31D)
    if new_item['addr'] != '':
        last_item_address = new_item['addr']
    if new_item['addr'] == '' and total_items < 20:
        last_item_address = 0xD31E + (total_items) * 2
        new_item['addr'] = last_item_address
        write_m(0xD31D, total_items + 1)
    else:
        return
    last_item_quantity_address = last_item_address + 1
    last_item_id = read_m(last_item_address)
    if last_item_id == 255:
        last_item_id = 19
    last_item_id += 1
    print(f'last item id: {hex(last_item_id)}')
    write_m(last_item_address, last_item_id)
    write_m(last_item_quantity_address, num)

def check_pressed_keys():
    if '4' in pressed_keys:
        pyboy.set_emulation_speed(4)
        pressed_keys.remove('4')
    if '9' in pressed_keys:
        create_tm(1)
        pressed_keys.remove('9')
    if '8' in pressed_keys:
        create_item(6)
        pressed_keys.remove('8')
    if '7' in pressed_keys:
        game_data.set_tilemap()
        game_data.print_tilemap()
        pressed_keys.remove('7')
    if '0' in pressed_keys:
        state['running'] = False
        pressed_keys.remove('0')
    if 'g' in pressed_keys:
        type_of_battle = read_m(0xD057)
        battle_type = read_m(0xD05A)
        slot_1_pokemon_number = read_m(0xD014)
        enemy_pokemon_id = read_m(0xCFD8)
        player_pokemon_id = read_m(0xCFD9)
        enemy_pokemon_id2 = read_m(0xCFE5)
        print('')
        print(f'type of battle: {type_of_battle}')
        print(f'battle type: {battle_type}')
        print(f'slot 1 pokemon number: {slot_1_pokemon_number}')
        print(f'enemy pokemon id: {enemy_pokemon_id}')
        print(f'player pokemon id: {player_pokemon_id}')
        print(f'enemy pokemon id 2: {enemy_pokemon_id2}')
        pressed_keys.remove('g')
    if 'm' in pressed_keys:
        tilemap = pyboy.tilemap_window
        print(tilemap)
        pressed_keys.remove('m')
    if 'b' in pressed_keys:
        game_data.set_encounter_data()
        game_data.print_encounter_data()
        game_data.change_encounter_data()
        pressed_keys.remove('b')
    if 'p' in pressed_keys:
        game_data.set_pos()
        game_data.print_pos()
        pressed_keys.remove('p')
    if 't' in pressed_keys:
        game_data.set_map_headers()
        game_data.print_map_headers()
        # print(f'Map headers: {map_headers}')
        # print()
        # print(f'Tileset headers: {tileset_headers}')
        # print(f'collision_data length: {len(tileset_headers["collision_data"])}')
        # print(f'collision_data: {tileset_headers["collision_data"]}')
        pressed_keys.remove('t')
    if '.' in pressed_keys:
        game_data.set_tileset_headers()
        game_data.print_tileset_headers()
        # check_data(tileset_headers['pointer to collision data'])
        # screen['tilemap_position_list'] = pyboy.screen.tilemap_position_list
        # screen['screen_ndarray.shape'] = pyboy.screen.ndarray.shape
        # print(f'tilemap_position_list: {screen["tilemap_position_list"]}')
        # print(f'screen_ndarray.shape: {screen["screen_ndarray.shape"]}')
        
        pressed_keys.remove('.')
    if ';' in pressed_keys:
        tilemaps['tilemap_window'] = pyboy.tilemap_window
        print(f'tilemap_window: {tilemap["tilemap_window"]}')
        # read_m()
        pressed_keys.remove(';')
    if 'w' in pressed_keys:
        pyboy.game_area_mapping(pyboy.game_wrapper.mapping_one_to_one)
        pyboy.game_area_mapping(pyboy.game_wrapper._set_dimensions(0, 0, 20, 18, True))
        game_area = pyboy.game_area()
        print('game_area: ')
        # print(game_area)
        print([list(row) for row in game_area])
        pressed_keys.remove('w')
    if '=' in pressed_keys:
        retrieve_items_and_quantities()
        pressed_keys.remove('=')
    else:
        if '/' not in pressed_keys:
            pressed_keys.clear()

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
thread = threading.Thread(target=listener.start)
thread.start()

commands = ['up', 'right', 'down', 'left']

def progress_frames(num_frames):
    for i in enumerate(range(0, num_frames)):
        if state['running'] == True:
            check_pressed_keys()
            pyboy.tick()

def input_command_and_progress_frames(commands, num_frames):
    for command in commands:
        pyboy.button(command)
        pyboy.tick()
            
tick_count = 26

while state['running']:
    if '`' in pressed_keys:
        input_command_and_progress_frames(commands, 1)
    else:
        progress_frames(tick_count)
    pass