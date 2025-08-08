# take: process file lines with a logic-like language

The goal of this tool is to filter files lines with a logic-like language.
That is, there are some built in predicates that applies operations on lines.
Then, the results can also be aggregated.

Each predicate takes as input at least one variable/constant with a string (the considered line) and unifies a variable with the result of the operation or succeeds/fails.

Why? Because I often have to write the same Python script to scan log files with a lot of text and extract results having a specific structure.

## Quick Examples
Assume you have a file called `log.txt` which contains something like
```
----- CV 1 ----- 
Train on: f2,f3,f4,f5, Test on: f1
AUCPR1:  0.720441984486102
AUCROC1: 0.735
LL1: -12.753700137597306

----- CV 2 ----- 
Train on: f1,f3,f4,f5, Test on: f2
AUCPR2:  0.9423737373737374
AUCROC2: 0.94
LL2: -7.4546895016487245

----- CV 3 ----- 
Train on: f1,f2,f4,f5, Test on: f3
AUCPR3:  0.7111492673992674
AUCROC3: 0.71
LL3: -11.836606612796992

----- CV 4 ----- 
Train on: f1,f2,f3,f5, Test on: f4
AUCPR4:  0.9536004273504273
AUCROC4: 0.95
LL4: -6.458126608595575

----- CV 5 ----- 
Train on: f1,f2,f3,f4, Test on: f5
AUCPR:  0.6554753579753579
AUCROC: 0.765
LL5: -12.149458117122595
```
and you want to extract the `AUCPR` results and average them.
With `take` you can quickly do so:
```
take -f log.txt -c "line(L), startswith(L,'AUCPR'), split_select(L,':',1,L1), strip(L1,L2), println(L2)" -a average
```
Output
```
0.720441984486102
0.9423737373737374
0.7111492673992674
0.9536004273504273
0.6554753579753579
[average] 0.7966081549169783
```

Another example: extract the `real` value of the bash time and convert it into seconds.
Suppose you have a file `log.txt` of the form
```
Started at: 
size 7
[RESULT]                   [4. 4.]
real	0m8.853s
user	0m8.231s
sys	0m0.110s

size 8
[RESULT]                    [4. 4.]
real	0m31.248s
user	0m30.784s
sys	0m0.177s

size 9
[RESULT]                    [4. 4.]
real	2m42.765s
user	2m41.007s
sys	0m1.205s
```

To do so:
```
take -f log.txt -c "line(L), startswith(L,'real'), split_select(L,tab,1,T), time_to_seconds(T,TS), println(TS)"
```
Output
```
8.853
31.248
162.765
```

