
import argparse
import io
import matplotlib.pyplot as plt
import os
import re
import time

from contextlib import redirect_stdout

from .aggregators import apply_aggregation_function
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
                print(f"{get_warning_prefix(not self.colored_output)} variable '{var}' appears only once in the command.")


def plot(data : 'list[tuple[str,str]]', uncolored : bool, keep_separated : bool) -> None:
    """
    Placeholder for a plotting function.
    """
    if not keep_separated:
        x_axis = list(range(len(data)))
        try:
            y_axis = [float(d[1]) for d in data]
            plt.plot(x_axis, y_axis)  # type: ignore
        except Exception as e:
            print(f"{get_error_prefix(uncolored)} Error plotting data: {e}")
    else:
        filenames = set(line[0] for line in data)
        for filename in filenames:
            y_axis = [float(line[1]) for line in data if line[0] == filename]
            x_axis = list(range(len(y_axis)))
            try:
                plt.plot(x_axis, y_axis, label=filename)  # type: ignore
            except Exception as e:
                print(f"{get_error_prefix(uncolored)} Error plotting data for {filename}: {e}")
    
    plt.show()  # type: ignore


def apply_sequence_commands(args : argparse.Namespace) -> 'list[tuple[str,str]]':
    """
    Apply a sequence of commands to the input file.
    This function is a placeholder for future implementation.
    """
    aggregate_lines : 'list[tuple[str,str]]' = []
    c_list : 'list[Command]' = [Command(cmd, colored_output=not args.uncolored) for cmd in args.command]
    count_processed : int = 0
    processed : bool = False
    stop_loop : bool = False
    context : 'list[str]' = []
    printed_warning : bool = False

    # explores recursively the directories if the -r option is set
    if args.recursive:
        files : 'list[str]' = []
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
            if args.keep_separated:
                count_processed = 0 # keep separated: process at most args.max_count lines per file
                processed = False
            with open(filename, "r") as fp:
                for idx, current_line in enumerate(fp):
                    if processed:
                        count_processed += 1
                    processed = False
                    if count_processed >= args.max_count and args.max_count > 0:
                        if not args.keep_separated:
                            stop_loop = True
                        break
                    current_line = current_line.rstrip('\n')
                    for c in c_list:
                        already_printed_filename = False
                        c.variables_dict = {var: None for var in c.variables_dict}
                        for command in c.literals:
                            res = False
                            if command.name == "line":
                                res = line(current_line, command.args[0], c.variables_dict)
                            elif command.name == "print" or command.name == "println":
                                processed = True
                                if not args.suppress_output:
                                    file_name = filename if args.with_filename else None
                                    res = print_line(command.args[0], c.variables_dict, with_newline=command.name == "println", filename=file_name, uncolored_output=args.uncolored, max_columns=args.max_columns, already_printed_filename=already_printed_filename)
                                    already_printed_filename = True
                                with io.StringIO() as buf, redirect_stdout(buf):
                                    print_line(command.args[0], c.variables_dict, with_newline=command.name == "println") # do not limit the length here
                                    gv : str = buf.getvalue()
                                    if gv.strip() != "":
                                        aggregate_lines.append((filename,gv))
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
        except Exception as e:
            print(f"{get_error_prefix(args.uncolored)} processing file {filename}")
            if args.debug:
                print(f"Error: {e}")

    return aggregate_lines    


def loop_process(args : 'argparse.Namespace'):
    """
    Main loop.
    """
    start_time = time.time()
    aggregate_lines = apply_sequence_commands(args)
    end_time = time.time()
    elapsed_time_file_analysis = end_time - start_time

    # check aggregation function
    if args.aggregate:
        res = apply_aggregation_function(aggregate_lines, args)
    else:
        res = aggregate_lines

    if args.stats:
        print(f"Elapsed time for file analysis: {elapsed_time_file_analysis:.2f} s.")

    if args.plot:
        if len(res) > 0:
            plot(res, args.uncolored, args.keep_separated)
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

