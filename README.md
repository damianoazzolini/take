# take: process file lines with a logic-based language

The goal of this tool is to filter files lines with logic-like predicates.

Why? For example, to quickly extract results from a log file of an experiment.

Each predicate takes as input at least one variable/constant with a string (the considered line) and unifies a variable with the result of the operation or succeeds/fails.


<!-- # Idea: multiple filtering stage, to compute, for example, aggregations, or an aggregation command
sum, average, stddev, min, max, count, ... -->

<!-- `split(L,",",L1)`: splits the lines L according to the delimiter , and unifies with L1 the remaining lines.  -->
<!-- In addition, each line in L1 is associated with an integer used to denote the length of the initial line -->
<!-- `select(L1,2,L2)`: select the second field from each split. The value stored in split also allows to keep track of the length -->


## Available Predicates
`lines(L)`: unifies L with the current file line. Note: each command must have `line/1` in it.
`startswith(L,P)`: true if `L` starts with `P`
`endswith(L,P)`: as `startswith/2`, but checks ends of the string
`length(L,N)`: true if `L` is of length N
`lt(L,N)`: true if `L < N`
`gt(L,N)`: true if `L > N`
`leq(L,N)`: true if `L <= N`
`geq(L,N)`: true if `L >= N`
`capitalize(L,C)`: `C` is the capitalized version of `L`, i.e., makes the first character as upper case and the rest lower case
`split_select(L,V,P,L1)`: splits `L` at each occurrence of `V` then `L1` contains the split at position `P`, starting from 0. Fails if `P` is larger than the number of splits

## Aggregation Functions
You can also aggregate the results of the applications of the predicates on the file with the option `-a/--aggregate`.
Available aggregates:
- `count`: count the lines
- `sum`
- `average`
- `min`
- `max`
- `concat`: concatenates the lines
- `unique`: filter unique lines
- `first`
- `last`

If you want only the result of the aggregation and suppress the other output, you can use the flag `-so/--suppress-output`.

You can specify multiple aggregates by repeating the flag.

## Examples

Assume the file is called `f.txt`.

Count the empty lines from a file: `take -f f.txt -c "line(L), length(L,N), lt(N,1), println(L)" -a count -so`

Assuming you have a file where the line contains results separated by spaces and you want to pick the second element of each line and sum all: `take -f f.txt -c "line(L), split_select(L,space,1,L1), println(L1)" -a sum -so`

<!-- 

I can escape startswith by doing

# i need to specify the allowed arguments directions
for instance, the second and third arguments must be ground
otherwise it does not work
split_select(L,",",2,L2)
but also, if line is 10,20,1,2
split_select(L,",",2,L2) -> L2 = 1
split_select(L,",",L2,L3) -> L3 = 20
concat(L2,L3,L4) (i.e., concat(L2,L3,"",L4)) ->  L4 = 120


ma con
split_select(L,",",E,L2), gt(E,3)


s = [...]
for i in range(len(s)):
    rem = i % split_size
    # print(rem, i)
    if rem == 1:
        print(s[i])



lines(L), length(L,N,L1), gt(N,4), startswith(L1,"v"), lt(N,7), print(L1)


se file
v0,2,6
a,v
v,6,4544

L = 
"v0,2,6"
"a,v"
"v,6,4544"

applico length(L,N,L1)
L1 = L
N = [6,3,8]

applico gt(N,4) ed L1 diventa
L1 = 
"v0,2,6"
"v,6,4544"

applico startswith(L1,"v"),
L2 = 
"v0,2,6"
"v,6,4544"

ora lt(N,7)
questo si deve riflettere su L2, quindi
L2 = 
"v0,2,6" 


lines(L), length(L,N), gt(N,4), startswith(L,"v"), lt(N,7), print(L)

line(L), length(L,3), append(L) -->