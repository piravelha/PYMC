# ================================================================================
# Thank you for using my compiler! This compiler is made by me, and is free to use.
# You don't need to credit me, but it would be appreciated.
# ================================================================================
# Instructions:
# 1. Put your mcpy (syntax is covered in yt tutorial) in the data/python/functions folder.
# 2. Run this file.
# 3. That's it! Your mcpy will be compiled into mcfunction files.
# ================================================================================
# Youtube tutorial: https://youtube.com/watch?v=HAVENT_UPLOADED_IT_YET
# ================================================================================
# Scroll down for the source code.
# ================================================================================

# Enter your namespace here:
NAMESPACE = 'namespace'











import os
import shutil
import re


# Clear the console:
os.system('cls' if os.name == 'nt' else 'clear')
print('Compiling Datapack...')

namespace_folder = f'data/{NAMESPACE}'
minecraft_folder = 'data/minecraft'
minecraft_function_tags_folder = f'{minecraft_folder}/tags/functions'

timer_order = 0

def create_function_tags():
    os.makedirs(minecraft_function_tags_folder, exist_ok=True)

    with open(f'{minecraft_function_tags_folder}/load.json', 'w') as load_f:
        load_f.write('{"values": ["'+NAMESPACE+':load"]}')

    with open(f'{minecraft_function_tags_folder}/tick.json', 'w') as tick_f:
        tick_f.write('{"values": ["'+NAMESPACE+':tick"]}')

    
def get_mcfunction_name(line):
    return line.split('/mcfunction')[1].strip().split('{')[0].strip()

def get_macroscore(line):
    macroscore_function = line.split('/%macroscore ')[1].split(' ')[0]

    arguments = " ".join(line.split('/%macroscore ')[1].split(' ')[1:]).split('|')
    arguments = [argument.strip() for argument in arguments]

    arguments = [((argument.split(']')[0]+']').lstrip(), (argument.split('] ')[1]).lstrip()) if '] ' in argument else (argument.split(' ')[0], argument.split(' ')[1]) for argument in arguments]

    score_arguments = [argument[1] for argument in arguments]
    score_selectors = [argument[0] for argument in arguments]

    macroscore_path = f'macroscores/{"_".join(score_arguments)}'
    return macroscore_function, score_selectors, macroscore_path

def loop_until_slash(lines, index, loop_command):
    next_line = lines[index + 1]
    loop_index = index

    full_loop_command = loop_command
    stripped_next_line = next_line.strip()

    while stripped_next_line != '':
        loop_index += 1
        
        if loop_index == len(lines) - 1:
            break

        if next_line.startswith('#'): 
            next_line = lines[loop_index + 1]
            continue

        if next_line.startswith('/'): break

        full_loop_command += ' ' + next_line
        next_line = lines[loop_index + 1]

    return full_loop_command

def get_loop(lines, line):
    loop_count = line.split(r'%loop ')[1].split(' ')[0]
    loop_command = ' '.join(line.split(r'%loop ')[1].split(' ')[1:])
    
    stripped_lines = [line.strip() for line in lines]
    stripped_line = line.strip()

    index = stripped_lines.index(stripped_line)

    full_loop_command = loop_until_slash(lines, index, loop_command)

    pre_loop_command = ''
    new_final_text = line[::-1]

    for old_line in lines[:index][::-1]:
        if old_line.endswith('#'): continue
        new_final_text += ' '+old_line[::-1]

    new_final_text = new_final_text[::-1]

    loop_command = re.sub(' +', ' ', loop_command)

    loop_command_position = new_final_text.find(f'%loop {loop_count}')

    for char in new_final_text[:(loop_command_position)][::-1]:
        if char == '/': break
        if char == '\n': pre_loop_command += ' '
        pre_loop_command += char

    pre_loop_command = pre_loop_command[::-1].strip()

    return loop_count, pre_loop_command, full_loop_command


