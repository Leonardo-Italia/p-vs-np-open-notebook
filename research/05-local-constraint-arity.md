# Isolated forbidden tuples in unary-degree cycles

**Working proof and executable finite checks.** This note extends the [obstruction for threshold checks](technical-drafts.md#linear-exponent-bound-for-multiple-cycles). It gives sharp bounds on the number of choices in a single forbidden tuple and the number of columns needed for the three-choice case. The last result allows degrees depending on multiple choices.

## Model

Let $D_1,\ldots,D_m$ be finite domains with at least two values each. Each column has a required degree $s_v\in\{0,1,2\}$ that is constant or depends on one variable. An assignment is accepted if binary selection bits on the edges satisfy the required degrees. On a path the entering bit is fixed and the exiting bit can be fixed or free. On a cycle all selection bits are initially free. The relation under study accepts every assignment except one designated tuple $u=(u_1,\ldots,u_m)$. There are no auxiliary domain variables.

## Paths can isolate at most two choices

**Lemma 1.** A path in this model cannot exclude just one tuple on three or more variables.

With entering bit fixed, the recurrence $x_j=s_j-x_{j-1}$ determines every successive wire even when the values cease to be binary. Each $x_j$ is an integer sum of functions of individual variables and a constant. If such a sum is binary on the full product of domains, at most one summand varies. With two varying summands, independently maximizing and minimizing them gives a range of at least two.

If propagation fails at $u$, take the first nonbinary wire. The preceding wire is binary on the full product and therefore depends on at most one variable. The current degree depends on at most one other variable, so the violation depends on at most two variables. A third variable can be changed to produce the same violation on an assignment that must be accepted. If propagation stays binary and only the fixed exit fails, the last wire depends on at most one variable and the same argument applies.

Two variables suffice with unrestricted unary degrees. Write $a,b\in\{0,1\}$ for the indicators of their designated values. With entering bit zero, the two degrees $(a,1-b)$ give wires $a,1-a-b$, which are binary exactly when $(a,b)\ne(1,1)$. Appending the degrees in reverse order returns the wire to zero on each accepted assignment, so both endpoints can be fixed.

## Cycles can isolate at most three choices

**Theorem 2.** With arbitrary unary degree functions, no disjoint union of cycles can exclude just one tuple on four or more variables. For three variables, a six-column cycle excludes just one tuple and gives exactly one selection on each accepted assignment. Six is the minimum length for a cycle realizing this relation.

For the upper bound it suffices to consider one cycle rejecting $u$, which must accept every other assignment. For an accepted assignment the total required degree is even, since it is twice the number of selected edges. This parity is also even at $u$. Choose any two variables and an alternative value for each. On the four corners formed by changing neither, one, or both of those variables, the parity values sum to zero modulo two because each column depends on at most one variable. Three corners are accepted.

If all degrees at $u$ are one, the cycle is even by the parity observation, and alternating selections accept $u$. Therefore some column has degree zero or two there. Fix the variable that controls this column at its value in $u$, if the degree is nonconstant. The column pins both incident bits, and cutting it away leaves a path with fixed ends. At least $m-1$ variables remain, and on their full product only the restricted tuple $u$ is forbidden. Lemma 1 rules out $m\ge4$.

For sharpness, let $a,b,c$ indicate membership at the three designated values. Form a six-column cycle with the cyclic degree order

$$
(a,\;1-b,\;1-a,\;b,\;1-c,\;1-c).
$$

Let $M_s[x,y]=\mathbf{1}[x+y=s]$ be the degree transfer matrix. The first four transfers multiply to $M_2$ when $a=b=1$, and to $M_0$ otherwise. The last two multiply to the identity for $c=0$ and to $M_0$ for $c=1$. The trace is zero at $(1,1,1)$ and one everywhere else. The construction applies to arbitrary domains by using the indicators as unary functions.

To prove minimality, restrict each domain to its designated value and any alternative. On this Boolean cube the total degree parity is even everywhere by the same four-corner argument. Every variable must affect at least one column. If it affected just one, that column would have degrees zero and two on the two values. For every choice of the other two variables other than their jointly designated values, both values of this sole controlling variable are accepted. Removing its column gives a path that allows both entering bits, each with its corresponding fixed exit. For the same assignment of the other two variables, degrees on that path must all be one. This follows by propagation, since both entering bits are initially possible, and a degree of one permutes them while zero or two removes one. Every value of each of the two other variables appears in a pair other than their jointly designated pair. Unarity therefore forces the path degrees to be one throughout this Boolean cube. Acceptance can then depend only on the sole controlling variable, contrary to the three-variable relation. Each of the three variables must affect at least two columns, so the cycle has length at least six.

## Consequences for combining tests

**Corollary 3.** Suppose there are $k$ disjoint triples of variables, each with one forbidden tuple. Accept all assignments that avoid the forbidden tuple in every triple. Exactly $k$ cycles are necessary and sufficient in the unrestricted unary-degree model.

Sufficiency follows by taking one six-column construction per triple. For necessity, assume fewer than $k$ cycles. While a cycle without a pinned column has a degree-zero or degree-two column at an allowed assignment, fix the triple containing its controlling variable to the values in that assignment. A constant column requires fixing no triple. The cycle now has a permanent pin. Each step fixes at most one triple and pins at least one more cycle, so some triple remains free.

Set the remaining free triples to allowed values except for one, which takes its forbidden tuple. Every pinned cycle accepts this assignment by Lemma 1, applied to the path with only this triple varied. Each unpinned cycle has degree one at every column on all remaining allowed assignments. Every value of an individual free variable occurs among those assignments. The required degrees are unary, so they are still one at the forbidden assignment. Each such cycle was even because it accepted the allowed assignments with all degrees one. It therefore accepts the forbidden assignment too, a contradiction.

For the narrower threshold model of the appendix, even an isolated forbidden **interior triple** is impossible for any number of cycles. In the argument of Theorem 2, parity forces a pin at the forbidden assignment. Fixing its controlling variable leaves at least two interior coordinates. For exactly two, the appendix's fixed-end lemma applies because a two-valued adjacent degree function cannot isolate an interior value. For three, Lemma 1 already applies.

These statements concern a direct representation on the original choices. The [one-cycle ETH gap](02-counting-and-parameters.md#several-cycles-and-the-eth-gap) remains open here. The six-column construction uses exact-value indicators. On larger ordered domains an interior singleton indicator is outside the threshold model.

## Blocks reading up to $p$ choices

**Theorem 4.** If each degree function depends on at most $p\ge1$ variables, the sharp limits are $2p$ choices for a path with a fixed entry and $3p$ for a cycle. A disjoint union of cycles has the same $3p$ limit when the relation forbids a single tuple.

For a path, restrict each variable to its designated value and one alternative. Label the designated value by one. On this Boolean cube a function of at most $p$ variables has a multilinear polynomial of degree at most $p$, by summing the indicator monomials of its local inputs. The propagated wires $x_j$ also have degree at most $p$ by the recurrence. The polynomial
$
F=\sum_j x_j(x_j-1)+(x_{\rm last}-b_{\rm out})^2
$
has degree at most $2p$ after multilinearization. Omit the last term if the exit is free. Propagation takes integer values, so $F$ is zero precisely on the accepted assignments. A function nonzero only at $(1,\ldots,1)$ is a nonzero multiple of the product of all $m$ variables in its unique multilinear representation. Thus $m\le 2p$.

For cycles, suppose $m>3p$ and choose a cycle that rejects the designated tuple. It accepts every other assignment. The parity of total required degree on the same cube has a multilinear polynomial over $\mathbb F_2$ of degree at most $p$. If the parity were one only at the forbidden tuple, it would have degree $m$. Therefore it is zero at that tuple, and there must be a column of degree zero or two there, as in Theorem 2. Fix the at most $p$ variables read by that column at their designated values. The column pins both wires, leaving a fixed-end path with more than $2p$ variables that forbids a single tuple, which is impossible.

Both bounds are attained. In the two-choice path or the six-column cycle, replace each Boolean indicator by the conjunction of $p$ indicators on a disjoint group of variables. Each degree reads at most one group, and all group indicators equal one exactly at the forbidden tuple. The six-column cycle is still parsimonious on the allowed tuples.

## Reproduction

Run `python verify.py` from the repository root. The checker exhausts all eight Boolean triples, checks the same gadget on a $3\times4\times5$ product with three interior designated values, checks all 64 Boolean assignments after replacing each indicator by a conjunction on two choices, and enumerates reachable path-transfer states on three Boolean variables through length six. The search verifies that a cycle excluding only $(1,1,1)$ first occurs at length six. The arguments above give the bounds for arbitrary finite domains and lengths.
