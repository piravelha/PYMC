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

def get_mcfunction_name(line):
    return line.split('/mcfunction')[1].strip().split('{')[0].strip()

def convert_minecraft_commands(input_text):
    lines = input_text.split('\n')
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
        is_macroscore = '/%macroscore' in stripped_line
        is_loop = r'%loop' in stripped_line
        is_definer_command = stripped_line.startswith('/')
        if is_macroscore: is_definer_command = False

        if is_loop: inside_loop = True

        if is_mcfuntion: mcfunction_name = get_mcfunction_name(stripped_line)

        if is_macroscore:
            macroscore_function = stripped_line.split('/%macroscore ')[1].split(' ')[0]

            arguments = " ".join(stripped_line.split('/%macroscore ')[1].split(' ')[1:]).split('|')
            arguments = [argument.strip() for argument in arguments]

            arguments = [((argument.split(']')[0]+']').lstrip(), (argument.split('] ')[1]).lstrip()) if '] ' in argument else (argument.split(' ')[0], argument.split(' ')[1]) for argument in arguments]

            score_arguments = [argument[1] for argument in arguments]
            score_selectors = [argument[0] for argument in arguments]

            macroscore_path = f'macroscores/{"_".join(score_arguments)}'
            macroscores[macroscore_function] = (score_selectors, macroscore_path)

        if is_loop:
            loop_count = stripped_line.split(r'%loop ')[1].split(' ')[0]
            loop_command = ' '.join(stripped_line.split(r'%loop ')[1].split(' ')[1:])
            full_loop_command = loop_command

            loop_index = index

            next_line = lines[loop_index + 1]

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
            #full_loop_command = ' '.join(full_loop_command.split(r'%loop ')[1].split(' ')[1:])

            pre_loop_command = ''
            new_final_text = stripped_line[::-1]

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


        def get_new_line(index):
            new_line = stripped_line

            if stripped_line.startswith('#'): return ''
            
            if is_definer_command or is_macroscore:
                non_slash_line = stripped_line[1:]
                new_line = f'\n{non_slash_line} '

            elif brace_count == 0 and inside_mcfunction:
                non_brace_line = stripped_line.replace('{', '').replace('}', '')
                new_line = f'\n{non_brace_line} '


            if is_macroscore:
                final_line = stripped_line
                if is_definer_command or is_macroscore: final_line = '\n' + final_line

                final_line = final_line.replace('/%macroscore', 'function')
                final_line = final_line.replace(macroscore_function, f'{NAMESPACE}:{macroscore_path}'.lower())
                final_line = final_line.split(macroscore_path.lower(), 1)[0] + macroscore_path.lower()

                new_line += final_line
                return new_line

            if is_loop:
                new_line = new_line.replace(r'%loop', r'&%loop')

                #for i in range(int(loop_count)):
                #    new_line += f'\n{full_loop_command} {loop_command.replace(f'%(i)', str(i + 1))}'


            if inside_loop and (not is_definer_command):
                reached_max_index = False
                if index == len(lines) - 1: 
                    index -= 1
                    reached_max_index = True

                next_line = lines[index + 1]

                stripped_next_line = next_line.strip()

                while stripped_next_line == '' and not reached_max_index:
                    index += 1
                    
                    if index == len(lines) - 1:
                        index -= 1
                        reached_max_index = True
                        break

                    next_line = lines[index + 1]

                if stripped_next_line.startswith('/')\
                    or reached_max_index: 
                    new_line += '&'

            if not is_macroscore and not is_loop:
                new_line = ' ' + new_line + ' '

            if stripped_line == '':
                new_line = ''

            return new_line

        if inside_mcfunction and not is_mcfuntion:
            cur_mcfunction_command += get_new_line(index)
            
        if not inside_mcfunction:
            final_text += get_new_line(index)

        if not inside_mcfunction and cur_mcfunction_command:
            mcfunction_commands[mcfunction_name] = cur_mcfunction_command[1:]
            cur_mcfunction_command = ''

        if is_definer_command: inside_loop = False

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

    final_text = final_text.lstrip()

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
shutil.rmtree(f'data/{NAMESPACE}/functions', ignore_errors=True)
os.makedirs(f'data/{NAMESPACE}/functions', exist_ok=True)

for function in os.listdir(functions_folder):
    with open(os.path.join(functions_folder, function)) as f:
        lines = f.readlines()
    
    if not lines and not lines[0].startswith('# PATH:'): continue

    path = extract_path(lines[0])
    input_text = ''.join(lines[1:])  # Skip the first line

    final_text, mcfunction_commands, macroscores = convert_minecraft_commands(input_text)

    full_save_path = get_full_path(path)
    os.makedirs(os.path.dirname(full_save_path), exist_ok=True)

    with open(full_save_path, 'w') as f:
        f.write(final_text)

    for mcfunction_name, commands in mcfunction_commands.items():
        mcfunction_path = get_full_path(mcfunction_name)
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