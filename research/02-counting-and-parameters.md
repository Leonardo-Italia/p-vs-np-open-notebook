# Counting and parameterized complexity

**Proof drafts and exact finite checks.** [The construction note](01-alternating-target.md) defines the model. The [technical drafts](technical-drafts.md) give the full selector and comparator constructions. The supplied checker compares the carry-counting identity with exact integer subset search.

## Carries as the search variables

Write $r$ for the number of maximal constant runs in the target bits, and $\ell_i$ for their lengths. In a zero run the carry can only increase. In a one run it can only decrease. With the incoming carry fixed, a run has at most $1+\ell_i$ options. For a candidate carry vector the required graph degree at column $v$ is known:

$$
s_v=t_v+2c_{v+1}-c_v.
$$

On a cycle, label vertices $v_0,\ldots,v_{m-1}$ in cyclic order. Starting with the selection bit $b$ of one edge, propagate $x_{-1}=b$ and $x_j=s_{v_j}-x_{j-1}$. Check that all values are binary and that $x_{m-1}=b$. At most two subsets realize one carry vector. A subset determines its own carries, so summing over feasible vectors counts each subset once.

The elementary algorithm costs $O(N\prod_i(1+\ell_i))$ arithmetic operations. This is polynomial for fixed $r$ and subexponential in $N$ if $r=o(N)$. One can reduce the factor per carry vector to $O(\log N)$. The allowed carry vectors are ideals of the prerequisite relation obtained by orienting the edges between adjacent carry bits. Propagate the forced endpoint zeros, order the remaining vertices topologically, and enumerate each ideal by adding its elements in that order. Maintain currently eligible vertices in an ordered data structure. Adding or removing a carry changes the eligibility of at most two adjacent vertices. Maintain the cyclic product in a balanced tree, using

$$
M_0=\begin{pmatrix}1&0\\0&0\end{pmatrix},\quad
M_1=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
M_2=\begin{pmatrix}0&0\\0&1\end{pmatrix}.
$$

A carry change updates only the two adjacent columns. The trace of the product counts precisely the cyclic selection vectors. This gives $O(N+Q\log N)$ arithmetic operations for $Q$ arithmetically admissible carry vectors.

## Contracting intervals in both orders

For a single cycle, an interval consecutive both in bit order and in cyclic order exposes at most two carry bits and two choice bits. Tabulate its counts for each assignment to those at most four bits. If an interval is partitioned into $b$ such child intervals, the child tables share at most $b-1$ internal carries and at most $b$ internal choice edges. Contracting the child tables therefore takes $4^b\operatorname{poly}(N)$ time over the full decomposition when $b$ bounds every node's arity.

A decomposition minimizing the maximum arity can be found in polynomial time. A proper bit interval with $s$ vertices belongs to an interval of the cycle exactly when it induces $s-1$ cycle edges. Process intervals by length. For a proposed maximum arity, use a shortest path on cut positions to see whether feasible proper children tile the interval using at most that many children. The condition is monotone in the arity bound. For example, the cyclic order $m,m+1,m-1,m+2,\ldots,1,2m$ has a binary decomposition by successively extending its prefixes. All $2m$ cycle edges cross the bit cut between $m$ and $m+1$, so the example distinguishes interval decomposition from a plain left-to-right scan.

For a separate family, the technical drafts give a $2^{O(\sqrt N)}$ contraction after collapsing four-cycles, with a matching order of growth for the treewidth of the quotient graph. This is a statement about that family and that contraction.

## Exact parameterized classifications

For one cycle and parameter $r$, the decision problem is W[1]-complete and exact counting is #W[1]-complete. The hardness construction encodes a choice as the position where a carry first becomes one in a zero run. A read column with one edge fixed at zero satisfies $x+c=2d$, so both the read value and the outgoing carry equal the incoming carry. A marker with one of its edges carrying the outgoing carry exposes a second bit equal to the carry increase. These primitives implement threshold reads of the selected index and tests against the endpoints of a selected allowed pair. This gives a parsimonious construction from Multicolour Clique with $O(k^2)$ runs for $k$ colors. The [technical drafts](technical-drafts.md#parameterized-hardness-in-the-number-of-runs) give the synchronization, inequality checks and completion.

For membership, let each run choose one of its two constant states or a legal switch location. Require carries at run boundaries to agree. Add one more choice for the cycle seed $b$. The recurrence above produces integer values, and hence

$$
F=\sum_j x_j(x_j-1)+(x_{m-1}-b)^2
$$

is zero exactly for a valid subset. The propagated vector is the sum of a contribution from each run and one from $b$. Expanding $F$ gives tables of polynomially bounded integers, each depending on at most two choices. Express the sum of these tables using auxiliary variables for successive partial sums. Each auxiliary value records the indices of the table and its two partial sums, so it has a polynomial-sized domain and is uniquely determined by a valid set of choices. Binary consistency constraints enforce these records. The resulting binary CSP has $O(r^2)$ variables. Turning each variable into a color class and each compatible pair into an edge gives a parsimonious reduction to Multicolour Clique. [Jerrum and Meeks](https://eprints.gla.ac.uk/97129/1/97129.pdf) give the standard counting classification of the source problem.

The same quadratic expression gives a faster exact counting algorithm. Fix $b$, split the runs into three groups, and allocate the unary and intragroup costs to one outgoing pair of groups. Each cross-group cost is then attached to the corresponding edge of a weighted triangle. Unmatched carries disallow vertices or edges. A triangle represents a valid subset exactly when its three weights sum to zero. After shifting every edge weight by a constant $H$, encode it by the monomial $X^{w+H}$. The coefficient of $X^{3H}$ in the trace of the three matrix product counts the zero-weight triangles. Polynomial degrees and coefficient bit lengths are polynomial in $N$. [Strassen multiplication](https://deltadbu.github.io/UCAS_algorithm_course/Lectures/Lec5-Matrix-Multiplication-Strassen1969.pdf) on matrices of size at most $(N+2)^{\lceil r/3\rceil}$ yields $N^{(\log_2 7)r/3+O(1)}$ time.

## Several cycles and the ETH gap

For a disjoint union of cycles, let $F_{C,b}$ be the same penalty within cycle $C$ for seed $b$. Feasibility is equivalent to

$$
\sum_C F_{C,0}F_{C,1}=0.
$$

This expression expands into polynomially bounded tables depending on at most four run choices. The auxiliary-sum construction now proves W[1] membership for decision and #W[1] membership for the count of realizable carry vectors. The hardness reduction already has that count equal to the subset count, since its closing block pins an edge. The unrestricted subset count weights each realizable carry vector by $2^g$, where $g$ is the number of even cycles all of whose required degrees are one. For example $N/4$ four-cycles and an all-one target produce one carry vector and $2^{N/4}$ subsets. The full count is #W[1]-complete when the number of cycles is included in the parameter, by choosing one seed per cycle and summing its penalties.

The single-cycle construction also accepts arbitrary binary CSPs, with six selection blocks per domain and eight per listed relation. Applying [Marx's ETH bound for Partitioned Subgraph Isomorphism](https://toc.cs.uchicago.edu/articles/v006a005/) excludes $f(r)N^{o(r/\log(r+2))}$ time. A separate construction with multiple cycles uses one short cycle per forbidden pair and $O(k)$ runs for $k$ color classes. This gives the stronger ETH bound excluding $f(r)N^{o(r)}$ for multiple cycles. The table for the short-cycle test and a structural obstruction to merging these tests by unary threshold reads are in the [technical drafts](technical-drafts.md#linear-exponent-bound-for-multiple-cycles). The logarithmic gap for a single cycle remains open here.
