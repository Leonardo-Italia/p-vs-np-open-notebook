# Fixed weights and proof complexity

**Proof drafts.** The two constructions below are mathematical arguments based on the [local blocks](01-alternating-target.md). The [checker](../verify.py) exercises those shared blocks. The fixed circuit compiler and proof-system transfers are described here and in the [technical drafts](technical-drafts.md). The release checker does not test those full transfers. Independent proof review has not been recorded.

## Black-box verifier

For a Boolean circuit $V(x,y)$ of AND and NOT gates, there is a fixed list $W_V$ of distinct two-bit weights whose graph is a single cycle. The target $T_V(x)$ has each input bit of $x$ in a distinct position, with all other positions fixed. Valid subsets are in bijection with witnesses $y$ for which $V(x,y)=1$. The number of bit positions and weights is linear in the circuit size plus the number of input and witness bits. The topology is fixed for a given verifier.

To construct it, first compile the circuit into the exact-one relation $R(a,b,c)$, meaning $a+b+c=1$. The three relations $R(u,v,w),R(u,w,f),R(v,w,f)$ force $u=v=f=0$ and $w=1$. Give each signal $a$ a complementary variable with $R(a,\bar a,f)$. A NOT gate with output $z$ is $R(a,z,f)$. An AND gate with inputs $a,b$ and output $z$ uses fresh $u',v',w'$ in

$$
R(u',v',a),\qquad R(w',z,\bar a),\qquad R(v',z,\bar b).
$$

For $a=0$ the middle relation forces $z=w'=0$ and the last forces $v'=b$. For $a=1$ the first forces $u'=v'=0$ and the last gives $z=b$. In both cases all internal values are unique and $z=a\land b$. Also give unused inputs and witnesses their complement relation, so that every witness bit is represented.

Use the variable and clause blocks from the construction note. Attach one additional occurrence of each input signal to an isolated one-port column between zero-carry separators. Its edge bit must equal this column's target bit, which is set to the supplied input. Another one-port column pins the verifier output to one. These attachments extend the path forest by leaves.

For a fixed topology independent of the free input bits, use the following completion. Let the original positions be below $L$, let $T_{\mathrm{low}}<2^L$, and join consecutive path components using two new positions per connector, with all these positions assigned target zero. Close the last path to the first through five new positions at offsets $(0,2,3,4,1)$ in path order, starting at position $K$. Write $B=2^K$. The target is $29B+T_{\mathrm{low}}$. The closing path contributes local weights $(1,5,12,24,18,2)$ in units of $B$, where the first and last are terminal edges.

The sum below position $K$ is at most $2(B-1)$, so the carry into the closing block is zero or one. The six local weights reach 29 uniquely as $5+24$ and cannot reach 28. Thus the carry is zero, both terminal edges are unselected, and all earlier added connector edges are unselected because their weights would exceed $T_{\mathrm{low}}$. The completed graph and chosen high edges are independent of $x$. Every weight is below $29B$, and the complete construction preserves the witness count.

If all pins are constant, the alternating identities and connectors of the first note can be used instead. Taking a circuit whose free variables are the witnesses gives a parsimonious reduction from the parity of the satisfying-assignment count to the alternating-target class.

### Circuit consequences

