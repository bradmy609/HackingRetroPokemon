import keyboard
from pyboy.utils import WindowEvent
from pyboy import PyBoy

starting_states = ['states\\fast_text_start.state','states\init.state', 'states\has_pokedex.state', 'states\has_pokedex_nballs.state', 'PokemonRed.gb.state']

# Initialize the emulator
pyboy = PyBoy('./PokemonRed.gb',
                debugging=True,
                disable_input=False,
                window_type='SDL2',)

frame_count = 0

def load_state(state):
    with open(state, "rb") as f:
        pyboy.load_state(f)

def read_m(addr):
    return pyboy.get_memory_value(addr)

def read_hp(start):
    input_byte = hex(start)
    value_at_start = read_m(start)
    value_at_start_plus_1 = read_m(start+1)
    combine_values = read_m(start) + read_m(start+1)
    hp = 256 * read_m(start) + read_m(start+1)
    print(f'input_byte: {input_byte}, value_at_start: {value_at_start} ({hex(value_at_start)}), value_at_start_plus_1: {value_at_start_plus_1} ({hex(value_at_start_plus_1)}), combine_values: {combine_values}, hp: {hp}')
    return hp

def read_hp_fraction():
    hp_sum = sum([read_hp(add) for add in [0xD16C, 0xD198, 0xD1C4, 0xD1F0, 0xD21C, 0xD248]])
    max_hp_sum = sum([read_hp(add) for add in [0xD18D, 0xD1B9, 0xD1E5, 0xD211, 0xD23D, 0xD269]])
    max_hp_sum = max(max_hp_sum, 1)
    return hp_sum / max_hp_sum

# Keybuttons

def check_memory(e):
    for i in range(0xD163, 0xD16A+1):
        print(f'{hex(i)}: {read_m(i)}')
    

def get_pos(e):
    y_pos = read_m(0xD361)
    x_pos = read_m(0xD362)
    map_n = read_m(0xD35E)
    print(x_pos, y_pos, map_n)

def get_hp_fraction(e):
    hp_fraction = read_hp_fraction()
    print(hp_fraction)
    
def go_fast(e):
    target_speed = 6
    pyboy.set_emulation_speed(target_speed)

def increment_x_pos(e):
    pyboy.set_memory_value(0xD362, (read_m(0xD362) + 1) % 256)

def change_health_value(e):
    high_byte = 400 // 256  # Integer division to get the high byte
    low_byte = 400 % 256  # Modulo operation to get the low byte
    # Set
    # pyboy.set_memory_value(0xD16C, 0)
    # pyboy.set_memory_value(0xD16D, 25)
    pyboy.set_memory_value(0xD18D, int(high_byte))
    pyboy.set_memory_value(0xD18E, int(low_byte))
    
# Defining key inputs

keyboard.on_press_key('9', change_health_value)
keyboard.on_press_key(';', go_fast)
keyboard.on_press_key('1', get_pos)
keyboard.on_press_key('-', increment_x_pos)
keyboard.on_press_key('q', check_memory)
keyboard.on_press_key('h', get_hp_fraction)

while not pyboy.tick():
    pass