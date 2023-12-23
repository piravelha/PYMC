NAMESPACE = 'namespace'
from pymc.utils import *

delete_all_functions(NAMESPACE)
clear_console()
start_log()

def convert_to_commands(input_text):
    """Converts the text input to minecraft commands"""
    
    path = get_path(input_text)

    input_text = remove_path(input_text)

    commands = get_command_list(input_text)
    commands = filter_commands(commands)
    commands = convert_percent_commands(commands, NAMESPACE)
    commands = filter_commands(commands)

    mcfunctions = get_mcfunctions(input_text)
    write_mcfunctions(mcfunctions, NAMESPACE)

    percent_commands = get_percent_commands(input_text)
    write_percent_commands(percent_commands, NAMESPACE)

    write_commands(commands, path, NAMESPACE)

functions_folder = f'data/python/functions'

for file in os.listdir(functions_folder):
    if file.endswith('.mcpy'):
        file_path = os.path.join(functions_folder, file)

        with open(file_path, 'r') as file:
            input_text = file.read()

        if file.name.split('\\')[-1] == 'tick.mcpy':
            input_text = init_tick_file(input_text, NAMESPACE)

        convert_to_commands(input_text)

end_log()