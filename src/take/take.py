
import argparse
import io
import matplotlib.pyplot as plt
import math
import os
import re

from contextlib import redirect_stdout

from .arguments import parse_arguments
from .predicates import *
from .utils import *

class MalformedLiteralError(Exception):
    def __init__(self, literal: str) -> None:
        super().__init__(f"Malformed literal: {literal}")
        self.literal = literal
class LiteralNotFoundError(Exception):
    pass
class MissingLineError(Exception):
    pass

# constant to store the name and the arities of the predicates

class Literal:
    """
    Class containing a literal value.
    """
    def __init__(self, name : str, args : 'list[str]', is_negated : bool = False) -> None:
        self.name : str = name
        self.args : 'list[str]' = args
        self.is_negated : bool = is_negated
    def __str__(self):
        prefix = "not " if self.is_negated else ""
        return f"{prefix}{self.name}({', '.join(self.args)})"
    def __repr__(self):
        return self.__str__()

class Command:
    def __init__(self, command_line : str, colored_output : bool = True) -> None:
        self.command_line = command_line
        self.literals : 'list[Literal]' = []
        self.variables_dict : 'dict[str,str|None]' = {} # to store variable instantiations
        self.colored_output = colored_output
        self.parse()
        self.check_negation()

    def check_negation(self) -> None:
        """
        Check if the command line contains negated literals.
        """
        for literal in self.literals:
            if literal.is_negated and literal.name in ["line", "print", "println"]:
                if self.colored_output:
                    print(f"{bcolors.WARNING}[WARNING]{bcolors.ENDC}:", end=' ')
                else:
                    print("[WARNING]:", end=' ')
                print(f"the '{literal.name}' predicate cannot be negated, ignoring the negation.")

    def split_by_commas(self, s : str):
        in_quotes = False
        current : str = ""
        args : 'list[str]' = []
        for char in s:
            if char == "'":
                in_quotes = not in_quotes
            if char == ',' and not in_quotes:
                args.append(current.strip())
                current = ""
            else:
                current += char
        if current:
            args.append(current.strip())
        return args
    
    def parse(self) -> None:
        """
        Parse the command line and extract literals.
        """
        pattern = re.compile(r'''
            (?P<neg>not\s+)?                              # optional "not"
            (?P<name>[a-z][a-zA-Z0-9_]*)                  # predicate name
            \s*\(\s*
            (?P<args>
                (?:
                    (?:[A-Z][a-zA-Z0-9_]*                 # variable
                    |
                    [a-z][a-zA-Z0-9_]*                    # constant (lowercase)
                    |
                    '(?:[^'\\]|\\.)*'                     # quoted constant (handles escaped quotes)
                    |
                    \d+(?:\.\d+)?                         # number
                )
                (?:\s*,\s*
                    (?:[A-Z][a-zA-Z0-9_]*|[a-z][a-zA-Z0-9_]*|'(?:[^'\\]|\\.)*'|\d+(?:\.\d+)?)
                )*
            )?
            )
            \s*\)
        ''', re.VERBOSE)

        # literals = []
        malformed : 'list[str]' = []

        last_end = 0
        got_line = False # true if the predicate line/2 is used

        for match in pattern.finditer(self.command_line):
            # Capture unmatched text between matches
            unmatched = self.command_line[last_end:match.start()].strip(", \t\n")
            if unmatched:
                raise MalformedLiteralError(unmatched)
                malformed.append(unmatched)

            name = match.group('name')
            negated = match.group('neg') is not None
            raw_args = match.group('args')
            # args = [arg.strip() for arg in raw_args.split(',')]
            args = self.split_by_commas(raw_args) if raw_args else []
            if name not in PREDICATES:
                raise LiteralNotFoundError(f"Predicate '{name}' not implemented.")
            else:
                if len(args) != PREDICATES[name]:
                    raise LiteralNotFoundError(f"Predicate '{name}' expects {PREDICATES[name]} arguments, got {len(args)}.")
            
            if name == "line":
                got_line = True
            
            self.literals.append(Literal(name, args, negated))

            last_end = match.end()

        if not got_line:
            raise MissingLineError("The 'line' predicate is missing from the command line.")
        if self.literals[0].name != "line":
            raise MissingLineError("The first literal must be 'line(L)'.")

        # Check any remaining text after the last match
        unmatched = self.command_line[last_end:].strip(", \t\n")
        if unmatched:
            malformed.append(unmatched)
        
        # if len(malformed) > 0:
        #     for m in malformed:
        #         print(f"Malformed literal: {m}")
        
            # raise MalformedLiteralError()

        variables = list(set([arg for lit in self.literals for arg in lit.args if arg[0].isupper()]))
        self.variables_dict = {var: None for var in variables} 

        # check singleton variables (i.e., variables appearing only once in the command)
        for var in self.variables_dict:
            if sum(var in lit.args for lit in self.literals) == 1:
                if self.colored_output:
                    print(f"{bcolors.WARNING}[WARNING]{bcolors.ENDC}:", end=' ')
                else:
                    print("[WARNING]:", end=' ')
                print(f"variable '{var}' appears only once in the command.")


