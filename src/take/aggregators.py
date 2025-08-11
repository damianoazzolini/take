import argparse
import math

from .utils import wrap_sort, get_aggregate_prefix, get_warning_prefix, get_error_prefix

def _compute_sum_prod_count(sum_or_count_or_prod : str, aggregate_lines: 'list[tuple[str,str]]', filename : str | None = None) -> 'int | float':
    if sum_or_count_or_prod == "prod":
        result : float = 1
    else:
        result : float = 0
    
    for line in aggregate_lines:
        if filename is not None:
            if line[0] == filename:
                if sum_or_count_or_prod in ["prod", "sum"]:
                    val = float(line[1])
                else:
                    val = 1 # for count
            else:
                val = 1 if sum_or_count_or_prod == "prod" else 0
        else:
            val = float(line[1])
        if sum_or_count_or_prod == "sum":
            result += val
        elif sum_or_count_or_prod == "count":
            result += 1
        elif sum_or_count_or_prod == "prod":
            result *= val
            if result == 0:
                break # I can stop here
    return result

def _compute_count(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'int | float':
    return _compute_sum_prod_count("count", aggregate_lines, filename)

def _compute_sum(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'int | float':
    return _compute_sum_prod_count("sum", aggregate_lines, filename)

def _compute_product(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'int | float':
    return _compute_sum_prod_count("prod", aggregate_lines, filename)

def _compute_min_or_max(min_or_max : str, aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'int | float':
    fn = min if min_or_max == "min" else max
    if filename is not None:
        return fn(float(line[1]) for line in aggregate_lines if line[0] == filename)
    return fn(float(line[1]) for line in aggregate_lines)

def _compute_min(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'int | float':
    return _compute_min_or_max("min", aggregate_lines, filename)

def _compute_max(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'int | float':
    return _compute_min_or_max("max", aggregate_lines, filename)

def _compute_range(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'int | float':
    min_val = _compute_min(aggregate_lines, filename)
    max_val = _compute_max(aggregate_lines, filename)
    return max_val - min_val

def _compute_mean(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> float:
    if filename is not None:
        total = sum(float(line[1]) for line in aggregate_lines if line[0] == filename)
        count = sum(1 for line in aggregate_lines if line[0] == filename)
    else:
        total = sum(float(line[1]) for line in aggregate_lines)
        count = len(aggregate_lines)
    res = total / count if count > 0 else 0
    return res

def _compute_average(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> float:
    return _compute_mean(aggregate_lines, filename)

def _compute_median(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> float:
    if filename is not None:
        values = sorted(float(line[1]) for line in aggregate_lines if line[0] == filename)
        n = sum(1 for line in aggregate_lines if line[0] == filename)
    else:
        values = sorted(float(line[1]) for line in aggregate_lines)
        n = len(values)
    if n % 2 == 1:
        median = values[n // 2]
    else:
        median = (values[n // 2 - 1] + values[n // 2]) / 2
    return median

def _compute_variance(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> float:
    if filename is not None:
        n = sum(1 for line in aggregate_lines if line[0] == filename)
    else:
        n = len(aggregate_lines)
    if n < 2:
        return 0.0
    mean = _compute_mean(aggregate_lines, filename)
    if filename is not None:
        variance = sum((float(line[1]) - mean) ** 2 for line in aggregate_lines if line[0] == filename) / (n - 1)
    else:
        variance = sum((float(line[1]) - mean) ** 2 for line in aggregate_lines) / (n - 1)
    return variance

def _compute_stddev(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> float:
    return math.sqrt(_compute_variance(aggregate_lines, filename))

def _compute_summary(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> str:
    n = _compute_count(aggregate_lines, filename)
    total = _compute_sum(aggregate_lines, filename)
    mean = _compute_mean(aggregate_lines, filename)
    median = _compute_median(aggregate_lines, filename)
    # variance = _compute_variance(aggregate_lines)
    std_dev = _compute_stddev(aggregate_lines, filename)
    min_val = _compute_min(aggregate_lines, filename)
    max_val = _compute_max(aggregate_lines, filename)
    res = "\nCount:    " + str(n) + \
          "\nSum:      " + str(total) + \
          "\nMean:     " + str(mean) + \
          "\nMedian:   " + str(median) + \
          "\nStd Dev:  " + str(std_dev) + \
          "\nMin:      " + str(min_val) + \
          "\nMax:      " + str(max_val) + \
          "\nRange:    " + str(max_val - min_val)
    return res

def _compute_concat(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> str:
    if filename is not None:
        return ''.join(line[1] for line in aggregate_lines if line[0] == filename)
    return ''.join(line[1] for line in aggregate_lines)

def _compute_word_count(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> int:
    if filename is not None:
        return sum(len(line[1].split()) for line in aggregate_lines if line[0] == filename)
    return sum(len(line[1].split()) for line in aggregate_lines)

def _compute_unique(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> set[str]:
    if filename is not None:
        return set(line[1].rstrip() for line in aggregate_lines if line[0] == filename)
    return set(line[1].rstrip() for line in aggregate_lines)

def _compute_first_last(first_or_last : str, aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> str:
    idx = 0 if first_or_last == "first" else -1

    if filename is None:
        return aggregate_lines[idx][1].rstrip()
    
    # filename is not none
    lines = aggregate_lines if first_or_last == "first" else reversed(aggregate_lines)
    for line in lines:
        if line[0] == filename:
            return line[1].rstrip()
    return "-"

def _compute_first(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> str:
    return _compute_first_last("first", aggregate_lines, filename)

def _compute_last(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> str:
    return _compute_first_last("last", aggregate_lines, filename)

def _compute_sort_ascending_descending(ascending : bool, aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'str':
    sorted_lines = wrap_sort(aggregate_lines, filename, reverse=not ascending)
    return '\n' + '\n'.join([str(line) for line in sorted_lines])

def _compute_sort_ascending(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'str':
    return _compute_sort_ascending_descending(True, aggregate_lines, filename)

def _compute_sort_descending(aggregate_lines: 'list[tuple[str,str]]', filename : str | None) -> 'str':
    return _compute_sort_ascending_descending(False, aggregate_lines, filename)

def apply_aggregation_function(aggregate_lines : 'list[tuple[str,str]]', args : argparse.Namespace) -> 'list[str] | list[float]':
    """
    Apply the aggregate function.
    """
    # check aggregation function
    obtained_data : 'list[str] | list[float]' = []
    for aggregate in args.aggregate:
        prefix = get_aggregate_prefix(aggregate, args.uncolored)
        if len(aggregate_lines) == 0:
            print(f"{get_warning_prefix(args.uncolored)} No lines to aggregate")
            return []
        try:
            # TODO: if keep separated, loop through all the files: not super efficient
            # because I loop multiple times, but compact
            if args.keep_separated:
                files_with_data = set(line[0] for line in aggregate_lines)
                for filename in args.filename:
                    if filename in files_with_data:
                        res =  globals()[f"_compute_{aggregate}"](aggregate_lines, filename)
                    else:
                        res = "-"
                    print(f"{get_aggregate_prefix(aggregate + ' ' + filename, args.uncolored)} {res}")
            else:
                res =  globals()[f"_compute_{aggregate}"](aggregate_lines, None)
                if args.with_filename and aggregate in ["min", "max"]:
                    # to allow printing the file location of the min and max values
                    idxs = [line[0] for line in aggregate_lines if float(line[1]) == res]
                    s_idxs = ', '.join(idxs)
                    prefix = get_aggregate_prefix(aggregate + f" {s_idxs}", args.uncolored)
                print(f"{prefix} {res}")
        except Exception as e:
            print(f"\n{get_error_prefix(args.uncolored)} Error applying aggregation function '{aggregate}': {e}")

    return obtained_data
