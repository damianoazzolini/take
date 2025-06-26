
# each predicate working on a line takes as input a line and outputs a line,
# so it is not possible to obtain a list of lines starting from a line (say, with split)

# Idea: multiple filtering stage, to compute, for example, aggregations, or an aggregation command
sum, average, stddev, min, max, count, ...

`lines(L)`: unifies L with the file lines
`startswith(L,a)`: true if L starts with the specified pattern (a)
`endswith(L,a)`: true if L ends with the specified pattern (a)
`length(L,N)`: true if the line is of length N

<!-- `split(L,",",L1)`: splits the lines L according to the delimiter , and unifies with L1 the remaining lines.  -->
<!-- In addition, each line in L1 is associated with an integer used to denote the length of the initial line -->
<!-- `select(L1,2,L2)`: select the second field from each split. The value stored in split also allows to keep track of the length -->


# Available Predicates

`startswith(L,S)`: checks whether the string in `L` starts with with teh string `S`

<!-- maybe split and select only in one step? -->
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

line(L), length(L,3), append(L)