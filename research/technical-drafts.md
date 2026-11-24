# Supporting technical drafts

This appendix contains the extended derivations for the notes on [counting](02-counting-and-parameters.md), [matchgates](03-matchgate-representations.md), and [circuit lower bounds](04-fixed-weights-and-proofs.md). Test counts in individual sections refer to checks performed during the investigation. The [README](../README.md) identifies the checks reproducible with this release.

These are working arguments developed with ChatGPT/Codex. Independent review remains to be documented.

## Contracting cycles of selection edges

Let $s=2k$, $a=2s+1$, and $N=a^2-1$. Each weight is $2^i+2^{f(i)}$, where $f(i)=ai+s\bmod N$. The permutation satisfies $f^2(i)=i+N/2\bmod N$, so the selection edges form four-cycles. Contract the selection edges of each cycle and leave its carry ports exposed.

The quotient graph has treewidth $\Theta(\sqrt N)$. The orbits of $x+ay$, for $0\le x,y<s$, are distinct. Indeed, $f(x+ay)=y+ax+s\bmod N$, $f^2$ adds $N/2$, and none of the other three images returns to the initial square. Unit steps are carry edges. Steps of length $a$ become carry edges under $f^{-1}$, since $f(i+1)=f(i)+a$. This gives an $s\times s$ grid without using a wraparound carry from $N-1$ to $0$. The crosses formed by a row and a column are connected and pairwise intersecting. Any set meeting every cross has at least $s$ vertices. By the Helly property for subtrees, some bag of any tree decomposition must meet every cross.

For the upper bound, every orbit preserves its residue modulo $s$. Each layer has $s+1$ orbits, and the carries connect successive layers. A path decomposition can keep the first layer and two consecutive layers at each step. This gives an exact count in $2^{O(\sqrt N)}$ time for the family. Enumerate each layer's choices, determine its two carry vectors, and join the layers. The grid construction was checked for $k$ from 1 through 14. The count was compared with meet-in-the-middle enumeration on 25 targets of 24 columns.

## Sums with cancellation

A block is the signature obtained by contracting its internal carries and leaving the selection ports open. Repeat the four-column block with target bits $(0,0,1,0)$ in least-significant-first order. Fix both selection bits of the last column to zero, which forces its incoming and outgoing carries to zero. Leave four inputs of weights $1,1,2,4$ active in the first three columns. With both boundary carries zero, the target $4$ admits exactly two selections: the weight $4$ alone, or the other three weights. Flipping the bit of the weight $4$ reduces this block to $M=|0000\rangle+|1111\rangle$. Repeating it $r$ times gives $M^{\otimes r}$.

Pinning and flipping bits preserve matchgate identities. A Gaussian-rank lower bound for this restricted vector therefore bounds the number of terms in a sum for the arithmetic block in the original basis, with a common port order. With Clifford operators of degree at most $p$ and the same parity as $p$, one Gaussian signature generates a space of dimension at most $C_{4r,p}=\sum_{j\le p,\,j\equiv p\pmod 2}\binom{4r}{j}$. A sum of $h$ signatures generates dimension at most $hC_{4r,p}$.

On each copy of $M$, choose one degree-zero vector, eight degree-one vectors, and seven degree-two vectors with distinct pivot supports. The operators are the identity, creation or annihilation on one mode, double creation on a pair, and a projection using the number operator. Interleaving the ports introduces signs while preserving the supports. Each combination of exact degree $p$ has a unique pivot. On copies where the identity acts, use $0000$ as the pivot. A term can replace it by $1111$, whose pivot would require two additional degrees. This gives at least $[z^p](1+8z+7z^2)^r$ independent vectors. For $p=\lfloor 8r/9\rfloor$ the ratio is of order $(343/243)^r$. The bound permits negative or complex coefficients.

The arithmetic restriction is developed here. References for the signature characterization and rank estimates are listed below.

