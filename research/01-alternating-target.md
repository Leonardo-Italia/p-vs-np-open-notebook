# Subset Sum on a single cycle with an alternating target

**Proof draft.** The construction is given below. The [executable checker](../verify.py) exhausts the local tables and compares exact counts on finite instances. Independent proof review has not yet been recorded.

## Result

Label the bit positions from $0$ to $N-1$. An edge $\{i,j\}$ denotes the weight $2^i+2^j$. For even $N$, fix the target

```math
T_N=(1010\ldots10)_2=\frac{2(2^N-1)}3.
```

There is a parsimonious reduction from positive exact-one 3-SAT to Subset Sum with this target and a simple cycle as the edge graph. Each position occurs in exactly two weights, and the weights are distinct and smaller than $T_N$. The decision problem is NP-complete, and counting solutions is #P-complete. In the input to the reduction, a clause is satisfied when exactly one of its three occurrences is true. Repeated occurrences are allowed, and the variables are those appearing in the formula.

The source results are [Schaefer, *The Complexity of Satisfiability Problems*](https://doi.org/10.1145/800133.804350) for decision and [Hunt, Marathe, Radhakrishnan and Stearns, *The Complexity of Planar Counting Problems*, Corollary 3.11](https://arxiv.org/abs/cs/9809017) for counting. The construction below does not require planarity.

## The carry equation

Let $s_i$ be the number of selected incident edges at position $i$, and let $c_i$ be its incoming carry. With at most two occurrences per position, all carries are binary. The column equation is

```math
s_i+c_i=t_i+2c_{i+1}, \qquad c_0=c_N=0.
```

A column with no incident edges and target bit zero forces both carries to zero. Append such a separator to each of the following blocks. Each named wire is an edge whose two endpoints are columns. All bit patterns below are specified from least to most significant unless explicitly displayed as binary integers.

## The initial path forest

**Variable with $k$ occurrences.** Use $k$ zero columns followed by two one columns. The first zero column has the first occurrence and an internal wire $q$. Its incoming carry is zero, so the occurrence, $q$, and its outgoing carry share a value $v$. Each of the other zero columns has one occurrence wire $x$. The equation $x+c=2d$ forces $x=c=d=v$. The first one column has a wire $z$ and forces $z=1-v$ and an outgoing carry of zero. The second one column connects the other ends of $q,z$ and checks $q+z=1$. Each value of the variable determines the internal choices uniquely.

**Clause.** Use target bits $0,1$. Attach occurrence $x_1$ and an auxiliary wire $u$ to the first column, so the outgoing carry and $u$ equal $x_1$. Attach $x_2,x_3$ to the second column. Its outgoing carry is zero because of the separator, so this column checks $x_1+x_2+x_3=1$.

**Free end for $u$.** Use a three-column block with local target $6$. Connect $u$ to the least significant column and add the two internal edges of weights $5$ and $6$. For $u=0$, select the weight $6$. For $u=1$, select the weight $5$. Both extensions are unique.

An occurrence wire links the corresponding variable column and clause column. The resulting edge graph is a forest of paths. A variable occurrence has either a single endpoint on its variable side or, for its first occurrence, a three-vertex arm ending at the first one column. Each clause column connects two such arms, or one arm and the path through the free-end block. The separators are isolated vertices. Each satisfying assignment extends uniquely, and any valid subset gives a satisfying assignment.

## Alternating target and cycle completion

A block of length $k$ with local target $U$ needs a local weight sum $U+2^k d-c$ for incoming and outgoing carries $c,d$. A path such as $(0,4,3,1,2)$ gives the relative bit positions in graph order. Its internal edges contribute $2^i+2^j$ on adjacent path positions. In a connector, the two terminal edges also meet columns below the block and contribute one bit each within the block.

| Block | Path order | Local target | Unique choice for $c=d=0$ | Unique choice for $c=d=1$ |
|---|---|---:|---|---|
| Identity starting with zero | $(0,4,3,1,2)$ | 10 | $10$ | $17+24$ |
| Identity starting with one | $(0,1,3,4,5,6,2)$ | 85 | $3+10+24+48$ | $48+96+68$ |
| Six-column connector | $(0,3,2,5,1,4)$ | 21 | $9+12$ | impossible |
| Seven-column closing connector | $(0,2,3,1,5,4,6)$ | 85 | $5+80$ | impossible |

The mixed carry cases are impossible for all four blocks. The available contributions for the four rows are respectively $(17,24,10,6)$, $(3,10,24,48,96,68)$, $(1,9,12,36,34,18,16)$ and $(1,5,12,10,34,48,80,64)$. The first and last contributions in a connector belong to its terminal edges. Each table entry can be verified as the coefficient of $X^{U+2^kd-c}$ in $\prod_w(1+X^w)$. In particular both terminal edges of a connector are unselected.

Between two consecutive original columns with equal target bit, insert the odd-length identity beginning with the opposite bit. Its endpoints have the same target bit, so the expanded sequence alternates. The identity preserves the carry with a unique extension. Each identity adds a new path component to the edge graph.

Order and orient the path components, treating isolated vertices as paths with both endpoints at the same vertex. Join adjacent paths using six-column connectors above the expanded sequence, then join the last path to the first using the seven-column connector. Each six-column block starts with one and ends with zero, and the last block starts and ends with one. The original sequence starts and ends with zero, so the final target is $T_N$ with even $N$. The graph is a simple cycle and the connectors add no independent choices. Their terminal edges stay unselected in every solution.

The two highest positions are nonadjacent in the closing connector. Thus every weight is at most $2^{N-1}+2^{N-3}<T_N$ for even $N\ge6$. All constructed instances satisfy this bound. The construction has a linear number of positions and edges in the size of the formula, so the explicit binary encoding is polynomial. The bijections above prove parsimony. Membership in NP and #P follows by checking the sum of a proposed subset or counting the accepting branches of that verifier.

## Extensions in the research notebook

Under the Exponential Time Hypothesis (ETH), no uniform $`2^{o(N)}\mathop{\mathrm{poly}}\nolimits(N)`$ algorithm decides this class. The number of positions is linear in the size of the exact-one formula. To start from sparse 3-SAT, fix complementary pairs for each variable with the exact-one relation $R(x,\bar x,0)$, where a constant zero can be forced by a constant-size exact-one gadget. For a three-literal clause use three selectors with $R(p_1,p_2,p_3)$ and impose $R(p_j,\overline{\ell_j},z_j)$ for fresh slack bits. An extension exists precisely if a selector can point to a true literal. The number of added variables and clauses is linear. The [sparsification lemma of Impagliazzo, Paturi and Zane](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiZane_2001_jcss.pdf) gives the stated conditional bound.

The parity of the solution count is also $\oplus P$-complete. For this conclusion, a parsimonious source reduction is needed. The [fixed-weight verifier construction](04-fixed-weights-and-proofs.md#black-box-verifier) gives one directly from a Boolean circuit and, in the absence of free input pins, admits the same alternating completion after all constant pins are laid out in the low part.

## Reproduction

From the repository root, run `python verify.py` with Python 3.10 or newer. For this note the script checks all four local tables, the output graph and target conditions, and exact subset counts before and after the alternating completion against Boolean assignment counts. The cases include all one- and two-clause formulas on three symbols up to clause and occurrence order, plus 100 seeded formulas. These are finite checks of the construction.
