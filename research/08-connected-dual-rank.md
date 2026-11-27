# Exponential dual rank on one selection cycle

**Working proof and finite checks.** [Note 03](03-matchgate-representations.md#the-transformed-equality-signature) gives an exponential rank obstruction for the explicit pair bases on a disjoint union of triangles. The obstruction holds for a single selection cycle in bit order, with an alternating target. It also holds for every choice of which physical wire within a column is the first port of the pair basis.

## The single-cycle instance

Use $N=4m$ columns in bit order, starting from zero. Selection edges connect successive columns, including the edge from the last column to column zero. The target bits repeat $(0,1,0,1)$ in increasing bit order. Use $A_0,A_1$ from [Note 03](03-matchgate-representations.md#joint-changes-within-a-column) and put $D_t=4A_t^{-\mathsf{T}}$. Scalar factors of four are immaterial to rank. The dual equality signature is the ordinary coefficient tensor after applying $D_{t_j}$ to the two selection ports of each column. The terminal order places the two ports of each column consecutively in bit order.

Mark column $4j$ in every block as a separator. Its target bit is zero. In coordinates ordered $(00,10,01,11)$, use the covector $(0,2,-1,0)$ if the incoming cycle wire is the first port, and $(0,2,1,0)$ otherwise. Pulling these covectors back through $D_0$ gives respectively $(2,4,0,0)$ and $(2,0,4,0)$. On the two physical wires in incoming and outgoing order either pullback equals

```math
2\,p(\mathrm{incoming})q(\mathrm{outgoing}),\qquad
p=(1,2),\quad q=(1,0).
```

The covector on the transformed pair is an odd two-mode matchgate. It is a linear combination supported on the two one-particle basis vectors. An invertible number-preserving change of basis on that pair turns it into a computational-basis covector. Slicing a fermionic Gaussian signature at fixed occupation bits preserves its Gaussian form or gives zero. To relate the ordinary slice to fermionic postselection, move the measured adjacent pair to the end by fermionic swaps. The resulting sign for a fixed measured parity is a parity operator on the modes that were to its right. That operator is Gaussian, so the ordinary slice in the retained terminal order has the same preservation property. Apply the argument to each separator.

The pulled-back covectors split all separator vertices into independent boundary factors. The projected signature is a nonzero scalar multiple of a product of $m$ active blocks on six modes apiece. Each block has target $(1,0,1)$, left boundary given by $q$ and right boundary given by $p$. The blocks are contiguous in the retained terminal order.

## Rank certificate and growth

For a six-mode block, form the matrix of the block vector and its images under Majorana words of degree at most $d$. The checker gives cumulative ranks $1,13,63,64$ for $d=0,1,2,3$ in **all eight** port orders, using elimination modulo 1009 on integer coefficient columns. The modular ranks give lower bounds over the complex numbers. They certify independent block vectors of respective degree costs $0,1,2,3$ in quantities $1,12,50,1$.

For $m$ blocks, the filtered dimensions of these independent vectors multiply. The Jordan–Wigner strings from the rightmost block act by one fixed invertible parity operator on the earlier blocks for each choice of a word on the rightmost one. The selected vectors of the rightmost block are independent. Inducting over the blocks proves independence of the resulting products. Thus the degree-$d$ span has dimension at least the sum of coefficients through degree $d$ in $(1+12z+50z^2+z^3)^m$.

A Gaussian signature on $6m$ modes has cumulative degree-$d$ span at most $\sum_{j\le d}\binom{6m}{j}$. In the vacuum basis, a Majorana word of degree at most $d$ makes at most $d$ excitations. An invertible Gaussian change of basis preserves the filtration. This is the Majorana span argument used in [Note 03](03-matchgate-representations.md#the-transformed-equality-signature) and in the [Gaussian-rank bounds of Wei et al.](https://arxiv.org/abs/2610.02172). For a sum of $R$ Gaussian signatures the span is bounded by the sum of their dimensions.

Weight the cumulative bounds by $z^d$ for $0\lt z\lt1$ and sum over $d$. The cumulative sums contribute the same geometric factor on both sides. After cancellation,

```math
R \ge
\left(\frac{1+12z+50z^2+z^3}{(1+z)^6}\right)^m
> 1.89^m
\quad\text{at }z=3/10.
```

Every Gaussian summand of the original unprojected signature remains Gaussian or vanishes under the caps. Hence the lower bound applies to the original transformed equality signature. The same obstruction holds for limits of sums of a fixed number of Gaussian signatures, since each necessary rank bound is closed by vanishing minors.

## Comparison with the subset count

This particular family admits a direct count. The internal weights are $3\cdot 2^j$ for $0\le j\le N-2$. The closing weight is $2^{N-1}+1$, also divisible by three because $N$ is even. The alternating target is twice the sum of the first $N/2$ powers of four, so it is divisible by three precisely when $m$ is a multiple of three. In that case the target and the target minus the closing weight are both nonnegative multiples of three within the internal range. Each choice for the closing weight then gives one subset by binary expansion. The count is two for multiples of three and zero otherwise. The exponential bound therefore concerns the separate Gaussian decomposition of the equality signature in these explicit bases.

## Reproduction

Run `python verify.py` from the repository root. The new check verifies the two pulled-back covectors, the eight local rank certificates, and 4,160 projected coefficients on one and two blocks using a cyclic transfer product. It also checks the subset count for the first five instance lengths.
