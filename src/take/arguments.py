import argparse

def parse_arguments():
    epilog = """
Available predicates (name and arity, i.e., number of arguments):
- arity 1
    - line/1
    - print/1
    - println/1
- arity 2
    - startswith/2
    - startswith_i/2
    - endswith/2
    - endswith_i/2
    - length/2
    - lt/2
    - leq/2
    - gt/2
    - geq/2
    - eq/2
    - neq/2
    - capitalize/2
    - line_number/2
    - contains/2
    - contains_i/2
    - strip/2
    - time_to_seconds/2
    - abs/2
- arity 3
    - add/3
    - sub/3
    - mul/3
    - div/3
    - pow/3
    - mod/3
- arity 4
    - split_select/4
    - replace/4
    - substring/4

Examples:
    take -f log.txt -c "line(L), print(L)" -a count
    take -f f.txt -c "line(L), split_select(L,space,1,L1), println(L1)" -a sum -so
"""
    parser = argparse.ArgumentParser(description="Process a command line with logic predicates", 
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f", "--filename", required=True, nargs="+", help="Filenames to process")
    parser.add_argument("-c", "--command", required=True, type=str, action="append", help="Command to process")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process directories recursively")
    parser.add_argument("-so", "--suppress-output", action="store_true", help="Suppress output, only show the result of the aggregation")
    parser.add_argument("-p", "--plot", action="store_true", help="Plot the results")
    parser.add_argument("-m", "--max-count", type=int, default=0, help="Maximum number of lines to process overall (0 for no limit)")
    parser.add_argument("-H", "--with-filename", action="store_true", help="Print the filename in the output lines")
    parser.add_argument("--uncolored", action="store_true", help="Disable colored output")
    parser.add_argument("--stats", action="store_true", help="Show statistics about the processed files")
    parser.add_argument("--debug", action="store_true", help="Show debug information")
    parser.add_argument("--max-columns", type=int, default=0, help="Maximum text length (0 for no limit)")
    parser.add_argument("-ks", "--keep-separated", action="store_true", help="Keep the file data separated during aggregation and plotting")
    parser.add_argument("-a", "--aggregate", action="append", choices=[
            "count",
            "sum",
            "product",
            "average",
            "mean",
            "stddev",
            "variance",
            "median",
            "min",
            "max",
            "range",
            "summary",
            "concat",
            "unique",
            "first",
            "last",
            "sort_ascending",
            "sort_descending",
            "word_count"
        ],
        help="Aggregation function to apply to the results")
    # parser.add_argument("-v", "--verbose", action="store_true",help="Enable verbose output")
    return parser.parse_args()