## Installation
Install [`uv`](https://docs.astral.sh/uv/), clone the repo, and run
```
uv pip install .
```
If you want to edit the project, add the `-e` flag after `install`.


## Quick Description and Available Predicates
Variables start with an uppercase letter while constants starts with a lowercase letter, are numbers, or are enclosed within single quotes.
The execution idea is simple: each command starts with a `line/1` predicate which assigns its argument to the content of the current file line (for instance `line(L)` assigns `L` to the content of the current line, since `L` is a variable. If `L` is a constant, it checks whether the current line is equal to the constant).
Then, iteratively, it applies subsequent commands, in order of appearance, until failure.
To print results, you can use the `print/1` or `println/1`.

Available predicates:
- `line(L)`: unifies `L` with the current file line. **Note: each command must have `line/1` in it**
- `print(L)/println(L)`: print the content of `L` (`println/1` also adds a newline)
- `startswith(L,P)`: true if `L` starts with `P`
- `startswith_i(L,P)`: true if `L` starts with `P`, case insensitive
- `endswith(L,P)`: as `startswith/2`, but checks ends of the string
- `endswith_i(L,P)`: as `startswith/2`, but checks ends of the string, case insensitive
- `length(L,N)`: true if `L` is of length `N`
- `lt(L,N)`: true if `L < N`
- `gt(L,N)`: true if `L > N`
- `leq(L,N)`: true if `L <= N`
- `geq(L,N)`: true if `L >= N`
- `eq(L,N)`: true if `L == N`
- `neq(L,N)`: true if `L != N`
- `capitalize(L,C)`: `C` is the capitalized version of `L`, i.e., makes the first character as upper case and the rest lower case
- `split_select(L,V,P,L1)`: splits `L` at each occurrence of `V` then `L1` contains the split at position `P`, starting from 0. Fails if `P` is larger than the number of splits. Special split delimiters: `V = space` and `V = tab`
- `replace(L,A,B,L1)`: replace the occurrences of the string `A` in L with `B` and unifies `L1` with the results
- `contains(L,A)`: true if the string unified with `L` contains the string unified with `A`, false otherwise
- `contains_i(L,A)`: true if the string unified with `L` contains the string unified with `A`, false otherwise, case insensitive
- `strip(L,L1)`: removes leading and trailing whitespaces from `L` and unifies `L1` with the result
- `time_to_seconds(L,L1)`: converts a bash time of the form AmBs into seconds (example: `L = 2m42.765s` into `L1 = 162.765`)
- `add(A,B,C)`: `C` is the result of `A + B`
- `sub(A,B,C)`: `C` is the result of `A - B`
- `mul(A,B,C)`: `C` is the result of `A * B`
- `div(A,B,C)`: `C` is the result of `A - B`
- `pow(A,B,C)`: `C` is the result of `A**B`
- `mod(A,B,C)`: `C` is the result of `A % B`
- `abs(A,B)`: `B` is `|A|`
- `substring(S,Start,End,ST)`: `ST` is the substring of `S` from position `Start` (included) to position `End` (excluded) 

You can also prepend `not` to predicates (except to `line/1`, `print/1`, and `println/1`) to flip the result.

You can pass arguments as strings by enclosing them into single quotes (e.g., `'Hello'` will be treated as a string and not as a variable).

## Aggregation Functions
You can also aggregate the results of the applications of the predicates on the file with the option `-a/--aggregate`.

Available aggregates (some are self-explanatory):
- `count`: counts the lines
- `sum`
- `product`
- `average` or `mean`
- `stddev`
- `variance`
- `min`
- `max`
- `range`: max value - min value
- `summary`: computes summary statistics (count, sum, mean, median, std dev, min, max, and range)
- `concat`: concatenates the lines
- `unique`: filters unique lines
- `first`
- `last`
- `sort_ascending`
- `sort_descending`
- `median`
- `word_count`

If you want only the result of the aggregation and suppress the other output, you can use the flag `-so/--suppress-output`.

You can specify multiple aggregates by repeating the flag.

## Few Examples

Assume the file is called `f.txt`.

Count the empty lines from a file: `take -f f.txt -c "line(L), length(L,N), lt(N,1), println(L)" -a count -so`

Assuming you have a file where the line contains results separated by spaces and you want to pick the second element of each line and sum all: `take -f f.txt -c "line(L), split_select(L,space,1,L1), println(L1)" -a sum -so`

## Benchmarking
We run a small experimental evaluation to benchmark the tool.
We considered files called `stress_N.txt` with `N` lines of the form `Iteration IT: R, data` where `R` is a random number.
The goal is to extract all the values of `R` and compute statistics on them, so we run the command
```
take -f stress_N.txt -c "line(L), split_select(L, space, 2, L1), replace(L1, ',', '',L2), println(L2)" -a summary -H -so
```
We consider 10 runs of the same command computed with [`multitime`](https://github.com/ltratt/multitime).
Overall, we run `multitime -n 10 take -f stress_N.txt -c "line(L), split_select(L, space, 2, L1), replace(L1, ',', '',L2), println(L2)" -a summary -H -so`.

Results:
```
N = 100 (size 4.2K)
            Mean                Std.Dev.    Min         Median      Max
real        0.476+/-0.0234      0.023       0.445       0.465       0.516       
user        2.245+/-0.0715      0.071       2.108       2.243       2.369       
sys         0.075+/-0.0152      0.015       0.051       0.074       0.099    

N = 1_000 (size 42K)
            Mean                Std.Dev.    Min         Median      Max
real        0.475+/-0.0240      0.024       0.445       0.474       0.515       
user        2.283+/-0.1124      0.112       2.080       2.296       2.479       
sys         0.086+/-0.0300      0.030       0.052       0.076       0.134   

N = 10_000 (size 419K)
            Mean                Std.Dev.    Min         Median      Max
real        0.593+/-0.0176      0.018       0.566       0.595       0.618       
user        2.421+/-0.1013      0.101       2.213       2.443       2.592       
sys         0.092+/-0.0253      0.025       0.052       0.092       0.127  

N = 100_000 (size 4.1M)
            Mean                Std.Dev.    Min         Median      Max
real        1.942+/-0.1521      0.152       1.668       1.981       2.148       
user        3.750+/-0.1404      0.140       3.449       3.768       3.915       
sys         0.104+/-0.0297      0.030       0.057       0.107       0.155  

N = 1_000_000 (size 41M)
            Mean                Std.Dev.    Min         Median      Max
real        14.054+/-1.1232      1.121       12.893      13.547      16.527      
user        15.702+/-1.0858      1.083       14.650      15.145      17.965      
sys         0.225+/-0.0231      0.023       0.182       0.232       0.258   
```


## Contributing
Suggestions, issues, pull requests, etc, are welcome.

## Disclaimer
The program is provided as it is and it main contain bugs.