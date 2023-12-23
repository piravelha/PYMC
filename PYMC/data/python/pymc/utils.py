import os
import shutil
import re
import re

timer_count = 1
macroscore_count = 1

def delete_all_functions(NAMESPACE):
    """Deletes all functions in the datapack"""

    shutil.rmtree(f'data/{NAMESPACE}/functions')
    os.mkdir(f'data/{NAMESPACE}/functions')

def clear_console():
    """Clears the console"""

    os.system('cls' if os.name == 'nt' else 'clear')

def start_log():
    """Starts the log file"""

    print('Compiling...')

def end_log():
    """Ends the log file"""

    print('Done!')

def get_path(input_text):
    """Returns the path of the file to be compiled"""
    input_text = input_text.strip()
    if not '# PATH: ' in input_text: raise(Exception('No path specified'))

    path = input_text.split('\n', 1)[0].split(': ')[1]
    return path

def remove_path(input_text):
    """Removes the path comment from the input text"""

    return input_text.split('\n', 1)[1]

def get_command_list(input_text):
    """Returns a list of commands split after every slash '/' that is preceded by a space or a line break"""

    commands = re.split(r'(?<=[\s\n])/', input_text)
    print(commands)

    return commands

def filter_commands(commands, is_final = False):
    """Filters the commands to remove empty lines, comments, and line breaks"""
    
    original_commands = commands

    commands = [command.strip() for command in commands]
    commands = [command[1:] if command.startswith('/') else command for command in commands]
    commands = filter(lambda x: x != '' and not x.startswith('#'), commands)
    commands = [command.replace('\n', ' ') for command in commands]
    commands = [re.sub(' +', ' ', command).strip() for command in commands]

    inside_mcfunction = False
    num_brackets = 0

    filtered_commands = []

    for command in commands:
        num_brackets += command.count('{')
        num_brackets -= command.count('}')

        if 'mcfunction' in command:
            inside_mcfunction = True
    
        last_command = num_brackets == 0 and inside_mcfunction

        if not inside_mcfunction:
            filtered_commands.append(command)

        if last_command:
            inside_mcfunction = False

    if not is_final:
        filtered_commands = filter_commands(filtered_commands, True)

    return list(filtered_commands)

def filter_other_commands(commands):
    """Filters the commands from other to remove empty lines, comments, and line breaks"""

    commands = [command.strip() for command in commands]
    commands = [command[1:] if command.startswith('/') else command for command in commands]
    commands = filter(lambda x: x != '' and not x.startswith('#'), commands)
    commands = [command.replace('\n', '') for command in commands]
    commands = [re.sub(' +', ' ', command).strip() for command in commands]

    return list(commands)

def remove_extra_brackets(input_text, command, mcfunction_name, mcfunction_code):
    if command.startswith(f'mcfunction {mcfunction_name}'):
        new_command = input_text.split(f'mcfunction {mcfunction_name} ')[1]
        num_brackets = 0

        for char_index, char in enumerate(new_command):
            num_brackets += 1 if char == '{' else 0
            num_brackets -= 1 if char == '}' else 0

            if num_brackets == 0:
                new_command = new_command[:char_index + 1]
                break

        mcfunction_code.append(new_command)
    
    return mcfunction_code

def get_mcfunctions(input_text):
    """Returns the mcfunctions in the input text"""

    commands = get_command_list(input_text)
    mcfunctions = {}

    mcfunction_names = re.findall(r'(?<=mcfunction\s)\w+', input_text)
    mcfunction_codes = []

    for mcfunction_name in mcfunction_names:
        mcfunction_code = []

        for command in commands:
            mcfunction_code = remove_extra_brackets(input_text, command, mcfunction_name, mcfunction_code)

        mcfunction_codes.append(mcfunction_code)

    filtered_mcfunction_codes = []

    for mcfunction_code in mcfunction_codes:
        filtered_mcfunction_codes.append(filter_other_commands(mcfunction_code))

    mcfunctions = {mcfunction_names[i]: filtered_mcfunction_codes[i] for i in range(len(mcfunction_names))}

    for mcfunction_name in mcfunctions:
        mcfunction_code = mcfunctions[mcfunction_name]

        if mcfunction_code[0].startswith('{'):
            mcfunction_code[0] = mcfunction_code[0][1:]

        if mcfunction_code[-1].endswith('}'):
            mcfunction_code[-1] = mcfunction_code[-1][:-1]

        for index, mcfunction_code_commandblock in enumerate(mcfunction_code):
            mcfunction_code[index] = mcfunction_code_commandblock.strip()
            mcfunction_code[index] = mcfunction_code[index].replace('/', '\n')


    return mcfunctions

def write_mcfunctions(mcfunctions, NAMESPACE):
    """Writes the mcfunctions to the datapack"""

    for mcfunction_name in mcfunctions:
        mcfunction_code = mcfunctions[mcfunction_name]
        mcfunction_path = f'data/{NAMESPACE}/functions/{mcfunction_name}.mcfunction'

        with open(mcfunction_path, 'w') as mcfunction_file:
            for command in mcfunction_code:
                mcfunction_file.write(f'{command}\n')

def convert_duration(timer_duration):
    """Converts duration in various formats to ticks"""

    if timer_duration.endswith('t'):
        return int(timer_duration[:-1])
    elif timer_duration.endswith('s'):
        return int(timer_duration[:-1]) * 20
    elif timer_duration.endswith('m'):
        return int(timer_duration[:-1]) * 1200
    elif timer_duration.endswith('h'):
        return int(timer_duration[:-1]) * 72000
    elif timer_duration.endswith('d'):
        return int(timer_duration[:-1]) * 24000
    else:
        return int(timer_duration)

