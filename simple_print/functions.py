import re
import traceback
from termcolor import cprint


def sprint(*args):

    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-2]
    code = code.strip()
    print_string = None
    color = "white"
    if re.compile(r'sprint\(\)').match(code):          
        print_string = "EMPTY PRINT"
    else:
        try:
            variables = [x.strip() for x in re.compile(r'\((.+)\).*$').search(code).groups()[0].split(',')]    
        except:
            variables = []

        if not args:
            args = []
            variables = None

        if len(variables) != len(args):
            variables = None

        if variables:              
            print_array = []
            len_variables = len(variables) - 1
            for i, variable in enumerate(variables):

                if len_variables == i and len_variables > 0 and variable.strip('"').strip("'") in ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
                    color = variables[-1].strip('"').strip("'")
                    continue

                if variable[0] and variable[-1] in ["'",'"']:
                    print_array.append(f'{args[i]}')
                else:
                    print_array.append(f'{variable}={args[i]}')

            if print_array:
                print_string = ' :: '.join(print_array)  

    if print_string:        
        cprint(f'{print_string} :: line {lineno}', color, 'on_cyan', attrs=['bold'])
    else:
        cprint(f'{code} :: line {lineno}', color, 'on_cyan', attrs=['bold'])


def sprint_f(*args):

    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-2]
    code = code.strip()
    print_string = None
    color = "white"
    if re.compile(r'sprint\(\)').match(code):          
        print_string = "EMPTY PRINT"
    else:
        try:
            variables = [x.strip() for x in re.compile(r'\((.+)\).*$').search(code).groups()[0].split(',')]    
        except:
            variables = []

        if not args:
            args = []
            variables = None

        if variables:              
            print_array = []
            len_variables = len(variables) - 1
            for i, variable in enumerate(variables):

                if len_variables == i and len_variables > 0 and variable.strip('"').strip("'") in ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
                    color = variables[-1].strip('"').strip("'")
                    continue

                if variable[0] and variable[-1] in ["'",'"']:
                    print_array.append(f'{args[i]}')
                else:
                    print_array.append(f'{variable}={args[i]}')

            if print_array:
                print_string = ' :: '.join(print_array)  

    if print_string:        
        cprint(f'{print_string} :: line {lineno} :: {filename}', color, attrs=['bold'])
    else:
        cprint(f'{code} :: line {lineno} :: {filename}', color, attrs=['bold'])
