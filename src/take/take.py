
import argparse
import io
import math
import re

from contextlib import redirect_stdout

from .predicates import *

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
    def __init__(self, command_line : str) -> None:
        self.command_line = command_line
        self.literals : 'list[Literal]' = []
        self.variables_dict : 'dict[str,str|None]' = {} # to store variable instantiations
        self.parse()
    
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
        # TODO: maybe tuple of "" and Bool. The bool is set to True if the variable is instantiated, False otherwise
        # so I can reason on empty lines (otherwise, empty lines are "" which is the same as a variable not instantiated)
        # or use None instead of "" for uninstantiated variables

        # check singleton variables (i.e., variables appearing only once in the command)
        for var in self.variables_dict:
            if sum(var in lit.args for lit in self.literals) == 1:
                print(f"Warning: variable '{var}' appears only once in the command")



def parse_arguments():
    epilog = """
Available predicates (name and arity, i.e., number of arguments):
- line/2
- startswith/2
- endswith/2
- length/2
- lt/2
- gt/2
- leq/2
- eq/2
- neq/2
- capitalize/2
- strip/2
- contains/2
- time_to_seconds/2
- split_select/4
- replace/4
    
Examples:
    take -f log.txt -c "line(L), print(L)" -a count
    take -f f.txt -c "line(L), split_select(L,space,1,L1), println(L1)" -a sum -so
"""
    parser = argparse.ArgumentParser(description="Process a command line with logic predicates", 
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f", "--filename", required=True, type=str, help="Filename to process")
    parser.add_argument("-c", "--command", required=True, type=str, action="append", help="Command to process")
    parser.add_argument("-so", "--suppress-output", action="store_true", help="Suppress output, only show the result of the aggregation")
    parser.add_argument("-a", "--aggregate", action="append", choices=[
            "count",
            "sum",
            "product",
            "average",
            "min",
            "max",
            "concat",
            "unique",
            "first",
            "last",
            "sort_ascending",
            "sort_descending",
        ],
        help="Aggregation function to apply to the results")
    # parser.add_argument("-v", "--verbose", action="store_true",help="Enable verbose output")
    return parser.parse_args()


def loop_process(args : 'argparse.Namespace'):
    """
    Mail loop.
    """
    # print(args.command)
    aggregate_lines : 'list[str]' = []
    c_list : 'list[Command]' = [Command(cmd) for cmd in args.command]

    with open(args.filename, "r") as fp:
        for idx, current_line in enumerate(fp):
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
                        if command.is_negated:
                            print(f"Warning: the 'line' predicate cannot be negated, ignoring the negation")
                        res = line(current_line, command.args[0], c.variables_dict)
                    elif command.name == "print":
                        if command.is_negated:
                            print(f"Warning: the 'print' predicate cannot be negated, ignoring the negation")
                        if not args.suppress_output:
                            res = print_line(command.args[0], c.variables_dict)
                        if args.aggregate:
                            with io.StringIO() as buf, redirect_stdout(buf):
                                print_line(command.args[0], c.variables_dict)
                                aggregate_lines.append(buf.getvalue())
                    elif command.name == "println":
                        if command.is_negated:
                            print(f"Warning: the 'println' predicate cannot be negated, ignoring the negation")
                        if not args.suppress_output:
                            res = print_line(command.args[0], c.variables_dict, with_newline=True)
                        if args.aggregate:
                            with io.StringIO() as buf, redirect_stdout(buf):
                                print_line(command.args[0], c.variables_dict, with_newline=True)
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
        
    # check aggregation function
    if args.aggregate:
        for aggregate in args.aggregate:
            prefix = f"[{aggregate}] "
            if len(aggregate_lines) == 0:
                print("[Warning] No lines to aggregate")
                return
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
                res = '\n'.join(unique_lines)
                print(f"{prefix}{res}")
            elif aggregate == "first":
                res = aggregate_lines[0]
                print(f"{prefix}{res}")
            elif aggregate == "last":
                res = aggregate_lines[-1]
                print(f"{prefix}{res}")
            elif aggregate == "sort_ascending":
                # TODO: check if all elements are numbers, and if so sort them as numbers
                aggregate_lines = [line.rstrip('\n') for line in aggregate_lines]
                sorted_lines = sorted(aggregate_lines)
                res = '\n'.join(sorted_lines)
                print(f"{prefix}\n{res}")
            elif aggregate == "sort_descending":
                sorted_lines = sorted(aggregate_lines, reverse=True)
                res = '\n'.join(sorted_lines)
                print(f"{prefix}\n{res}")
            else:
                print(f"Unknown aggregation function: {aggregate}")

def take_main():
    """
    Main function to process the command line and file.
    """
    args = parse_arguments()
    loop_process(args)
    
    # print(c.literals)