def percent_command_timer(command):
    """Converts the percent timer command to a function call"""

    timer_arguments = command.split('%timer ')[1]
    timer_function = timer_arguments.split(' ')[0]
    timer_function = timer_function.split(':')[0] + ':timers/' + timer_function.split(':')[1]

    timer_duration = timer_arguments.split(' ')[1]

    timer_duration = convert_duration(timer_duration)

    return f'function {timer_function}_{timer_duration}'

def percent_command_macroscore(command, NAMESPACE):
    """Converts the percent macroscore command to a function call"""

    global macroscore_count

    macroscore_arguments = command.split('%macroscore ')[1]
    macroscore_function = macroscore_arguments.split(' ')[0]
    macroscore_function = macroscore_function.split(':')[0] + ':macroscores/' + macroscore_function.split(':')[1]

    return f'function {macroscore_function}_{macroscore_count}'

def convert_percent_commands(commands, NAMESPACE):
    """Converts the percent commands to function calls"""

    for command in commands:
        if '%timer' in command:
            pre_timer_command = command.split('%timer')[0]
            pos_timer_command = ' '.join(command.split('%timer')[1].split(' ')[3:])
            new_command = f'{pre_timer_command} {percent_command_timer(command)} {pos_timer_command}'
            commands[commands.index(command)] = new_command

        elif '%macroscore' in command:
            pre_macroscore_command = command.split('%macroscore')[0]
            pos_macroscore_command = ' '.join(command.split('%macroscore')[1].split(' ')[2:])
            new_command = f'{pre_macroscore_command} {percent_command_macroscore(command, NAMESPACE)}'
            commands[commands.index(command)] = new_command

    return commands

def write_commands(commands, file_name, NAMESPACE):
    """Writes the commands to the file"""

    file_path = f'data/{NAMESPACE}/functions/{file_name}.mcfunction'

    with open(file_path, 'a') as file:
        for command in commands:
            file.write(f'{command}\n')

def get_percent_commands(input_text):
    """Returns the percent commands in the input text"""

    commands = get_command_list(input_text)
    percent_commands = []

    for command in commands:
        if '%' in command:
            percent_command = command.split('%')[1]
            percent_commands.append(percent_command)

    filtered_percent_commands = filter_other_commands(percent_commands)

    return filtered_percent_commands

def init_tick_file(input_text, NAMESPACE):
    return input_text + f'\n/function {NAMESPACE}:timers/main'

def write_percent_commands(percent_commands, NAMESPACE):
    """Writes the percent commands to the datapack"""

    global timer_count, macroscore_count

    timer_main_function_path = f'data/{NAMESPACE}/functions/timers/main.mcfunction'
    tick_function = f'data/{NAMESPACE}/functions/tick.mcfunction'

    os.makedirs(os.path.dirname(timer_main_function_path), exist_ok=True)
    os.makedirs(os.path.dirname(tick_function), exist_ok=True)

    load_function_path = f'data/{NAMESPACE}/functions/load.mcfunction'

    for percent_command in percent_commands:

        # %Timer

        if 'timer' in percent_command:
            timer_function = percent_command.split(' ')[1]
            timer_function_name = timer_function.split(':')[1]

            timer_duration = percent_command.split(' ')[2]
            timer_duration = convert_duration(timer_duration)

            init_function_path = f'data/{NAMESPACE}/functions/timers/{timer_function_name}_{timer_duration}.mcfunction'

            with open(tick_function, 'a') as file:
                file.write(f'\nexecute as @e if score @s _Timer{timer_count} matches 1.. run scoreboard players remove @s _Timer{timer_count} 1\n')

            with open(timer_main_function_path, 'a') as file:
                file.write(f'scoreboard objectives add _Timer{timer_count} dummy\nexecute as @e[tag=timer_{timer_count}] if score @s _Timer{timer_count} matches 0 run function {timer_function}\nexecute as @e[tag=timer_{timer_count}] if score @s _Timer{timer_count} matches 0 run tag @s remove timer_{timer_count}\n')

            with open(load_function_path, 'a') as file:
                file.write(f'tag @e remove timer_{timer_count}\n')

            with open(init_function_path, 'w') as file:
                file.write(f'tag @s add timer_{timer_count}\nscoreboard players set @s _Timer{timer_count} {timer_duration}')

            timer_count += 1


        # %macroscore
            
        elif 'macroscore' in percent_command:
            macro_function = percent_command.split(' ')[1]
            macro_function_name = macro_function.split(':')[1]
            macro_scores = [
                argument.split(' ') 
                for argument in' '.join(percent_command.split(' ')[2:]).split('|')
            ]

            macro_scores = [re.sub(' +', ' ', ' '.join(macro_score)).strip().split(' ') for macro_score in macro_scores]

            init_function_path = f'data/{NAMESPACE}/functions/macroscores/{macro_function_name}_{macroscore_count}.mcfunction'

            os.makedirs(os.path.dirname(init_function_path), exist_ok=True)

            for index, macro_score in enumerate(macro_scores):
                index += 1

                score_selector = macro_score[0]
                score_objective = macro_score[1]

                with open(init_function_path, 'a') as file:
                    file.write(f'execute store result storage macroscores main.{index} int 1 run scoreboard players get {score_selector} {score_objective}\n')

            with open(init_function_path, 'a') as file:
                file.write(f'function {macro_function} with storage macroscores main\n')

            macroscore_count += 1