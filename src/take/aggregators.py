import argparse
import math

from .utils import *

def _compute_sum(aggregate_lines: 'list[str]') -> float:
    return sum(float(line[1]) for line in aggregate_lines)
def _compute_product(aggregate_lines: 'list[str]') -> float:
    return math.prod(float(line[1]) for line in aggregate_lines)
def _compute_min_max(aggregate_lines: 'list[str]', aggregate: str) -> 'tuple[float,float]':
    min_val = min(float(line[1]) for line in aggregate_lines)
    max_val = max(float(line[1]) for line in aggregate_lines)
    return min_val, max_val
def _compute_median(aggregate_lines: 'list[str]') -> float:
    values = sorted(float(line[1]) for line in aggregate_lines)
    n = len(values)
    if n % 2 == 1:
        median = values[n // 2]
    else:
        median = (values[n // 2 - 1] + values[n // 2]) / 2
    return median
def _compute_variance(aggregate_lines: 'list[str]') -> float:
    n = len(aggregate_lines)
    if n < 2:
        return 0.0
    mean = sum(float(line[1]) for line in aggregate_lines) / n
    variance = sum((float(line[1]) - mean) ** 2 for line in aggregate_lines) / (n - 1)
    return variance
def _compute_mean(aggregate_lines: 'list[str]') -> float:
    total = sum(float(line[1]) for line in aggregate_lines)
    count = len(aggregate_lines)
    res = total / count if count > 0 else 0
    return res

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
                print(f"{prefix}{_compute_sum(aggregate_lines)}")
            elif aggregate == "product":
                print(f"{prefix}{_compute_product(aggregate_lines)}")
            elif aggregate == "average" or aggregate == "mean":
                print(f"{prefix}{_compute_mean(aggregate_lines)}")
            elif aggregate == "stddev":
                print(f"{prefix}{math.sqrt(_compute_variance(aggregate_lines))}")
            elif aggregate == "variance":
                print(f"{prefix}{_compute_variance(aggregate_lines)}")
            elif aggregate == "median":
                print(f"{prefix}{_compute_median(aggregate_lines)}")
            elif aggregate == "range":
                min_val, max_val = _compute_min_max(aggregate_lines, aggregate)
                print(f"{prefix}{max_val - min_val}")
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
            elif aggregate == "summary":
                n = len(aggregate_lines)
                total = _compute_sum(aggregate_lines)
                mean = _compute_mean(aggregate_lines)
                median = _compute_median(aggregate_lines)
                variance = _compute_variance(aggregate_lines)
                std_dev = math.sqrt(variance)
                min_val, max_val = _compute_min_max(aggregate_lines, aggregate)

                print(f"{prefix}")
                print(f"Count:    {n}")
                print(f"Sum:      {total:.6f}")
                print(f"Mean:     {mean:.6f}")
                print(f"Median:   {median:.6f}")
                print(f"Std Dev:  {std_dev:.6f}")
                print(f"Min:      {min_val:.6f}")
                print(f"Max:      {max_val:.6f}")
                print(f"Range:    {max_val - min_val:.6f}")
            elif aggregate == "concat":
                res = ''.join(line[1] for line in aggregate_lines)
                print(f"{prefix}{res}")
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