def convert_time_duration(duration):
    duration_number = int(duration[:-1])
    
    if 't' in duration:
        return duration_number
    elif 's' in duration:
        return duration_number * 20
    elif 'm' in duration:
        return duration_number * 1200
    elif 'd' in duration:
        return duration_number * 24000


def get_timer(lines, line):
    timer_function = line.split('%timer ')[1].split(' ')[0]
    lines = [line.strip() for line in lines]

    index = lines.index(line)

    timer_duration = line.split('%timer ')[1].split(' ')[1]
    timer_duration = convert_time_duration(timer_duration)

    timer_path = f'{NAMESPACE}:timers/{timer_function.split(':')[1]}_{timer_duration}'

    pre_timer_command = ''
    timer_command = re.sub(' +', ' ', line)

    timer_command_position = line.find(f'%timer')

    for old_line in lines[:index][::-1]:
        if old_line.endswith('#'): continue
        line += ' '+old_line[::-1]

    line = line[::-1]
    
    for char in line[:(timer_command_position)][::-1]:
        if char == '/': break
        if char == '\n': pre_timer_command += ' '
        pre_timer_command += char

    pre_timer_command = pre_timer_command[::-1].strip()

    return timer_function, timer_duration, timer_path, pre_timer_command

def convert_minecraft_commands(input_text):
    global main_timer, timer_order

    if '# PATH: tick' in input_text: 
        input_text += '\n\n'+rf'/%loop 10 function {NAMESPACE}'+':timers/main {"i": %(i)}'

    lines = input_text.split('\n')[1:]
    lines.append('')

    final_text = ''

    brace_count = 0
    inside_mcfunction = False

    inside_loop = False

    mcfunction_name = None
    cur_mcfunction_command = ''
    mcfunction_commands = {}

    macroscores = {}
    loop_count = 0

    for index, line in enumerate(lines):
        stripped_line: str = line.strip()

        if '/mcfunction' in stripped_line:
            inside_mcfunction = True
        elif brace_count == 0:
            inside_mcfunction = False
        
        brace_count += stripped_line.count('{')
        brace_count -= stripped_line.count('}')

        is_mcfuntion = '/mcfunction' in stripped_line
        is_macroscore = '%macroscore' in stripped_line
        is_loop = r'%loop' in stripped_line
        is_timer = '%timer' in stripped_line
        is_definer_command = stripped_line.startswith('/')

        if is_macroscore: is_definer_command = False
        if is_loop: inside_loop = True
        if is_mcfuntion: mcfunction_name = get_mcfunction_name(stripped_line)

        if is_macroscore:
            macroscore_function, score_selectors, macroscore_path = get_macroscore(stripped_line)
            macroscores[macroscore_function] = (score_selectors, macroscore_path)

        if is_loop:
            loop_count, pre_loop_command, full_loop_command = get_loop(lines, stripped_line)

        if is_timer:
            timer_function, timer_duration, timer_path, pre_timer_command = get_timer(lines,stripped_line)

        def get_new_line(lines, line):
            global timer_order
            stripped_lines = [line.strip() for line in lines]
            stripped_line = line.strip()

            index = stripped_lines.index(stripped_line)
            
            is_last_line = index == len(lines) - 1
            new_line = stripped_line

            has_slash = is_definer_command or is_macroscore
            end_of_mcfunction = brace_count == 0 and inside_mcfunction

            if stripped_line.startswith('#'): return ''
            
            if has_slash:
                non_slash_line = stripped_line[1:]
                new_line = f'\n{non_slash_line} '

            elif end_of_mcfunction:
                non_brace_line = stripped_line.replace('{', '').replace('}', '')
                new_line = f'\n{non_brace_line} '

            if is_macroscore:
                stripped_line = stripped_line.replace('%macroscore', 'function')
                stripped_line = stripped_line.replace(
                    macroscore_function, 
                    f'{NAMESPACE}:{macroscore_path}'.lower()
                )

                stripped_line = stripped_line.split(macroscore_path.lower(), 1)[0] + macroscore_path.lower()

                new_line += stripped_line
                return new_line

            if is_timer:
                stripped_line = stripped_line.replace('%timer', 'function')

                init_file = f'{namespace_folder}/functions/{timer_path.replace(f'{NAMESPACE}:', '') + "_init"}.mcfunction'

                os.makedirs(os.path.dirname(init_file), exist_ok=True)

                with open(init_file, 'w') as f:
                    f.write(f'$scoreboard players set @s _Timer $(duration)\nexecute store result storage timers uuid.temp int 1 run data get entity @s UUID[0]\nfunction {timer_path+'_order'}')

                stripped_line = f'function {timer_path + "_init"} '+'{"duration": '+str(timer_duration)+'}'

                #if pre_timer_command:
                #    print("PRE TIMER COMMAND")

                order_file = f'{namespace_folder}/functions/{timer_path.replace(f'{NAMESPACE}:', '') + "_order"}.mcfunction'

                with open(order_file, 'w') as f:
                    f.write(f'\nexecute store result storage timers uuid.order int 1 run scoreboard players get .TimerOrder Vars\nscoreboard players add .TimerOrder Vars 1\nfunction {timer_path}_store with storage timers uuid')

                store_file = f'{namespace_folder}/functions/{timer_path.replace(f'{NAMESPACE}:', '') + "_store"}.mcfunction'

                with open(store_file, 'w') as f:
                    f.write('$data merge storage timers {"uuid": {'+str(timer_order)+': {"UUID": $(temp), "order":'+str(timer_order)+'}}}\n$tag @s add timer_'+str(timer_order)+'_$(temp)')

                with open(main_timer, 'a') as f:
                    f.write(f'\nfunction {timer_path}_loop with storage timers uuid.{timer_order}')

                loop_file = f'{namespace_folder}/functions/{timer_path.replace(f'{NAMESPACE}:', '') + "_loop"}.mcfunction'

                with open(loop_file, 'w') as f:
                    f.write(f'\n$execute as @e[tag=timer_'+str(timer_order)+f'_$(UUID)] if score @s _Timer matches 0 run function {timer_path}_run '+'{"UUID":$(UUID), "order":'+str(timer_order)+'}')

                run_file = f'{namespace_folder}/functions/{timer_path.replace(f'{NAMESPACE}:', '') + "_run"}.mcfunction'

                with open(run_file, 'w') as f:
                    f.write(f'\n$tag @s remove timer_'+str(timer_order)+f'_$(UUID)\nfunction {timer_function}')

                new_line = stripped_line
                timer_order += 1
                return new_line

            if is_loop:
                new_line = new_line.replace(r'%loop', r'&%loop')

            if inside_loop or is_last_line and not is_timer:
                reached_max_index = index == len(lines) - 1
                index -= 1 if reached_max_index else 0

                next_index = index + 1
                next_line = lines[next_index]

                stripped_next_line = next_line.strip()

                empty_line = stripped_next_line == ''

                while empty_line and not reached_max_index:

                    index += 1
                    
                    reached_max_index = index == len(lines) - 1
                    index -= 1 if reached_max_index else 0
                    if reached_max_index: break

                    next_line = lines[index]

                end_of_loop = stripped_next_line.startswith('/') or reached_max_index

                if end_of_loop: 
                    new_line += '&'

            if not is_macroscore and not is_loop and not is_timer:
                new_line = ' ' + new_line + ' '

            if stripped_line == '':
                new_line = ''

            return new_line

        if inside_mcfunction and not is_mcfuntion:
            cur_mcfunction_command += get_new_line(lines, line)
            
        if not inside_mcfunction:
            final_text += get_new_line(lines, line)

        if not inside_mcfunction and cur_mcfunction_command:
            mcfunction_commands[mcfunction_name] = cur_mcfunction_command[1:]
            cur_mcfunction_command = ''

        if is_definer_command and not is_loop: inside_loop = False

    lines = final_text.split('\n')

    final_lines = []

    for line in lines:
        if line.count('&') != 2: 
            final_lines.append(line)
            continue

        for i in range(int(loop_count)):
            if r'%loop' in pre_loop_command:
                pre_loop_list = pre_loop_command.split(' ')
                pre_loop_command = ' '.join(pre_loop_list[:-2])

            final_lines.append(f'\n{pre_loop_command} {full_loop_command.replace(fr"%(i)", str(i + 1))}')

    for line in final_lines:
        final_lines[final_lines.index(line)] = line.strip()
            
    for line in final_lines:
        final_lines[final_lines.index(line)] = re.sub(' +', ' ', line)

    
    for line in final_lines:
        if '%macroscore' in line:
            final_lines.remove(line)
        

    final_text = '\n'.join(final_lines)

    final_text = final_text.lstrip().replace('¹', '\n')

    return final_text, mcfunction_commands, macroscores