The fixed topology places the Boolean input in individually specified target bits. A uniform polynomial-time preprocessing of the fixed weights followed by polynomial-time target queries would put CLIQUE, and hence NP, in P. Allowing arbitrary preprocessing of polynomial output length and polynomial-time queries would instead put NP in P/poly, giving the [Karp–Lipton collapse](https://pages.cs.wisc.edu/~jyc/02-810notes/lecture10.pdf).

The ordinary projection from free input bits to target bits transfers lower bounds for restricted circuit models. Compiling parity takes $N=\Theta(m)$ columns for $m$ input bits. Thus on one such family, depth-$d$ unbounded-fan-in AND/OR circuits with input negations require $2^{\Omega_d(N^{1/(d-1)})}$ size for fixed $d\ge2$, by [Håstad's parity bound](https://eccc.weizmann.ac.il/report/2019/073/).

Compiling an $O(m\log^3m)$-gate verifier for Harnik–Raz yields a monotone restriction on the free inputs with a monotone circuit lower bound of $2^{\Omega(\sqrt N/\log^{5/2}N)}$. The verifier guesses a small-degree polynomial over a field of prime size $m$, checks sufficient distinct evaluations, and looks up the input bit for each evaluation using an oblivious sorting network. The bound transfers [Cavalar, Kumar and Rossman's Harnik–Raz lower bound](https://eccc.weizmann.ac.il/report/2020/181/revision/2/download/). The technical drafts give the verifier's parameters and size accounting.

For fixed weights and target, the symbolic subset polynomial is $G(z)=\sum_{S:\,\sum_{e\in S}w_e=T}\prod_{e\in S}z_e$. There are one-cycle families for which $G$ requires $2^{\Omega(N)}$ gates in monotone arithmetic circuits. Use a positive-rate constant-alphabet code with linear-size verification and agreement below one third, and compile flags indicating each symbol of each codeword. The variable gadget's internal edge $q$ is selected precisely when its flag is true. Map its formal weight to the codeword's corresponding symbol variable and all other formal weights to one. This is a monotone projection onto the codeword polynomial, which has a circuit lower bound equal to the code size by [Cavalar, Kumar and Rossman, Theorem 7](https://pmc.ncbi.nlm.nih.gov/articles/PMC9705498/). Existence of codes with the required linear-size implementation follows from the sparse parity-check and constant-length sampling argument in the technical drafts. This lower bound concerns the symbolic polynomial.

## A proof-system separation at an alternating target

There are infeasible instances with the single-cycle alternating target for which the local carry CNF requires resolution size $2^{\Omega(N)}$. Sum-of-squares refutations of the single weighted equation with Boolean axioms require degree $\Omega(N)$ and explicit monomial size $2^{\Omega(N)}$. Cutting planes have polynomial-size refutations of the same weighted equation.

### Translate a Tseitin contradiction

On a bounded-degree expander with $n$ vertices, use one Boolean variable per graph edge and impose a prescribed parity $b_v$ at each vertex, with $\sum_v b_v$ odd. Over the whole graph each edge is counted twice, so the constraints are inconsistent. Split each prescribed parity into a chain of ternary XORs using prefix-parity variables. Each prefix variable occurs twice and the total charge is preserved.

For one ternary XOR, use three columns with target bits $(0,b,1)$, read least significant first. In the first column place the first input $a_1$ and a wire $u$, so with incoming carry zero both equal the outgoing carry. In the second column attach $a_2,a_3$. Its equation is $a_1+a_2+a_3=b+2q$. In the third attach one wire $z$, requiring $z=1-q$ and resetting the outgoing carry to zero. Terminate $u,z$ in the free-end blocks of [Note 01](01-alternating-target.md#the-initial-path-forest). Use the variable blocks to tie occurrences and zero separators between blocks. Then apply the alternating identities and cycle completion. As each source edge and prefix variable occurs a bounded number of times, the output has $N=\Theta(n)$.

The translation admits a bounded-locality substitution on every assignment, including assignments violating the source. Assign each prefix its actual parity. In a ternary test assign $q=\lfloor(a_1+a_2+a_3)/2\rfloor$, using the corresponding choices in all auxiliary blocks. A wrong parity creates a nonzero residue only in the central column of that test. After the prefix substitutions the only possible residues are at one column $j_v$ per original graph vertex. They are

$$
g_v(x)=\operatorname{parity}(x_{e:e\ni v})-b_v.
$$

Each substitution is a Boolean function of a constant number of source variables. The intermediate identities use the assigned incoming carry, and the connectors have constant choices.

### Resolution and sums of squares

Encode each target column by the clauses that forbid its invalid local truth-table rows. If this formula had a resolution refutation of width $w$, replace each variable by its local Boolean function and each clause by the canonical CNF of the substituted clause. An initial clause becomes a tautology or a consequence of one source parity. Each simulated inference involves only the source variables used by the two substituted premises, at most $O(w)$. Derive the necessary clauses by exhausting the remaining assignments on that support and resolving the unassigned bits away. This gives a source refutation of width $O(w)$. [Ben-Sasson and Wigderson](https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf) give linear source width and an exponential target size lower bound from linear width, bounded initial width and $O(N)$ variables.

Represent each substitution by its multilinear real polynomial $f_e$. Let $L(z)=\sum_e w_ez_e-T$. Multiplying the local residues by their bit weights and telescoping the carries gives the exact polynomial identity

$$
L(f(x))=\sum_v2^{j_v}g_v(x).
$$

The equality holds on the Boolean cube, and both sides are multilinear. The polynomial $g_v$ is a scalar multiple of the usual Tseitin polynomial constraint. Substituting into an SOS refutation preserves squares. Each Boolean residue $f_e^2-f_e$ lies in the source Boolean ideal with a constant-degree derivation by multilinear reduction. A target degree-$D$ proof would give a source proof of degree $O(D)$. The lower bound of [Grigoriev](https://logic.pdmi.ras.ru/~grigorev/pub/square_journal.pdf) therefore transfers. The [Atserias–Hakoniemi size–degree trade-off](https://drops.dagstuhl.de/storage/00lipics/lipics-vol137-ccc2019/LIPIcs.CCC.2019.24/LIPIcs.CCC.2019.24.pdf) gives the exponential monomial bound.

### Cutting planes

Every local implication used by the construction has a constant number of variables. One can derive it in cutting planes by excluding each invalid Boolean assignment with a linear clause, then eliminating the unneeded variables. To obtain a clause from a violated input inequality, use the Boolean bounds to upper-bound its slack by an integer multiple of the Hamming distance to the offending assignment and divide with rounding. Summing the two inequalities for clauses differing only on a variable and dividing by two gives their resolvent.

The local implications recover all copy equalities, all separator pins and the ternary parity equations. Summing these equations gives $2A=B$, where the affine integer form $A$ combines the repeated inputs and the quotients, and $B=\sum_v b_v$ is odd. Divide the two inequalities by two with rounding to get $A\ge\lceil B/2\rceil$ and $A\le\lfloor B/2\rfloor$.

The proof also works over the original weight variables. Use the integer affine form $\ell_i(z)=\sum_{j\ge i}2^{j-i}(t_j-s_j(z))$ for carry $i$. The column equations then hold identically. From $L=0$,

$$
2^i\ell_i=\sum_{j<i}2^j(s_j-t_j).
$$

Boolean bounds put the right side between $-(2^i-1)$ and $2(2^i-1)$. Division with rounding yields $0\le\ell_i\le1$, with both endpoint carries pinned to zero. Integer affine substitution commutes with the rounding rule, so the original cutting-planes proof can be written in the weight variables with polynomial bit length.

These circuit and proof-system results apply to the models stated above. The general decision question remains open.
