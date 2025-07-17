# take: process file lines with a logic-based language

The goal of this tool is to filter files lines with a logic-like language.
That is, there are some built in predicates that applies operations on lines.

Each predicate takes as input at least one variable/constant with a string (the considered line) and unifies a variable with the result of the operation or succeeds/fails.

Why? Because I often have to write the same python script to scan log files with a lot of text and extract results having a specific structure.

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
Install `uv` and execute take like `uv run take ...` (see below the options and use the `-h` flag).


## Available Predicates
- `line(L)`: unifies L with the current file line. **Note: each command must have `line/1` in it**
- `startswith(L,P)`: true if `L` starts with `P`
- `endswith(L,P)`: as `startswith/2`, but checks ends of the string
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
- `strip(L,L1)`: removes leading and trailing whitespaces from `L` and unifies `L1` with the result
- `time_to_seconds(L,L1)`: converts a bash time of the form AmBs into seconds (example: `L = 2m42.765s` into `L1 = 162.765`)

You can also prepend `not` to predicates (except to `line/1`, `print/1`, and `println/1`) to flip the results.

## Aggregation Functions
You can also aggregate the results of the applications of the predicates on the file with the option `-a/--aggregate`.
Available aggregates:
- `count`: count the lines
- `sum`
- `product`
- `average`
- `min`
- `max`
- `concat`: concatenates the lines
- `unique`: filter unique lines
- `first`
- `last`
- `sort_ascending`
- `sort_descending`

If you want only the result of the aggregation and suppress the other output, you can use the flag `-so/--suppress-output`.

You can specify multiple aggregates by repeating the flag.

## Few Examples

Assume the file is called `f.txt`.

Count the empty lines from a file: `take -f f.txt -c "line(L), length(L,N), lt(N,1), println(L)" -a count -so`

Assuming you have a file where the line contains results separated by spaces and you want to pick the second element of each line and sum all: `take -f f.txt -c "line(L), split_select(L,space,1,L1), println(L1)" -a sum -so`