def plot(data : 'list[str]') -> None:
    """
    Placeholder for a plotting function.
    """
    x_axis = list(range(len(data)))
    try:
        plt.plot(x_axis, data)  # type: ignore
        plt.show()  # type: ignore
    except Exception as e:
        print(f"ERROR: Error plotting data: {e}")
        # Handle the error, e.g., log it or print a message
        # For now, just print the error



def apply_sequence_commands(args : argparse.Namespace) -> 'list[str]':
    """
    Apply a sequence of commands to the input file.
    This function is a placeholder for future implementation.
    """
    aggregate_lines : 'list[str]' = []
    c_list : 'list[Command]' = [Command(cmd, colored_output=not args.uncolored) for cmd in args.command]
    count_processed : int = 0
    processed : bool = False
    stop_loop : bool = False
    context : 'list[str]' = []
    printed_warning : bool = False

    # explores recursively the directories if the -r option is set
    if args.recursive:
        files = []
        for f in args.filename:
            if os.path.isdir(f):
                # if it's a directory, get all files in it
                w = os.walk(f)
                for root, _, filenames in w:
                    for filename in filenames:
                        files.append(os.path.join(root, filename))
            elif os.path.isfile(f):
                files.append(f)
        args.filename = files

    for filename in args.filename:
        if stop_loop:
            break
        try:
            with open(filename, "r") as fp:
                for idx, current_line in enumerate(fp):
                    if processed:
                        count_processed += 1
                    processed = False
                    if count_processed >= args.max_count and args.max_count > 0:
                        stop_loop = True
                        break
                    current_line = current_line.rstrip('\n')
                    # apply the corresponding predicates to the line
                    # print(f"Processing line: {current_line}")
                    # clean up the variables dictionary
                    for c in c_list:
                        c.variables_dict = {var: None for var in c.variables_dict}
                        for command in c.literals:
                            # print(f"Processing command: {command}")
                            # print(c.variables_dict)
                            # arity 1 predicates
                            # if command.name in ["print", "line"]:
                            #     fn = getattr(f"{command.name}", f"{command.name}")
                            #     res = fn(line, command.args[0], c.variables_dict)
                            res = False
                            if command.name == "line":
                                res = line(current_line, command.args[0], c.variables_dict)
                            elif command.name == "print" or command.name == "println":
                                processed = True
                                if not args.suppress_output:
                                    if args.with_filename:
                                        if not args.uncolored:
                                            print(f"{bcolors.PURPLE}{filename}:{bcolors.ENDC}", end='')
                                        else:
                                            print(f"{filename}:", end='')
                                    res = print_line(command.args[0], c.variables_dict, with_newline=command.name == "println")
                                # if args.aggregate:
                                with io.StringIO() as buf, redirect_stdout(buf):
                                    print_line(command.args[0], c.variables_dict, with_newline=command.name == "println")
                                    aggregate_lines.append(buf.getvalue())
                            elif command.name == "line_number":
                                res = line_number(command.args[0], command.args[1], idx, c.variables_dict, command.is_negated)
                            # arity 2 predicates
                            # elif command.name in ["startswith","endswith","length","lt","leq","gt"]:
                            elif command.name in [k for k in PREDICATES if PREDICATES[k] == 2]:
                                fn =  globals()[command.name]
                                res = fn(command.args[0], command.args[1], c.variables_dict, command.is_negated)
                            elif command.name in [k for k in PREDICATES if PREDICATES[k] == 3]:
                                fn =  globals()[command.name]
                                res = fn(command.args[0], command.args[1], command.args[2], c.variables_dict, command.is_negated)
                            elif command.name in [k for k in PREDICATES if PREDICATES[k] == 4]:
                                fn =  globals()[command.name]
                                res = fn(command.args[0], command.args[1], command.args[2], command.args[3], c.variables_dict, command.is_negated)
                            
                            if not res:
                                break
        except Exception:
            if args.uncolored:
                print("[ERROR]", end=' ')
            else:
                print(f"{bcolors.ERROR}[ERROR]{bcolors.ENDC}", end=' ')
            print(f"processing file {filename}")

    return aggregate_lines    


