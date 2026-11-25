# Exact counting by run cutwidth

**Algorithm, proof, and executable checks.** This note counts Subset Sum solutions for a single selection cycle by processing whole runs of equal target bits. It uses the [carry model in Note 02](02-counting-and-parameters.md#carries-as-the-search-variables). The matching conditional lower bound in the width parameter uses the alternating-target reduction of [Note 01](01-alternating-target.md).

## The width parameter

The input has $N$ bit columns, a selection cycle on those columns, and a target written on the same $N$ columns. Each selection edge between columns $i,j$ represents a weight $2^i+2^j$. A run is a maximal constant substring of the target in increasing bit order. Form a multigraph with one vertex per run. Include one edge for each selection wire whose ends belong to different runs, and one for each carry wire joining consecutive runs in bit order. Retain all parallel edges. Choose an order of the runs. Let $w$ be the largest number of wires crossing a prefix cut of this order.

**Theorem.** Given the order, the exact number of solutions can be computed in
$$
O\bigl(N\log(N+1)+N(w+1)2^w\bigr)
$$
arithmetic operations and $O(N+2^w)$ arithmetic slots. The counts use $O(N)$ bits per slot. Under ETH, time $2^{o(w)}\operatorname{poly}(N)$ is impossible uniformly, even with the order supplied.

## What a run contributes

At a column $v$ with target bit $t$, the incoming and outgoing carries $c,d$ determine the required sum $s=t+2d-c$ of the two selection bits. A zero run starts and stays in carry one with all degrees one, starts and stays in zero with all degrees zero, or switches from zero to one at a designated column. The switch puts degree two at that column, degree zero before it, and degree one after it. A one run has the complementary pattern $s\mapsto 2-s$ with carries complemented. Thus a run of length $\ell$ has $\ell+2$ options, each fixing both of its boundary carries. Impose carry zero at the two ends of the full bit order.

In cyclic order a proper run induces disjoint path fragments. With the carries of the run fixed, a fragment is a partial bijection from its entering selection bit to its exiting selection bit. At each column the transition is $b\mapsto s-b$ on the inputs for which the output is binary. For $s=0,1,2$, these transitions respectively pin zero, flip, and pin one. A composition preserves partial bijectivity. Every accepted pair of endpoint bits has exactly one internal selection. The whole-cycle case with one run is counted by summing the fixed points of its transfer over options having both external carries zero.

A balanced product tree per fragment maintains its transfer. Enumerate first the all-degree-one option, then the switch positions in bit order, then the all-pinned option. Consecutive options change at most two columns, so setup and updates for all runs use $O(N\log(N+1))$ operations. The fragment trees contain $O(N)$ entries.

## Counting across the cut

Keep a table indexed by the crossing wires. An entry counts compatible choices inside the processed runs. It starts with the empty assignment of count one. To add a run, separate the wires into three sets. Some cross both the old and new cuts, some end on the run from the processed side, and some start at the run toward the unprocessed side.

For one run option, filter old table entries by the fixed old carry values and the transfers of fragments with both endpoints on the old side. A fragment with one endpoint on each side determines the new bit from the old bit, possibly rejecting the old entry. Use the inverse partial map when the fragment points from new to old. Sum each surviving entry into a temporary table keyed by the common wires and the new bits determined by these mixed fragments. Then scan the new cut assignments. Keep those that satisfy the new carry values and the transfers of fragments with both endpoints on the new side. Add the temporary count matching their key. Each remaining fragment with endpoints on only the new side has exactly one internal selection for its chosen pair of endpoint bits.

The two scans have at most $2^w$ entries each. Fragment endpoints are distinct incident wires from the union of the old and new cuts. There are at most $2w$ such wires, so classifying the fragment transfers and doing the work per assignment costs $O(w+1)$. Summing over all $\sum_i(\ell_i+2)=O(N)$ options gives the stated bound. A subset fixes all selection bits and all carries, so each valid subset is counted once when the final table has empty boundary. The per-entry count is bounded by the number of assignments to $O(N)$ binary wires.

## Tightness and an example

In [Note 01](01-alternating-target.md), ETH excludes $2^{o(N)}\operatorname{poly}(N)$ time even for alternating targets. For those instances, every run is one column and every order has $w\le 2N-1$ by the total wire count. Supplying bit order to an algorithm with time $2^{o(w)}\operatorname{poly}(N)$ would give the excluded bound. This establishes the order of growth of the exponent in $w$. The separate question of a bound in the number of runs alone remains open.

For a family of width three, label the runs $0,\ldots,r-1$. Arrange two nonempty fragments per run in cyclic order
$$
0,1,\ldots,r-1,r-1,\ldots,1,0 .
$$
For $r\ge2$, every proper prefix of the bit order has two selection wires and one carry wire across its cut. The arrangement inside any fragment is arbitrary. For example, with 40 runs of length 32, split each run into its first 16 and last 16 positions in bit order, placing the first halves on the forward pass and the last halves on the reverse pass. The implementation returns 22 solutions on this 1,280-column instance when the first run is zero.

## Reproduction

`count_by_runs` in [run_counting.py](../run_counting.py) takes the target bits least significant first, the cyclic list of columns, and an optional run order. The default is bit order. Run `python verify.py` from the repository root. It compares the resulting counts with exact integer subset search on all 440 simple cycle and target cases with three to five columns up to cycle rotation and reversal, and on 240 further seeded instances with up to twelve columns. Each case uses bit order and a seeded permutation of the runs.
