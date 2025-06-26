from .predicates import *

import argparse
import re
import sys

class MalformedLiteralError(Exception):
    pass
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
        self.variables_dict : 'dict[str,str]' = {} # to store variable instantiations
        self.parse()
    
    def parse(self) -> None:
        """
        Parse the command line and extract literals.
        """
        pattern = re.compile(r'''
            (?P<neg>not\s+)?                      # optional negation
            (?P<name>[a-z][a-zA-Z0-9_]*)          # predicate name
            \(
                (?P<args>
                    \s*
                    (?:
                        [a-zA-Z][a-zA-Z0-9_]*        # uppercase identifier
                        |
                        \d+(?:\.\d+)?             # or number
                    )
                    (?:\s*,\s*
                        (?:
                            [a-zA-Z][a-zA-Z0-9_]*
                            |
                            \d+(?:\.\d+)?
                        )
                    )*
                )
            \)
        ''', re.VERBOSE)

        # literals = []
        malformed : 'list[str]' = []

        last_end = 0
        got_line = False # true if the predicate line/2 is used

        for match in pattern.finditer(self.command_line):
            # Capture unmatched text between matches
            unmatched = self.command_line[last_end:match.start()].strip(", \t\n")
            if unmatched:
                raise MalformedLiteralError()
                malformed.append(unmatched)

            name = match.group('name')
            negated = match.group('neg') is not None
            raw_args = match.group('args')
            args = [arg.strip() for arg in raw_args.split(',')]
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
        self.variables_dict = {var: "" for var in variables}


        # check singleton variables (i.e., variables appearing only once in the command)
        for var in self.variables_dict:
            if sum(var in lit.args for lit in self.literals) == 1:
                print(f"Warning: variable '{var}' appears only once in the command")



def parse_arguments():
    parser = argparse.ArgumentParser(description="Process a command line with logic predicates")
    parser.add_argument("-f", "--filename", required=True, type=str, help="Filename to process")
    parser.add_argument("-c", "--command", required=True, type=str, help="Command to process")
    # parser.add_argument("-v", "--verbose", action="store_true",help="Enable verbose output")
    return parser.parse_args()


def take_main():
    """
    Main function to process the command line and file.
    """
    args = parse_arguments()

    c = Command(args.command)
    # print(c.literals)

    fp = open(args.filename, "r")
    lines = fp.read().splitlines()
    fp.close()

    # print(f"Processing file: {args.filename}")
    for current_line in lines:
        # apply the corresponding predicates to the line
        # print(f"Processing line: {current_line}")
        # clean up the variables dictionary
        c.variables_dict = {var: "" for var in c.variables_dict}
        for command in c.literals:
            # arity 1 predicates
            # if command.name in ["print", "line"]:
            #     fn = getattr(f"{command.name}", f"{command.name}")
            #     res = fn(line, command.args[0], c.variables_dict)
            res = False
            if command.name == "line":
                res = line(current_line, command.args[0], c.variables_dict)
            elif command.name == "print":
                res = print_line(command.args[0], c.variables_dict)
            # arity 2 predicates
            # elif command.name in ["startswith","endswith","length","lt","leq","gt"]:
            elif command.name in [k for k in PREDICATES if PREDICATES[k] == 2]:
                fn =  globals()[command.name]
                res = fn(command.args[0], command.args[1], c.variables_dict)
            
            if not res:
                break