def apply_aggregation_function(aggregate_lines : 'list[str]', args : argparse.Namespace) -> 'list[str] | list[float]':
    """
    Apply the aggregate function.
    """
    # check aggregation function
    obtained_data : 'list[str] | list[float]' = []
    for aggregate in args.aggregate:
        if args.uncolored:
            prefix = f"[{aggregate}] "
        else:
            prefix = f"{bcolors.GREEN}[{aggregate}]{bcolors.ENDC} "
        if len(aggregate_lines) == 0:
            if colored:
                print(f"{bcolors.WARNING}[WARNING]{bcolors.ENDC}:", end=' ')
            else:
                print("[WARNING]:", end=' ')
            print("No lines to aggregate")
            return []
        if aggregate == "count":
            print(f"{prefix}{len(aggregate_lines)}")
        elif aggregate == "sum":
            total = sum(float(line) for line in aggregate_lines)
            print(f"{prefix}{total}")
        elif aggregate == "product":
            total = math.prod(float(line) for line in aggregate_lines)
            print(f"{prefix}{total}")
        elif aggregate == "average":
            total = sum(float(line) for line in aggregate_lines)
            count = len(aggregate_lines)
            res = total / count if count > 0 else 0
            print(f"{prefix}{res}")
        elif aggregate == "min":
            res = min(float(line) for line in aggregate_lines)
            print(f"{prefix}{res}")
        elif aggregate == "max":
            res = max(float(line) for line in aggregate_lines)
            print(f"{prefix}{res}")
        elif aggregate == "concat":
            res = ''.join(aggregate_lines)
            print(f"{prefix}{res}")
        # elif aggregate == "join": # TODO: with a separator
        #     print(', '.join(aggregate_lines))
        elif aggregate == "unique":
            unique_lines = set(aggregate_lines)
            obtained_data = list(unique_lines)
            res = '\n'.join(unique_lines)
            print(f"{prefix}{res}")
        elif aggregate == "first":
            res = aggregate_lines[0]
            print(f"{prefix}{res}")
        elif aggregate == "last":
            res = aggregate_lines[-1]
            print(f"{prefix}{res}")
        elif aggregate == "sort_ascending":
            sorted_lines = wrap_sort(aggregate_lines, reverse=False)
            obtained_data = sorted_lines
            res = '\n'.join([str(s) for s in sorted_lines])
            print(f"{prefix}\n{res}")
        elif aggregate == "sort_descending":
            sorted_lines = wrap_sort(aggregate_lines, reverse=True)
            obtained_data = sorted_lines
            res = '\n'.join([str(s) for s in sorted_lines])
            print(f"{prefix}\n{res}")
        else:
            print(f"Unknown aggregation function: {aggregate}")

    return obtained_data


def loop_process(args : 'argparse.Namespace'):
    """
    Main loop.
    """
    aggregate_lines : 'list[str]' = apply_sequence_commands(args)

    # check aggregation function
    if args.aggregate:
        res = apply_aggregation_function(aggregate_lines, args)
    else:
        res = aggregate_lines
        
    if args.plot:
        if len(res) > 0:
            plot(res)
        else:
            if args.uncolored:
                print("[WARNING]:", end=' ')
            else:
                print(f"{bcolors.WARNING}[WARNING]{bcolors.ENDC}:", end=' ')
            print("no data to plot.")


def take_main():
    """
    Main function to process the command line and file.
    """
    args = parse_arguments()
    loop_process(args)
    
    # print(c.literals)