def extract_path(comment_line):
    paths = comment_line.split(':')[1:]
    return '/'.join(path.strip() for path in paths)

def get_full_path(path):
    path = path.replace(':', '/')
    path_list = path.split('/')
    path_list.insert(0, 'functions')
    path = '/'.join(path_list)
    return os.path.join(f'data/{NAMESPACE}', path + '.mcfunction')

functions_folder = 'data/python/functions'
ns_functions_folder = f'data/{NAMESPACE}/functions'
shutil.rmtree(f'data/{NAMESPACE}/functions', ignore_errors=True)
os.makedirs(f'data/{NAMESPACE}/functions', exist_ok=True)

main_timer = f'{ns_functions_folder}/timers/main.mcfunction'
os.makedirs(os.path.dirname(main_timer), exist_ok=True)

with open(main_timer, 'w') as f:
    f.write('scoreboard objectives add _Timer dummy\nscoreboard objectives add Vars dummy\nexecute unless score .TimerOrder Vars matches 0.. run scoreboard players set .TimerOrder Vars 1\nexecute unless score .TimerOrder Vars matches 0.. run scoreboard players set .TimerOrder Vars 0')

for function in os.listdir(functions_folder):
    with open(os.path.join(functions_folder, function)) as f:
        lines = f.readlines()
    
    if not lines and not lines[0].startswith('# PATH:'): continue

    path = extract_path(lines[0])
    input_text = ''.join(lines)

    final_text, mcfunction_commands, macroscores = convert_minecraft_commands(input_text)

    full_save_path = get_full_path(path)
    os.makedirs(os.path.dirname(full_save_path), exist_ok=True)

    with open(full_save_path, 'w') as f:
        f.write(final_text)

    for mcfunction_name, commands in mcfunction_commands.items():
        mcfunction_path = get_full_path(mcfunction_name)
        commands = re.sub(' +', ' ', commands)
        os.makedirs(os.path.dirname(mcfunction_path), exist_ok=True)

        with open(mcfunction_path, 'w') as mc_f:
            mc_f.write(commands)

    for macroscore_function, (macroscore_selector, macroscore_path) in macroscores.items():
        macroscore_path = get_full_path(macroscore_path)
        file_name = os.path.basename(macroscore_path).replace('.mcfunction', '')
        arguments = file_name.split('_')
        formatted_file_name = file_name.replace(' ', '_').lower()

        os.makedirs(os.path.dirname(macroscore_path), exist_ok=True)

        macroscore_path = macroscore_path.lower()

        with open(macroscore_path, 'w') as macroscore_f:
            used_arguments = []

            for index, argument in enumerate(arguments):
                underlined_argument = ''.join(['_' + i.lower() if i.isupper() else i for i in argument]).lstrip('_')

                used_arguments.append(argument)
                used_count = used_arguments.count(argument)
                storage_element_path = f'{underlined_argument}_{used_count}' if used_count > 1 else underlined_argument

                macroscore_f.write(
                    f'execute store result storage macroscores main.{storage_element_path} int 1 run scoreboard players get {macroscore_selector[index]} {argument}\n'
                )

            macroscore_f.write(f'function {macroscore_function} with storage macroscores main')

print('Finished Compiling... \n\nIf your datapack does not work, try checking the generated .mcfunction files for errors.\n')