import argparse
import math

from .utils import *

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
            if args.uncolored:
                print("[WARNING]:", end=' ')
            else:
                print(f"{bcolors.WARNING}[WARNING]{bcolors.ENDC}:", end=' ')
            print("No lines to aggregate")
            return []
        try:
            if aggregate == "count":
                print(f"{prefix}{len(aggregate_lines)}")
            elif aggregate == "sum":
                total = sum(float(line[1]) for line in aggregate_lines)
                print(f"{prefix}{total}")
            elif aggregate == "product":
                total = math.prod(float(line[1]) for line in aggregate_lines)
                print(f"{prefix}{total}")
            elif aggregate == "average":
                total = sum(float(line[1]) for line in aggregate_lines)
                count = len(aggregate_lines)
                res = total / count if count > 0 else 0
                print(f"{prefix}{res}")
            elif aggregate == "stddev":
                n = len(aggregate_lines)
                if n < 2:
                    print(f"{prefix}0.0")
                else:
                    mean = sum(float(line[1]) for line in aggregate_lines) / n
                    variance = sum((float(line[1]) - mean) ** 2 for line in aggregate_lines) / (n - 1)
                    stddev = math.sqrt(variance)
                    print(f"{prefix}{stddev}")
            elif aggregate == "variance":
                n = len(aggregate_lines)
                if n < 2:
                    print(f"{prefix}0.0")
                else:
                    mean = sum(float(line[1]) for line in aggregate_lines) / n
                    variance = sum((float(line[1]) - mean) ** 2 for line in aggregate_lines) / (n - 1)
                    print(f"{prefix}{variance}")
            elif aggregate == "min" or aggregate == "max":
                fn = min if aggregate == "min" else max
                res = fn(float(line[1]) for line in aggregate_lines)
                print(f"{prefix}", end='')
                if args.with_filename:
                    idxs = [line[0] for line in aggregate_lines if float(line[1]) == res]
                    s_idxs = ', '.join(idxs)
                    if not args.uncolored:
                        print(f"{bcolors.PURPLE}{s_idxs}:{bcolors.ENDC}", end='')
                    else:
                        print(f"{s_idxs}:", end='')
                print(f"{res}")
            elif aggregate == "concat":
                res = ''.join(line[1] for line in aggregate_lines)
                print(f"{prefix}{res}")
            elif aggregate == "median":
                values = sorted(float(line[1]) for line in aggregate_lines)
                n = len(values)
                if n % 2 == 1:
                    median = values[n // 2]
                else:
                    median = (values[n // 2 - 1] + values[n // 2]) / 2
                print(f"{prefix}{median}")
            elif aggregate == "word_count":
                total_words = sum(len(line[1].split()) for line in aggregate_lines)
                print(f"{prefix}{total_words}")
            # elif aggregate == "join": # TODO: with a separator
            #     print(', '.join(aggregate_lines))
            elif aggregate == "unique":
                unique_lines = set(line[1].rstrip() for line in aggregate_lines)
                obtained_data = list(unique_lines)
                print(f"{prefix}")
                if args.with_filename:
                    for d in obtained_data:
                        # print(d)
                        idxs = [line[0] for line in aggregate_lines if line[1].rstrip() == d]
                        s_idxs = ', '.join(idxs)
                        # print(s_idxs, end=': ')
                        if not args.uncolored:
                            print(f"{bcolors.PURPLE}{s_idxs}:{bcolors.ENDC} ", end='')
                        else:
                            print(f"{s_idxs}: ", end='')
                        print(d.strip())
                else:
                    res = '\n'.join(unique_lines)
                    print(f"{prefix}{res}")
            elif aggregate == "first" or aggregate == "last":
                idx = 0 if aggregate == "first" else -1
                res = aggregate_lines[idx]
                print(f"{prefix}", end='')
                if args.filename:
                    if not args.uncolored:
                        print(f"{bcolors.PURPLE}{res[0]}:{bcolors.ENDC}", end='')
                    else:
                        print(f"{res[0]}:", end='')
                print(f"{res[1].strip()}")
            elif aggregate == "sort_ascending" or aggregate == "sort_descending":
                reverse = aggregate == "sort_descending"
                sorted_lines = wrap_sort(aggregate_lines, reverse=reverse)
                obtained_data = sorted_lines
                print(f"{prefix}")
                for s in sorted_lines:
                    if args.with_filename:
                        if not args.uncolored:
                            print(f"{bcolors.PURPLE}{s[0]}:{bcolors.ENDC}", end='')
                        else:
                            print(f"{s[0]}:", end='')
                    print(s[1])
            else:
                print(f"Unknown aggregation function: {aggregate}")
        except Exception as e:
            print("")
            if args.uncolored:
                print("[ERROR]:", end=' ')
            else:
                print(f"{bcolors.ERROR}[ERROR]{bcolors.ENDC}:", end=' ')
            print(f"Error applying aggregation function '{aggregate}': {e}")
            obtained_data = []

    return obtained_data