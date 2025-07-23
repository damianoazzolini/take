import argparse

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
    parser.add_argument("-f", "--filename", required=True, action="append", help="Filename to process")
    parser.add_argument("-c", "--command", required=True, type=str, action="append", help="Command to process")
    parser.add_argument("-so", "--suppress-output", action="store_true", help="Suppress output, only show the result of the aggregation")
    parser.add_argument("-p", "--plot", action="store_true", help="Plot the results")    
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
