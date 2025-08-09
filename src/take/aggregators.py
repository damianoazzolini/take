import argparse
import math

from .utils import *

def _compute_count(aggregate_lines: 'list[tuple[str,str]]') -> int:
    return len(aggregate_lines)

def _compute_sum(aggregate_lines: 'list[tuple[str,str]]') -> float:
    return sum(float(line[1]) for line in aggregate_lines)

def _compute_product(aggregate_lines: 'list[tuple[str,str]]') -> float:
    return math.prod(float(line[1]) for line in aggregate_lines)

def _compute_min_max(aggregate_lines: 'list[tuple[str,str]]') -> 'tuple[float,float]':
    min_val = min(float(line[1]) for line in aggregate_lines)
    max_val = max(float(line[1]) for line in aggregate_lines)
    return min_val, max_val

def _compute_average(aggregate_lines: 'list[tuple[str,str]]') -> float:
    return _compute_mean(aggregate_lines)

def _compute_mean(aggregate_lines: 'list[tuple[str,str]]') -> float:
    total = sum(float(line[1]) for line in aggregate_lines)
    count = len(aggregate_lines)
    res = total / count if count > 0 else 0
    return res

def _compute_median(aggregate_lines: 'list[tuple[str,str]]') -> float:
    values = sorted(float(line[1]) for line in aggregate_lines)
    n = len(values)
    if n % 2 == 1:
        median = values[n // 2]
    else:
        median = (values[n // 2 - 1] + values[n // 2]) / 2
    return median

def _compute_variance(aggregate_lines: 'list[tuple[str,str]]') -> float:
    n = len(aggregate_lines)
    if n < 2:
        return 0.0
    mean = sum(float(line[1]) for line in aggregate_lines) / n
    variance = sum((float(line[1]) - mean) ** 2 for line in aggregate_lines) / (n - 1)
    return variance

def _compute_stddev(aggregate_lines: 'list[tuple[str,str]]') -> float:
    return math.sqrt(_compute_variance(aggregate_lines))

def _compute_summary(aggregate_lines: 'list[tuple[str,str]]') -> str:
    n = len(aggregate_lines)
    total = _compute_sum(aggregate_lines)
    mean = _compute_mean(aggregate_lines)
    median = _compute_median(aggregate_lines)
    # variance = _compute_variance(aggregate_lines)
    std_dev = _compute_stddev(aggregate_lines)
    min_val, max_val = _compute_min_max(aggregate_lines)
    res = "\nCount:    " + str(n) + \
          "\nSum:      " + str(total) + \
          "\nMean:     " + str(mean) + \
          "\nMedian:   " + str(median) + \
          "\nStd Dev:  " + str(std_dev) + \
          "\nMin:      " + str(min_val) + \
          "\nMax:      " + str(max_val) + \
          "\nRange:    " + str(max_val - min_val)
    return res

def _compute_concat(aggregate_lines: 'list[tuple[str,str]]') -> str:
    return ' '.join(line[1] for line in aggregate_lines)

def _compute_word_count(aggregate_lines: 'list[tuple[str,str]]') -> int:
    return sum(len(line[1].split()) for line in aggregate_lines)

def apply_aggregation_function(aggregate_lines : 'list[tuple[str,str]]', args : argparse.Namespace) -> 'list[str] | list[float]':
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
            print(f"{get_warning_prefix(args.uncolored)} No lines to aggregate")
            return []
        try:
            if aggregate == "min" or aggregate == "max":
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
                res =  globals()[f"_compute_{aggregate}"](aggregate_lines)
                print(f"{prefix}{res}")
        except Exception as e:
            print(f"\n{get_error_prefix(args.uncolored)} Error applying aggregation function '{aggregate}': {e}")

    return obtained_data