- [Cai and Gorenstein, *Matchgates Revisited*](https://theoryofcomputing.org/articles/v010a007/), Sections 2 and 5, for identities and Pfaffian normalization.
- [Wei, Wu, Liu and Liu, *Robust exponential lower bounds for fermionic and bosonic Gaussian ranks*](https://arxiv.org/abs/2610.02172), preprint, Proposition 3 and Appendix B.1, for Gaussian rank and the asymptotic ratio.
- [Reardon-Smith, *Exponential lower bounds on the fermionic Gaussian rank of magic states*](https://arxiv.org/abs/2610.03699), independent preprint, for the same fermionic-vector obstruction.

## Individual-port changes of basis

A Hadamard on each of the four ports maps $M$ to the uniform even-parity signature, which is a matchgate. To test the full chain, use three active columns with target $(0,0,1)$ and expose all six ports of weights $1,1,2,2,4,4$. Let $S$ denote the selected sum in a block. The common terminal order follows the column order, and the two ports of each column are adjacent.

Under uniform Hadamards, pin the two ports of each zero-target separator to transformed bits $0$ and $1$. In the original coordinates the resulting rows are $(1,1)$ and $(1,-1)$, up to normalization. The carry matrix is $K=|0\rangle(\langle0|-\langle1|)$. Use a separator on both sides of each block, shared between consecutive blocks, and fix the exterior carries to zero. The result is a tensor product of blocks $\psi=H^{\otimes6}(\mathbf 1[S=4]-\mathbf 1[S=3])$, up to a nonzero scalar. Indeed, the relation is $S+c=4+8d$, with outgoing carry $d=0$ and opposite signs for the two values of the incoming carry $c$.

For arbitrary invertible single-port bases, a four-column separator with target $(0,0,1,1)$ pins both boundary carries to zero. In the original coordinates a cap with coefficients $q_{ab}$ induces
$$
K_0(q)=\begin{pmatrix}q_{00}&q_{11}\\0&q_{01}+q_{10}\end{pmatrix},
\qquad
K_1(q)=\begin{pmatrix}q_{01}+q_{10}&0\\q_{00}&q_{11}\end{pmatrix}.
$$
The two parity planes in the transformed coordinates correspond to complementary planes in the original coordinates. For the first $K_0$ impose $q_{01}+q_{10}=0$, and for the last $K_1$ impose $q_{11}=0$. Each condition intersects each of the two planes in dimension at least one. The common kernel of the two maps $K_t$ is a line, so at least one intersection gives a nonzero matrix. The first matrix then has only row $0$ nonzero, and the last matrix has only column $0$ nonzero. In the two middle columns, the four computational projections span the upper and lower triangular matrix spaces, respectively. The products of the two spaces span all $2\times2$ matrices. Thus some pair of projections makes the overall product a nonzero multiple of $|0\rangle\langle0|$. The caps have definite parity in the transformed coordinates and are matchgate signatures on two adjacent terminals. Planar composition preserves the upper bound on the number of terms in a sum.

The four-column separator isolates blocks $\psi=(G_1\otimes\cdots\otimes G_6)\mathbf 1[S=4]$. One useful example applies unnormalized Hadamards on ports $3,5,6$, counted from $1$, and identities on the others. This is a choice for the active block and is independent of the separator bases.

## Rank certificate

For a six-mode block, consider the spans of the even-degree Clifford words through degrees $d=0,2,4$. Uniform Hadamards with single-column separators and the example for the four-column separator both give ranks $1,53,64$ modulo $1009$. Work with integer coefficients and unnormalized Hadamards. Enumerate words with $0,2,4$ distinct indices in increasing order from $0,\dots,11$, and accumulate the resulting vector columns by increasing degree. With Pauli matrices $X,Z$, use generators $(Z_0\cdots Z_{j-1})X_j$ and $(Z_0\cdots Z_j)X_j$ for $j=0,\dots,5$. The latter differs from the corresponding Majorana by a phase. Gaussian elimination modulo $1009$ certifies nonzero minors in characteristic zero. All $64$ coefficients for the uniform separator were checked with integer arithmetic. The general separator was also checked in one hundred examples with invertible integer matrices.

For a matchgate on $n$ modes the span of all Clifford words of degree at most $d$ has dimension at most $\sum_{j\le d}\binom nj$. A Gaussian transformation takes the matchgate to the vacuum, on which pure creation words suffice. A sum of $R$ matchgates increases the bound by at most a factor of $R$. In each of $r$ contiguous blocks, choose $1$, $52$, and $11$ new independent vectors of costs $0,2,4$, respectively. Even words act locally because the preceding Jordan–Wigner strings cancel. Multiply the bounds for each cumulative degree by $z^d$ and sum over $d\ge0$. Cancelling the factor $1/(1-z)$ gives
$$
R\ge \left(\frac{1+52z^2+11z^4}{(1+z)^6}\right)^r
\qquad(0<z<1).
$$
At $z=1/2$ the ratio is $940/729$, proving the exponential bound for uniform Hadamards. In the four-column-separator construction the witnessing minors at degrees $2$ and $4$ are polynomials in the entries of the six bases. They are nonzero in the example, so the bound holds for generic local bases outside a proper algebraic set. If only $g$ blocks satisfy the minor condition, pin the others to nonzero coefficients to get $(940/729)^g$. The bound permits signed and complex coefficients.

See [Bravyi, *Contraction of matchgate tensor networks on non-planar graphs*](https://arxiv.org/abs/0801.2989) for planar composition, and Proposition 3 and Lemma 13 in the Wei et al. preprint for the Majorana filtration. The separators, blocks, and rank calculations are part of this investigation.

## Uniform bound for all local bases

For the same family with four-column separators, an exponential bound also holds in the exceptional bases. It applies to arbitrary invertible complex matrices on individual ports and the common natural terminal order, with the six ports in each block contiguous. After postselecting the separators, write $\phi$ for a transformed block.

### A block invariant

Cut the coefficient matrix of $\mathbf 1[S=4]$ after the third port. The weights on the two sides are $(1,1,2)$ and $(2,4,4)$. The only pairs of partial sums are $(0,4),(2,2),(4,0)$. Each gives a rank-one summand and the three have disjoint row and column supports. The matrix has rank three. Invertible local matrices act by invertible row and column transformations, so every $\phi$ has rank three across this cut.

### From cut rank to the first Majorana span

Let $D_1(\phi)=\dim\operatorname{span}\{\phi,\gamma_1\phi,\dots,\gamma_{2n}\phi\}$ for $n$ modes and Majorana operators $\gamma_i$. Let $K$ be the kernel of $(a,v)\mapsto(aI+v)\phi$, with $v$ a linear combination of Majoranas. For $(a,v),(b,w)\in K$, the identity $\{v,w\}\phi=2ab\phi$ implies that $K$ is isotropic for $v\cdot w-ab$. Thus $\dim K\le n$.

If $\dim K=n$, flip bits to make the vacuum coefficient nonzero and normalize it to $1$. This preserves $D_1$ and the matrix rank across the cut. In exterior coordinates, with creation $x_j\wedge$ and annihilation $\partial_j$, project $K$ onto the annihilation coefficients. The projection is injective. In the kernel of the projection, the degree-zero equation forces the scalar to vanish, and the degree-one equation forces the creation coefficients to vanish. Since both spaces have dimension $n$, the projection is an isomorphism. The annihilation equations can therefore be written
$$
\left(a_i+\partial_i+\sum_j B_{ij}x_j\wedge\right)\phi=0,\qquad
B_{ij}+B_{ji}=2a_i a_j .
$$
The solution with constant coefficient $1$ is $\phi=(1+\ell)\exp Q$, with $\ell=-\sum_i a_i x_i$ and the skew matrix of $Q$ given by $a_i a_j-B_{ij}$. Exterior differentiation verifies it. For uniqueness, the first nonzero homogeneous component of the difference of two solutions would be annihilated by every $\partial_i$.

This form has power-of-two rank across any consecutive cut. Eliminate the internal terms of $Q$ by invertible local exterior exponentials. Change variables separately on the two sides to make its cross part $\sum_{i=1}^k x_i y_i$. On the $k$ paired modes per side, the matrix of $\exp Q$ is diagonal and invertible, with sign $(-1)^{s(s-1)/2}$ at degree $s$. Dividing by that diagonal makes the principal block of $(1+\ell)\exp Q$ equal to $I+C$, with $C$ a linear combination of creation and annihilation operators on $k$ modes. For the right component of $\ell$, the parity sign from the left variables cancels the ratio of the diagonal signs in consecutive degrees. Its operators thus become annihilation with the usual fermionic signs. We have $C^2=\lambda I$ and $\operatorname{tr}C=0$. If $\lambda\ne1$, the principal block is invertible. If $\lambda=1$, its rank is $2^{k-1}$. Any unpaired component of $\ell$ can be concentrated on one mode per side by local transformations. A side with such a component adds an invertible off-diagonal block of size $2^k$. With one extra block the rank is $2^k$. With two, it is $2^{k+1}$, since the corner opposite $I+C$ is zero. This gives a power of two in every case.

The dimension of $K$ also has a gap. Add one mode and form the even-parity vector $\widetilde\phi=\phi_{\rm even}\otimes|0\rangle+\phi_{\rm odd}\otimes|1\rangle$. The relation $(aI+v)\phi=0$ is equivalent to $(v\otimes I-iaP\otimes Y)\widetilde\phi=0$, where $P$ is the parity of the first $n$ modes and $Y$ is the Pauli matrix. These operators form a hyperplane of the extended Majorana space. If $\dim K\ge n-2$, at most three modes remain after bringing the independent annihilators in $K$ to standard form. To see this, take a Hermitian-orthonormal basis of the isotropic subspace. The real and imaginary parts form orthogonal real pairs to which a Majorana rotation applies. The remaining parity is definite. On at most three modes, a parity-definite vector, after bit flips making the vacuum coefficient nonzero, is proportional to $1+Q=\exp Q$. It has the annihilators of a Gaussian vector. The annihilator space of $\widetilde\phi$ then has dimension $n+1$, and its intersection with the hyperplane has dimension at least $n$. Hence $\dim K=n$.

Cut rank three excludes $\dim K=n$. Thus $\dim K\le n-3$, or $D_1(\phi)\ge n+4$. For the six-mode block, $D_1=10$ is attained by applying a Hadamard only to the second port. This was checked by exact integer elimination. Over the $64$ identity-or-Hadamard choices, the frequencies for $D_1=10,11,12,13$ were $8,16,16,24$. These examples test the first-degree threshold. The uniform bound follows from the argument above.

### Products of blocks

In each block take $\phi$ and nine independent degree-one images. Apply the block operations from left to right. Each choice on the rightmost block selects an independent local vector, while its action on the preceding blocks is a fixed invertible parity operator. Induction gives at least $\sum_{j\le d}[z^j](1+9z)^r$ independent images through degree $d$. Comparing with the Gaussian bound and summing the weighted inequalities gives
$$
R\ge\left(\frac{1+9z}{(1+z)^6}\right)^r
\quad(0<z<1),
\qquad
R\ge \left[\frac85\left(\frac{15}{16}\right)^6\right]^r
>1.086^r .
$$
The last inequality uses $z=1/15$. Each degree-rank constraint is closed because it is defined by vanishing minors. The bound therefore also excludes limits of sums with fewer terms in the same representation.

See [Lyu and Bu, *Displaced Fermionic Gaussian States and their Classical Simulation*](https://arxiv.org/abs/2411.18517) for the formalism of fermionic Gaussians with linear terms. The Gaussian degree filtration is Lemma 13 in the Wei et al. preprint. The use of cut rank three, the gap argument for these blocks, and the uniform bound are developed here.

## Joint changes on the two ports of a column

An invertible $4\times4$ change on each pair of selection ports changes the situation. For a chain of any length with two choices per column and binary carries, the open signature in the new basis is a sum of at most two matchgates.

Order the variables as $a,x,y,d$, for the incoming carry, the two selection ports, and the outgoing carry. In exterior coordinates set
$$
\Phi=(1+y)\exp(ax+xd)=1+y+ax+xd+axy-xyd.
$$
The variables anticommute, and the monomials are in the stated order. In the sectors $(a,d)=(0,0),(1,0),(0,1),(1,1)$ the internal vectors are $1+y,x+xy,x-xy,0$. In the physical basis $(00,10,01,11)$ use
$$
A_0=\begin{pmatrix}
0&0&0&2\\
2&1&1&0\\
0&-1&1&2\\
-2&1&1&0
\end{pmatrix},
\qquad A_1=A_0 P_{00,11},
$$
where $P_{00,11}$ exchanges the first and last coordinates. For $t=0$, applying $A_0$ to the selection ports of $T_t=\mathbf1[s_1+s_2+a=t+2d]$ gives $2\Phi$ with the bit $d$ flipped. For $t=1$, applying $A_1$ gives $2\Phi$ with $a$ flipped. Direct coefficient comparison verifies all $32$ identities.

In the product of unflipped columns in natural order, each $y_i$ squares to zero, and each ordinary commutator $[y_i,y_j]=2y_i y_j$ commutes with the other terms. The Baker–Campbell–Hausdorff formula stops at the commutator and gives
$$
\prod_i(1+y_i)\exp(a_i x_i+x_i d_i)
=(1+L)\exp Q,\qquad
L=\sum_i y_i,\quad Q=\sum_i(a_i x_i+x_i d_i)+\sum_{i<j}y_i y_j .
$$
The terms $\exp Q$ and $L\exp Q$ are Gaussian signatures of opposite parity. For the second, an invertible linear change takes $L$ to the first mode. Multiplication then kills the terms of $Q$ containing that mode, leaving a Gaussian product with the first mode occupied. Apply the carry-bit flips to both terms. Then contract adjacent pairs with $\langle00|+\langle11|$ and pin the boundary carries. These operations preserve the matchgate property. For the first four chain lengths, all target words and exposed coefficients were checked, giving $4680$ comparisons with the carry-matrix product. Through three columns, both parity components were also checked against all matchgate identities.

### Two terms are necessary for the repeated-block family

The four-column separators also work under arbitrary invertible $4\times4$ pair bases. The proof only requires that the parity cap planes remain complementary. In the isolated block with target $(0,0,1)$, the rank across the middle column versus the other four ports is exactly three. The middle-column vectors $|00\rangle$, $|01\rangle+|10\rangle$, and $|11\rangle$ are associated with independent pairs of vectors in the outer columns. The three invertible pair bases preserve rank.

A single matchgate has power-of-two rank across a fermionic bipartition. To handle the middle interval, use a fermionic permutation to move the middle column $B$ to the left. The sign is $(-1)^{p_Ap_B}$, where $p_A,p_B,p_C$ are the parities of the three columns. On a signature of fixed total parity $\delta$, we have $p_B=\delta+p_A+p_C$ modulo two. The sign is therefore an invertible diagonal transformation on $AC$ alone and preserves ordinary rank. For fermionic rank, use the pair decomposition of [Botero and Reznik, *BCS-like Modewise Entanglement of Fermion Gaussian States*](https://arxiv.org/abs/quant-ph/0404176). Rank three requires at least two terms, as attained by the construction above.

### The cost of the equality constraints

Closing the instance identifies the two occurrences of each selection bit. Let $E$ be the equality signature and $A$ the product of the column bases. The count is the bilinear pairing of the transformed arithmetic signature with $A^{-T}E$. The two-term bound applies to the arithmetic signature.

For the explicit bases above, the equality signature can require exponentially many terms even on independent groups of three columns. In each group take one weight for each edge of a triangle. Let $e_0,e_1,e_2$ be the selection bits, with the two ports of column $j$ reading $e_j,e_{j-1}$ modulo three. The group's target is $(1,1,0)$. Put
$$
D_0=4A_0^{-T}=\begin{pmatrix}
0&2&-2&2\\
1&1&1&0\\
0&-2&2&0\\
-1&1&1&0
\end{pmatrix},
\qquad D_1=D_0P_{00,11}.
$$
Up to a nonzero scalar, the transformed triangle has coefficients
$$
\eta(b_0,b_1,b_2)
=\sum_{e_0,e_1,e_2}\prod_{j=0}^2
 D_{t_j}[b_j,e_j+2e_{j-1}] .
$$
Number the six ports from left to right and encode each pair as $b_j=x_j+2y_j$. Elimination modulo $1009$ on the columns $\gamma_{i_1}\cdots\gamma_{i_k}\eta$ for $k=0,1,2,3$ gives cumulative ranks $1,13,63,64$. Use the Majorana conventions above, with distinct indices increasing in each word and words in lexicographic order within each degree. The sum of the squares of the integer coefficients of $\eta$ is $2616$. Pivot products in that order, reduced modulo $1009$, are $985,743,969,516$. The ranks are lower bounds in characteristic zero. For $r$ repeated triangles, the contiguous-block independence argument and the Gaussian bound give
$$
R_E\ge \left(\frac{1+12z+50z^2+z^3}{(1+z)^6}\right)^r > 1.89^r
\quad\text{at }z=3/10 .
$$
This bounds the separate representation of the equality constraints in these bases. At its own scale, each group has weights $3,5,6$ and target $3$. Selecting the weight $3$ in every group solves the instance.

The equality-signature bound holds generically in the family obtained by replacing the column form $\Phi$ with $(1+\lambda y)\exp(pax+qxd)$, for $\lambda,p,q\ne0$, and completing the basis on the antisymmetric vector. The open product still has at most two terms, even with parameters varying by column. The witnessing minors become rational functions of the parameters. They are nonzero at the explicit example, hence outside their vanishing set. Exceptional joint bases remain open.

## Parameterized hardness in the number of runs

For Subset Sum on a simple cycle, with parameter $r$ equal to the number of constant runs of the target, decision is W[1]-hard and counting is #W[1]-hard. Under ETH, a running time $f(r)N^{o(r/\log(r+2))}$ is excluded for any computable $f$. The construction starts from a finite-domain binary CSP. For variable $i$ choose an index $a_i\in[1,n_i]$. Each constrained pair is given a list of allowed index pairs. Intersect repeated constraints on the same pair first.

### Selecting and reading a switch position

A selector is a zero run with incoming carry zero followed by a one-target column with no choices. The last column forces incoming carry one and outgoing carry zero. Hence the run contains exactly one switch from zero to one.

A read column has target zero and one port fixed to zero. Its other port reads the carry $c$ because $x+c=2d$ forces $x=c=d$. To supply the fixed zero endpoints, put all such columns in an initial zero region, followed by a zero-target column with no choices. Its boundary carries are zero, and monotonicity keeps every internal carry zero. To make two reads equal, join them by an edge. To make them complementary, connect their two edges to a one-target column before the initial zero region. Throughout this initial one run the carry stays zero, so exactly one of its two edges is selected.

Option $j$ has a zero-target marker column with two edges. One carries the outgoing carry $d$, read immediately after the marker. The other carries $p_j$. Its equation $d+p_j+c=2d$ gives $p_j=d-c$. The edge $p_j$ is selected precisely when this marker switches the carry. Cut $j$ means the site after marker $j$ and before the next marker. Cut zero precedes all markers and cut $n_i$ follows the last. For choice $a_i$, the carry at cut $j$ is $C_i(j)=\mathbf1[a_i\le j]$.

### Comparing a choice with the endpoints of a constraint

Use six blocks per variable: two for the main choice, two forward readers, and two reverse readers. Couple the $p_j$ edges of the first two blocks directly to enforce agreement. At every cut $j$ of a forward reader, tie two distinct main-block reads to the reads at the beginning and end of the reader's test site. These enclose the test columns and cross no marker. At cut $j$ of a reverse reader, enforce instead the complement of the main carry at cut $n_i-j$. Its value is $1-C_i(n_i-j)$. Equality of the endpoint reads and monotonicity make the carry constant throughout every test site. Thus a reader also switches only at a marker. Pair the marker edges of the two readers with the same orientation to terminate them without introducing a choice.

For a constraint between two variables, use eight synchronized copies of a selector whose options are the allowed pairs. Synchronize by equating the reads at every cut. Each pair $(u,v)$ then has eight copies of a signal $p$ that is one exactly if that pair is selected. Four pairs of copies check $a_i\le u$, $a_i\ge u$, $a_j\le v$, and $a_j\ge v$, respectively, conditional on $p=1$.

A test uses one column in each of the two readers of the same orientation of the relevant variable. Put one copy of $p$ at each column and join those columns by an edge $q$. The site carry $C$ is constant, so both equations are $p+q=C$. There is one choice of $q$ if $p\le C$ and zero choices otherwise. The forward reader uses cut $u$, giving $C=\mathbf1[a_i\le u]$. The reverse reader uses cut $n_i-u+1$, giving $C=1-C_i(u-1)=\mathbf1[a_i\ge u]$. Apply the same two tests to the other endpoint. A satisfying assignment picks a unique allowed pair in each list and determines all auxiliary edges. A numerical solution determines a satisfying assignment.

### One cycle and a bound on runs

Every column has degree at most two, and the weight graph is a forest of short paths. Reads terminate at fixed endpoints. Equalities, complements, marker pairings, and paired comparison columns all lie on paths with such endpoints. The longest path goes from a pin to a read, a marker, two tests, the other marker, another read, and the other pin. Empty columns are isolated. Apply the [completion with two new positions per ordinary connector and final local target 29](04-fixed-weights-and-proofs.md#black-box-verifier). All completion edges except the two specified internal edges are forced to zero. This preserves the count and gives a single simple cycle with distinct weights strictly smaller than the target.

With $k$ variables and $m$ constrained pairs there are $6k+8m$ selectors. Each adds at most two runs. The initial complement and pin regions and the completion add at most six, giving $r\le12k+16m+6$. The number of columns is linear in the sum of domain sizes and the sizes of the allowed-pair lists, plus $k+m$. Each option requires a constant number of synchronization reads, and each listed pair a constant number of tests. The explicit binary encoding is polynomial.

For Multicolour Clique take one variable per color and the adjacency list for every pair of colors. Then $m=\binom{k}{2}$ and the reduction is parameterized and parsimonious. This gives W[1]-hardness and #W[1]-hardness. See [Jerrum and Meeks, *Some hard families of parameterised counting problems*](https://eprints.gla.ac.uk/97129/1/97129.pdf), Section 1.2, for the source counting problem.

For the ETH bound start directly from Partitioned Subgraph Isomorphism. Each pattern vertex is a variable and each pattern edge supplies an allowed-pair list. It suffices to use the patterns without isolated vertices in [Marx, *Can You Beat Treewidth?*](https://toc.cs.uchicago.edu/articles/v006a005/v006a005.pdf), Corollaries 6.2 and 6.3. If the pattern has $m$ edges, then $k\le2m$ and $r=O(m)$. Under ETH, Marx excludes $f(G)n^{o(m/\log m)}$ for pattern $G$ and host size $n$. Since the numerical output size is polynomial, a running time $f(r)N^{o(r/\log(r+2))}$ would violate that bound. For empty domains or lists, output a fixed negative instance, the cycle with weights $3,5,6$ and target $7$.

### Checks of the reduction

Direct enumeration of domain assignments and an exact solver for the column equations agreed on 68 Multicolour Clique instances, 14 negative, and on 75 other CSPs, including 60 with a path constraint graph. In the first 68 experiments, counts were checked both before and after completion, with up to 6022 columns. The completed solver used the pins implied by the closing block. Its property was checked separately on all $64$ local subsets. The total $28$ is absent, and only $\{5,24\}$ gives $29$.

## Exact parameterized classification on one cycle

For Subset Sum on a simple cycle, with parameter $r$ the number of constant target runs, decision is W[1]-complete and exact counting is #W[1]-complete. The previous section proves hardness. For membership, construct a parsimonious reduction to Multicolour Clique with $O(r^2)$ color classes.

For run $i$ of length $\ell_i$, its local options are the two constant carries and the $\ell_i$ possible switch positions in the allowed direction. An option specifies every required degree $s_v$ in the run. Consecutive runs agree at their common boundary, and the first and last carries are zero. These are unary and binary constraints.

Let $v_0,\ldots,v_{N-1}$ be the columns in cyclic order, and let $b$ be the selection bit of the edge immediately before $v_0$. From the chosen options, compute $x_{-1}=b$ and $x_j=s_{v_j}-x_{j-1}$. Cycle closure and binary values for every edge are equivalent to
$$
F=\sum_{j=0}^{N-1}x_j(x_j-1)+(x_{N-1}-b)^2=0.
$$
Every summand is nonnegative on integers. A valid subset gives exactly one option per run and one $b$. The converse follows by propagation.

The vector $x$ depends additively on the choices. For each option $a$ of run $i$, precompute $q_{i,a}$ by running the recurrence with $b=0$ and all degrees outside the run set to zero. Append a duplicate of its last coordinate to represent its contribution to $x_{N-1}-b$. The vector for $b$ uses alternating signs and an additional $-b$ in the appended coordinate. The sum of all vectors has first $N$ entries $x_j$ and last entry $x_{N-1}-b$. Thus $F$ is the squared norm of the sum minus the sum of the first $N$ entries. Expanding gives a constant and $O(r^2)$ tabulated terms, each depending on at most two choices. All weights have magnitude polynomial in $N$.

Introduce an auxiliary variable for each table term. Its domain consists of a tuple of the relevant choice indices and the partial sums before and after that term, retaining only tuples with the prescribed change. All partial sums lie in a polynomial-sized integer interval. Binary constraints match the indices to the original variables and the partial sums of adjacent terms. Require both the initial and final sums to be zero and include any constant as a term. A valid assignment uniquely determines all auxiliary tuples. One color class per variable and one edge for every compatible pair give Multicolour Clique, with one clique per subset. The target counting problem is #W[1]-complete by [Jerrum and Meeks](https://eprints.gla.ac.uk/97129/1/97129.pdf), Section 1.2.

### Counting with three groups

For each fixed $b$, split the runs into three groups $A,B,C$. A vertex in a group specifies a choice in every run of that group. Discard incompatible choices within groups and edges between choices with mismatched carries at run boundaries. Assign to each pair of groups the sum of the corresponding cross terms of $F$. Add each group's internal cost to its outgoing edge in the orientation $A\to B\to C\to A$, and put the constant on one of the three edges. The total triangle weight is $F$.

Add the same shift $H$ to all edge weights to make the exponents nonnegative. In matrices $P_{AB},P_{BC},P_{CA}$ encode each allowed edge of weight $w$ by $X^{w+H}$ and each absent edge by zero. The coefficient of $X^{3H}$ in the trace of $P_{AB}P_{BC}P_{CA}$ counts valid triangles. The polynomial degree is polynomial in $N$. Equivalently, evaluate at a power of two larger than the total number of possible triangles, and extract digit $3H$. The degree and the $O(r\log(N+2))$ bits of the base make the cost per arithmetic operation polynomial in $N$.

With at most $\lceil r/3\rceil$ runs per group, the largest matrix size is $(N+2)^{\lceil r/3\rceil}$. [Strassen multiplication](https://deltadbu.github.io/UCAS_algorithm_course/Lectures/Lec5-Matrix-Multiplication-Strassen1969.pdf) gives exact running time
$$
N^{(\log_2 7)r/3+O(1)}.
$$
One may balance domain products instead of the number of runs. Assign each run to the group with the current smallest sum of log domain sizes. The final maximum sum is at most one third of the total plus two thirds of the largest individual log. Thus the time is at most $\operatorname{poly}(N)\bigl(\prod_i(\ell_i+2)\bigr)^{(\log_2 7)/3}$.

The quadratic test and triangle method agreed with direct enumeration on 425 instances, covering 11412 carry-vector and initial-bit pairs. An exact integer trace was also checked on 276 instances. These are finite checks of the count identity. The running time comes from substituting Strassen multiplication.

## Linear exponent bound for multiple cycles

When the weight graph is a disjoint union of cycles, ETH excludes time $f(r)N^{o(r)}$. Here the parameter of the Multicolour Clique reduction is linear in the number of colors. Enumerating carry vectors and propagating around each cycle gives decision and counting in $N^{O(r)}$ time. Lemma 13 of [*Tight Bounds for Clique-Packing Parameterized by Clique-Width*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/html/LIPIcs.ESA.2026.115/LIPIcs.ESA.2026.115.html) states the source ETH bound.

For each color use the six selector and reader blocks above. At forward sites use $C_i(u)=\mathbf1[a_i\le u]$, and at reverse sites use the complement of the corresponding main read. Endpoint reads keep each test site's carry constant. Thus arbitrarily many two-choice columns of degree $C_i(u)$ or $1-C_i(u)$ can be inserted without adding runs. Columns of degree one can be placed in the initial one run.

For every forbidden pair $(u,v)$ between colors $i,j$, use a path of six columns with two open terminals. With $M_0,M_1$ the transfer matrices for degrees zero and one from [Note 02](02-counting-and-parameters.md), this path has matrix
$$
P=M_{C_i(u-1)}\,M_{1-C_j(v-1)}\,M_1\,
M_{C_j(v)}\,M_{1-C_i(u)}\,M_1 .
$$
Each conditional factor is a column at the corresponding read site. The factors are consecutive in the weight graph because they are joined by the path. Their bit positions are determined by their read sites. In the nine cases, with rows $a_i<u,a_i=u,a_i>u$ and columns $a_j<v,a_j=v,a_j>v$, the matrix $P$ takes the values
$$
\begin{pmatrix}
E_{11}&E_{01}&E_{11}\\
E_{01}&0&E_{01}\\
E_{00}&E_{01}&E_{00}
\end{pmatrix}.
$$
Here $E_{ab}$ is the $2\times2$ matrix with a single one at $(a,b)$ using zero-based indices. Join two copies of the path at their left and right terminals. The resulting twelve-column cycle contributes $\operatorname{tr}(PP^{\mathsf T})$, equal to one on every allowed pair and zero on the forbidden pair.

The test cycles are already closed. The other components are paths from selection and synchronization. Complete only those into one additional cycle by the construction with final local target $29$. The weights are distinct, with two set bits apiece and two occurrences per column. The target bit is constant throughout each run's test sites. There are at most $12k+6$ runs for $k$ colors, independent of the number of forbidden pairs. The number of columns is polynomial in the domain sizes. The reduction preserves counts and transfers the Multicolour Clique bound against $f(k)n^{o(k)}$ time under ETH.

The nine cases and the complete construction were checked. On 85 Multicolour Clique instances, 50 positive and 35 negative, the column-equation count agreed with the direct clique count. The largest instances had 1530 columns and 34 test cycles.

## Limit on combining threshold checks

Threshold readings alone cannot combine the checks from the preceding section arbitrarily. The following bound concerns a local model in which, once the choices are fixed, each column has a required degree $s\in\{0,1,2\}$ that is constant or determined by a single ordered variable. If a function of one variable takes two consecutive values, it may not isolate one interior domain position as the sole occurrence of either value. This condition includes all forward and reverse thresholds in the preceding blocks. It also includes the degree of an interior marker column, which takes all three values $0,1,2$.

### A single check with one endpoint fixed

Let $a,b$ be two variables with interior positions $u,v$. Consider a path of columns with a fixed initial wire and a final wire that may be free or fixed. Such a path cannot accept exactly all pairs other than $(u,v)$.

With the initial wire fixed, the recurrence $x_j=s_j-x_{j-1}$ determines every wire. Since each $s_j$ depends on at most one variable, each $x_j$ has the form $f_j(a)+g_j(b)$ with integer-valued $f_j,g_j$. A function of this form that is binary on the full product of the domains depends on at most one variable. If both functions vary, the maximum of their sum exceeds its minimum by at least two.

Suppose the path accepts every pair other than $(u,v)$. Consider the first wire that ceases to be binary at $(u,v)$. If the preceding wire and the column degree depend on the same variable, or if either is constant, the violation also affects a pair that must be accepted. Up to swapping the variables, the remaining case is $x_{j-1}=f(a)$ and $s_j=g(b)$. For any $a\ne u$, all values of $b$ must give a binary result. Hence $g$ can take only one value or two consecutive values. By the assumption on degrees, some $b'\ne v$ satisfies $g(b')=g(v)$. The pair $(u,b')$ then has the same violation. If all wires are binary on the full product, the last wire also depends on at most one variable, so fixing it cannot exclude only $(u,v)$.

### How many components are needed

In the same model, excluding $k$ interior pairs on $k$ disjoint pairs of variables while allowing every other combination requires at least $k$ cycles in the summand graph. This holds even when the initial bit of each cycle is free.

If a cycle has a vertex of degree zero or two on an allowed assignment, fix the pair containing the variable on which that degree depends to its values in that assignment. A constant degree requires fixing no pair. The vertex fixes both incident wires, so the rest of the cycle can be treated as a path. On any variable pair still free, with the other variables fixed to allowed values, this path accepts all the allowed combinations. By the lemma it also accepts the interior pair that was to be excluded.

Repeat for each cycle that still lacks a fixed vertex and can attain degree zero or two at a vertex on an allowed assignment to the remaining pairs. At most one pair is fixed per cycle. If there are fewer than $k$ cycles, at least one pair remains free at the end. In every cycle still lacking a fixed vertex, all columns have degree one on every remaining allowed assignment. Each free variable takes every value in its domain on these assignments. Since each column degree depends on at most one variable, those columns retain degree one on the excluded interior pair as well. This gives a configuration that every cycle accepts and the desired relation forbids.

The result explains why merging the components directly with additional threshold paths cannot in general produce a single cycle. The conclusion applies to the specified representation with unary degrees. A mechanism that couples degrees to multiple choices, or introduces a different type of unary dependence, falls outside the lemma.

Exhaustive exploration with two domains of size three and the 23 allowed unary functions on each found 14 reachable binary states for each initial bit while keeping the eight allowed pairs valid. No transition kept those eight pairs and made only the ninth fail. The proof above holds independently of this enumeration.

## Parameterized classification for multiple cycles

For a disjoint union of cycles, decision is W[1]-complete with respect to the number $r$ of runs. Counting only the carry configurations that admit at least one subset is also #W[1]-complete for the same parameter. Counting all subsets introduces a multiplicity per configuration and requires separate treatment.

For each cycle $C$ and initial bit $b\in\{0,1\}$, use the penalty $F_{C,b}$ from the single-cycle section, computed only on the vertices of $C$. For fixed carries the penalty is a nonnegative integer and vanishes exactly when that initial bit yields a valid choice. Every cycle admits a choice if and only if
$$
\Phi=\sum_C F_{C,0}F_{C,1}=0 .
$$
The two factors remove the need to guess each cycle's initial bit separately. Each $F_{C,b}$ is a sum of terms that can be tabulated using at most two run options. The product has interactions among at most four options. Aggregate the tables by summing over all cycles for each set of at most four runs. This leaves $O(r^4)$ tables with entries of magnitude polynomial in $N$. Applying the partial-sum and binary-constraint construction for one cycle to terms with up to four indices gives a parsimonious reduction to Multicolored Clique. Each realizable carry configuration corresponds to one clique. For hardness of counting configurations, the previous single-cycle reduction has a vertex forced to degree zero in the final block. There is thus at most one subset per carry configuration, and the preceding reduction from Multicolored Clique also preserves the number of configurations. For the parsimonious definition of the counting classes, see [Jerrum and Meeks, Some hard families of parameterised counting problems](https://eprints.gla.ac.uk/97129/1/97129.pdf), §1.2.

A cycle with at least one degree zero or two has at most one solution per configuration, because that vertex fixes both incident wires. If all degrees are one, there are two solutions for an even cycle and zero for an odd one. Thus, given the realizable configurations $\mathbf c$, the total number of subsets is
$$
\sum_{\mathbf c:\,\Phi(\mathbf c)=0}2^{g(\mathbf c)},
$$
where $g$ counts the even cycles whose degrees are all one. The multiplicity can be exponential even for $r=1$. With an all-ones target and a union of four-cycles, all carries remain zero and all degrees are one. The sole configuration has $2^{N/4}$ subsets. A parsimonious reduction to Multicolored Clique parameterized by $r$ cannot preserve this count. For a fixed parameter, the resulting instance would have polynomial size and a bounded number of color classes, so its count would be at most polynomial. For the combined parameter $r+h$, where $h$ is the number of cycles, counting all subsets is #W[1]-complete. Retain an initial bit for each cycle and impose $\sum_C F_{C,b_C}=0$, with exactly one auxiliary choice for each subset.

In the weighted formula, $g$ also has a geometric description. Let $\lambda_i=0$ denote the option of run $i$ with all degrees one, let $\lambda_i=\ell_i+1$ denote the option with all degrees fixed, and otherwise let $\lambda_i$ be the switch position, numbered from one. An even cycle contributes to $g$ exactly when, for every run it intersects, $\lambda_i$ precedes its first column in that run. Counting the free cycles is therefore a dominance counting problem in dimension $r$. This observation describes the weight of a given configuration.

The global penalty, the realizable configurations, and their multiplicities were compared against an enumeration of all subsets on 377 instances, 207 of them with multiple cycles, for a total of 6021 arithmetically admissible configurations. The expansion into terms depending on at most four choices was also checked in 311 cases.

## Derivations of the circuit lower bounds

### Unconditional Boolean lower bounds

Fixing the constant bits and renaming the other bits preserves fan-in and depth in Boolean circuits. Compiling Parity, which has a linear-size XOR circuit and hence a linear-size AND and NOT circuit, produces a family with $N=\Theta(m)$ that requires $2^{\Omega_d(N^{1/(d-1)})}$ gates at fixed depth $d\ge2$ in the model with unbounded-fan-in AND and OR and input negations. This transfers [Håstad's lower bound for Parity](https://eccc.weizmann.ac.il/report/2019/073/) to the restriction to the free target bits.

There is also a restriction of the target that is itself monotone and hard for monotone Boolean circuits. Use the Harnik–Raz function on $m$ bits for prime $m$. The verifier takes as a witness the coefficients of a polynomial $P$ over $\mathbb F_m$ of degree below $c=\Theta(\sqrt m/\log m)$. It checks that among $P(1),\ldots,P(k)$, with $k=\lfloor\sqrt m\rfloor$, there are at least $k/2$ distinct values and all the corresponding input bits are one. The parameters are those of [Cavalar, Kumar and Rossman, Monotone Circuit Lower Bounds from Robust Sunflowers](https://eccc.weizmann.ac.il/report/2020/181/revision/2/download/), §2.2 and Theorem 2.19.

There is a verifier with $O(m\log^3 m)$ gates. Horner's method uses $O(kc)$ modular operations, each implemented with $O(\log^2 m)$ gates by schoolbook arithmetic. Comparing all pairs of computed values and marking the first occurrence of each gives the number of distinct values in $O(k^2\log m)$ gates. To read the input bits, use a Batcher bitonic sorting network. Sort the $m$ data records together with the $k$ records requesting a bit. Each key is an $O(\log m)$-bit index, with data preceding requests on ties. A scan updates the current bit at every data record and checks it at every request. The network uses $O(m\log^2 m)$ comparators at a cost of $O(\log m)$ gates each. Checking canonical encodings of the coefficients and counting the first occurrences fit within the same bounds.

The compiled size is therefore $N=O(m\log^3 m)$. The monotone lower bound $2^{\Omega(\sqrt m/\log m)}$ of Cavalar, Kumar and Rossman gives
$$
2^{\Omega(\sqrt N/\log^{5/2}N)}
$$
for the resulting target restriction. Monotonicity concerns the free inputs of the compiled instance. Constant bits can be wired directly without adding negations.

### Exponential lower bound for the subset polynomial

For a fixed cycle and a fixed target, consider the polynomial
$$
G(z)=\sum_{S:\,\sum_{e\in S}w_e=T}\prod_{e\in S}z_e .
$$
There are families with $N$ columns for which any arithmetic circuit with addition, multiplication, and nonnegative constants computing $G$ has size $2^{\Omega(N)}$. The bound concerns the symbolic polynomial. Evaluating it at a point, such as counting the subsets by setting every $z_e$ to one, is a separate problem.

First construct a binary linear code of length $m$ with at least $2^{m/2}$ codewords, positive relative distance, and a linear-size verifier. For $m$ a multiple of six, connect $m$ variables with four ports each to $m/2$ parity checks with eight ports each, using a random permutation to match the ports. A nonzero word of weight $t$ can be valid only if its $4t$ ports meet at most $2t$ checks, since each check they meet must receive an even number of ports from the word. Taking the union bound over all supports of size $t$ gives
$$
\binom{m}{t}\binom{m/2}{2t}(4t/m)^{4t}
\ \le\ (16e^3t/m)^t .
$$
The sum over $1\le t\le\delta m$ tends to zero for a sufficiently small constant $\delta>0$. This follows by splitting the sum at $t=\sqrt m$. The valid words form a subspace of dimension at least $m/2$. Each check has a constant number of inputs, so verification uses $O(m)$ gates. The existence argument allows multiple connections between a variable and a check.

Next amplify the distance by choosing an ordered tuple of $L$ independent uniform indices for each of $m$ new positions, with constant $L$ such that $(1-\delta)^L\le2^{-9}$. Each new position contains the tuple of corresponding bits of the original codeword, a symbol over a constant alphabet of size $2^L$. Two distinct codewords agree at a new position with probability at most $2^{-9}$. The probability that they agree at at least $m/3$ positions is at most $2^m(2^{-9})^{m/3}=2^{-2m}$. By linearity of the binary code, it suffices to take the union bound over its fewer than $2^m$ nonzero differences. There is therefore a fixed choice of tuples for which the amplified code $C$ has at least $2^{m/2}$ codewords and any two distinct codewords agree in at most $m/3-1$ coordinates. The tuple map is injective. The two structures follow from probabilistic existence arguments, without requiring an efficient uniform algorithm to find them.

For every new position $j$ and symbol $a$, create a variable that is one exactly when the tuple at that position is $a$. The total Boolean cost is $O(m)$ because $L$ and the alphabet size are constants. Compile the verifier and all these auxiliary values into Subset Sum, with the binary words as witnesses and no free target bits. In $G$, substitute $X_{j,a}$ for the variable $z_e$ of the edge $q$ that reads this flag, and substitute one for every other indeterminate. This gives exactly
$$
P_C(X)=\sum_{c\in C}\prod_{j=1}^m X_{j,c_j}.
$$
The correspondence between the original words, amplified words, and subsets ensures that every monomial has coefficient one. By [Theorem 7 of Cavalar, Kumar and Rossman](https://pmc.ncbi.nlm.nih.gov/articles/PMC9705498/), the distance of the code forces any monotone arithmetic circuit for $P_C$ to have size at least $|C|$. Substitution preserves the circuit model, and $N=\Theta(m)$, giving the stated lower bound for $G$.
