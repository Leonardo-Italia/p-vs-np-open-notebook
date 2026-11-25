# Exact counting with trees of target runs

**Algorithm, separation, and executable checks.** [Note 06](06-run-cutwidth.md) contracts the target runs in a linear order. Here a binary tree groups them. For an explicit family of single-cycle instances, the best linear order can have a boundary logarithmically larger than the best tree.

## The tree and its width

Use the same multigraph $G$ as in [Note 06](06-run-cutwidth.md#the-width-parameter). Its vertices are maximal runs of equal target bits. A selection wire between different runs contributes an edge, and each boundary between consecutive runs in bit order contributes a carry edge. Parallel edges are distinct wires. For a subset $S$ of runs, write $\delta(S)$ for the set of wires with exactly one end in $S$.

Let a rooted binary tree have one leaf per run. Each node represents the set $S$ of its descendant leaves. Its table records, for each assignment on $\delta(S)$, the number of compatible configurations in $S$. Write $W$ for the largest $|\delta(S)|$ over the nodes. Minimizing $W$ over such trees gives the carving width of $G$. This is the edge congestion parameter in [O'Gorman, Parameterization of Tensor Network Contraction](https://doi.org/10.4230/LIPIcs.TQC.2019.10). The setting here uses the run structure to build the leaf tables and to realize the width separation within single-cycle Subset Sum.

## Exact counting

For one run of length $\ell$, there are $\ell+2$ carry options. Each fixes its two carry endpoints. With an option fixed, the induced path fragments of the selection cycle act as partial bijections on their endpoint bits. Sum the corresponding tests over the options to fill the leaf table. Across options in bit order at most two column degrees change at a time, so the balanced transfer trees of Note 06 maintain the fragment maps in total $O(N\log(N+1))$ operations. Testing one option against one assignment on its leaf cut takes $O(W+1)$ operations. The one-run case uses the trace of the whole cycle transfer with external carries zero.

At an internal node, let $A,B$ be the two child sets and $C$ the remaining runs. The wires between $A,B$ are indexed by $i$, those between $A,C$ by $j$, and those between $B,C$ by $k$. Each index is an assignment to all wires of the corresponding class. The merge is

```math
T_{A\cup B}(j,k)=\sum_i T_A(i,j)\,T_B(i,k).
```

All constraints internal to one child were already enforced. The sum gives each common wire a consistent bit. At the root the boundary is empty, and each subset has unique selection bits and carries. The table contains the exact subset count.

If the three classes have sizes $a,b,c$, then $a+b,a+c,b+c\le W$. Direct merging costs $O(2^{a+b+c})$ arithmetic operations, at most $O(2^{3W/2})$. For faster merging, view the expression as multiplication of a $2^b$ by $2^a$ matrix and a $2^a$ by $2^c$ matrix. Let $m=\min(a,b,c)$. Split all dimensions into blocks of size $2^m$. With [Strassen's integer matrix multiplication](https://doi.org/10.1007/BF02165411), the cost is

```math
O\!\left(2^{\,a+b+c-3m} 2^{\,m\log_2 7}\right)
\ \le\ O\!\left(2^{\,W\log_2(7)/2}\right).
```

The largest two sizes sum to at most $W$, and $m\le W/2$. The leaf construction, wiring and table packing, and the $r-1$ merges give

```math
O\!\left(N\log(N+1)+N(W+1)2^W+r\,2^{\,W\log_2(7)/2}\right)
```

arithmetic operations for a supplied tree. The finite checker below uses direct merging and enumerates leaf selections for its small leaves. The displayed faster bound uses the transfer trees and matrix multiplication in the proof.

## How much can a tree improve the width?

Let $`W_*`$ and $`L_*`$ denote the smallest tree width and smallest linear width, respectively. For $r\ge2$,

```math
W_*\le 2L_*,\qquad L_*\le W_*\lfloor\log_2 r\rfloor.
```

For the first bound, use the binary tree whose internal groups are the successive prefixes of an optimal linear order. Internal cuts have at most $`L_*`$ wires. The singleton for a run has at most $`2L_*`$ incident wires, since every one crosses the cut immediately before or after that run.

For the second bound, start from an optimal tree and recursively visit the child with more leaves first, breaking ties arbitrarily. For any proper prefix of the resulting leaf order, follow the path from the root to its first unvisited leaf. The prefix is the disjoint union of the first-child subtrees whose second-child subtrees contain that leaf. Every such descent is into a subtree with at most half as many leaves, so there are at most $\lfloor\log_2 r\rfloor$ of them. Each subtree has at most $`W_*`$ outgoing wires, which bounds the outgoing wires of their union.

## A logarithmic separation on a single cycle

Let $B_h$ be a complete binary tree of height $h\ge1$, with $r=2^{h+1}-1$ vertices. Replace each edge by $2q$ parallel edges, for an integer $q\ge1$, and take an Euler circuit. Make one bit column for every departure on this circuit. Group the columns for each vertex contiguously in bit order, with the groups in preorder of $B_h$. Give successive groups alternating target bits. In selection order put the columns along the Euler circuit. The bit columns are distinct, so this gives a single simple selection cycle. Its quotient by target runs is the doubled-and-repeated tree with the preorder carry path added.

Build a binary grouping tree by first merging each vertex with its full left subtree and then adding its full right subtree. The groups so formed are singletons, full rooted subtrees, and a vertex together with its left subtree. They are intervals of the preorder and have at most two carry wires leaving each group. At most three original binary-tree edges leave any group. The grouping tree has width at most $6q+2$. For $h\ge2$ a nonroot internal vertex has three binary-tree neighbors and two preorder neighbors counted as wires. Its singleton cut has exactly $6q+2$ wires, so $`W_*=6q+2`$.

The linear cutwidth of $B_h$ is at least $\lceil h/2\rceil$. To see this, take any linear order and the four subtrees rooted at the grandchildren. Choose one whose first vertex is not the earliest first vertex and whose last vertex is not the latest last vertex among the four. A cut attaining its internal width occurs with some exterior vertex already processed and another exterior vertex still unprocessed. The complement of the chosen subtree is connected, giving at least one extra crossing edge outside it. Thus the linear cutwidth increases by at least one from height $h-2$ to height $h$. The base widths are zero for height zero and at least one for height one. Parallel edges now give

```math
L_*\ge 2q\lceil h/2\rceil.
```

Together with the general comparison, this gives a worst-case ratio $`L_*/W_*=\Theta(\log r)`$ on these instances. The same quotient can be realized on a satisfiable instance by replacing each Euler visit by two consecutive columns of its run. Choose the internal edge of each two-column visit in a one run and no other edges. Every target bit then matches its selection degree with carries zero.

For $h=9$ and $q=1$, the satisfiable construction has 1,023 runs and 4,088 columns. Its tree width is 8 and every linear order has width at least 10. The bound in the number of runs alone remains open.

## Reproduction

The following small-instance checker compares the tree count with direct integer subset enumeration on 270 seeded instances in two trees apiece. It computes the exact minimum linear width on six small members of the separation family using a subset dynamic program. It also counts the satisfiable instance with 4,088 columns. Copy the JavaScript block into a file and run it with Node.js.

<details>
<summary>Executable checker</summary>

```javascript
function runsOf(bits) {
  const labels = [0];
  for (let i = 1; i < bits.length; i++) {
    labels.push(labels.at(-1) + Number(bits[i] !== bits[i - 1]));
  }
  return labels;
}

function instance(bits, cycle) {
  const labels = runsOf(bits);
  const selection = cycle.map((v, i) => [v, cycle[(i + 1) % cycle.length]]);
  const byRun = Array.from({ length: labels.at(-1) + 1 }, () =>
    ({ columns: [], boundary: [], internal: [], entering: null, exiting: null }));
  const edgesAt = bits.map(() => []);
  for (const [v, run] of labels.entries()) byRun[run].columns.push(v);
  const wires = selection.map(([u, v], id) => {
    edgesAt[u].push(id);
    edgesAt[v].push(id);
    const a = labels[u], b = labels[v];
    if (a === b) byRun[a].internal.push(id);
    else {
      byRun[a].boundary.push(id);
      byRun[b].boundary.push(id);
    }
    return [a, b];
  });
  for (let v = 1; v < bits.length; v++) {
    const a = labels[v - 1], b = labels[v];
    if (a === b) continue;
    const id = wires.length;
    byRun[a].exiting = id;
    byRun[b].entering = id;
    byRun[a].boundary.push(id);
    byRun[b].boundary.push(id);
    wires.push([a, b]);
  }
  return { bits, labels, selection, wires, byRun, edgesAt };
}

function binaryAssignments(ids) {
  return Array.from({ length: 2 ** ids.length }, (_, mask) =>
    new Map(ids.map((id, i) => [id, (mask >> i) & 1])));
}

function leafTable(data, run) {
  const { bits, byRun, edgesAt } = data;
  const { boundary, columns, internal, entering, exiting } = byRun[run];
  const inside = binaryAssignments(internal);
  const values = binaryAssignments(boundary).map(exterior => {
    const first = entering === null ? 0 : exterior.get(entering);
    const last = exiting === null ? 0 : exterior.get(exiting);
    let accepted = 0n;
    for (const interior of inside) {
      let carry = first;
      for (const v of columns) {
        const degree = edgesAt[v].reduce((sum, id) =>
          sum + (interior.get(id) ?? exterior.get(id)), 0);
        carry = (degree + carry - bits[v]) / 2;
        if (carry !== 0 && carry !== 1) break;
      }
      if (carry === last) accepted++;
    }
    return accepted;
  });
  return { boundary, values, width: boundary.length };
}

function countOnTree(data, tree) {
  if (Number.isInteger(tree)) return leafTable(data, tree);
  const a = countOnTree(data, tree[0]);
  const b = countOnTree(data, tree[1]);
  const boundary = [...a.boundary.filter(id => !b.boundary.includes(id)),
                    ...b.boundary.filter(id => !a.boundary.includes(id))];
  const shared = binaryAssignments(a.boundary.filter(id => b.boundary.includes(id)));
  const values = binaryAssignments(boundary).map(outside => {
    let count = 0n;
    for (const joined of shared) {
      const bits = new Map([...outside, ...joined]);
      const index = ids => ids.reduce((sum, id, i) => sum + bits.get(id) * (2 ** i), 0);
      count += a.values[index(a.boundary)] * b.values[index(b.boundary)];
    }
    return count;
  });
  return { boundary, values, width: Math.max(boundary.length, a.width, b.width) };
}

function directCount(data) {
  const weights = data.selection.map(([a, b]) => (1n << BigInt(a)) + (1n << BigInt(b)));
  const target = data.bits.reduce((sum, bit, i) => sum + (BigInt(bit) << BigInt(i)), 0n);
  let count = 0n;
  for (let mask = 0; mask < 2 ** weights.length; mask++) {
    let total = 0n;
    for (let i = 0; i < weights.length; i++) {
      if ((mask >> i) & 1) total += weights[i];
    }
    if (total === target) count++;
  }
  return count;
}

function binaryTree(order) {
  if (order.length === 1) return order[0];
  const mid = Math.floor(order.length / 2);
  return [binaryTree(order.slice(0, mid)), binaryTree(order.slice(mid))];
}

function binaryFamily(height, q, columnsPerVisit = 1) {
  const neighbors = [];
  function make(depth) {
    const root = neighbors.length;
    neighbors.push([]);
    if (!depth) return { root, tree: root };
    const left = make(depth - 1);
    const right = make(depth - 1);
    for (const child of [left.root, right.root]) {
      neighbors[root].push(child);
      neighbors[child].push(root);
    }
    return { root, tree: [[root, left.tree], right.tree] };
  }
  const { tree } = make(height);
  const visits = [];
  function tour(v, parent) {
    for (const child of neighbors[v]) {
      if (child === parent) continue;
      visits.push(v);
      tour(child, v);
      visits.push(child);
      for (let copy = 1; copy < q; copy++) visits.push(v, child);
    }
  }
  tour(0, -1);
  const bits = [], slots = [];
  for (const [run, adjacent] of neighbors.entries()) {
    slots[run] = [];
    for (let j = 0; j < q * adjacent.length; j++) {
      const block = [];
      for (let k = 0; k < columnsPerVisit; k++) {
        block.push(bits.length);
        bits.push(run % 2);
      }
      slots[run].push(block);
    }
  }
  const cycle = visits.flatMap(v => slots[v].pop());
  if (new Set(cycle).size !== bits.length || cycle.includes(undefined)) throw new Error("Cycle construction");
  return { data: instance(bits, cycle), tree };
}

function bestLinearWidth(data) {
  const r = data.labels.at(-1) + 1;
  const costs = new Uint16Array(2 ** r);
  for (let mask = 1; mask < costs.length; mask++) {
    let prior = Infinity;
    for (let j = 0; j < r; j++) {
      if ((mask >> j) & 1) prior = Math.min(prior, costs[mask ^ (1 << j)]);
    }
    const cut = data.wires.reduce((size, [a, b]) =>
      size + (((mask >> a) ^ (mask >> b)) & 1), 0);
    costs[mask] = Math.max(prior, cut);
  }
  return costs.at(-1);
}

function verify() {
  function require(condition, label) {
    if (!condition) throw new Error(label);
  }
  let state = 2879;
  function random(limit) {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return (state >>> 8) % limit;
  }
  function shuffled(values) {
    const result = values.slice();
    for (let i = result.length - 1; i > 0; i--) {
      const j = random(i + 1);
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }
  let cases = 0;
  for (let n = 3; n <= 11; n++) {
    for (let j = 0; j < 30; j++) {
      const cycle = shuffled(Array.from({ length: n }, (_, i) => i));
      const bits = Array.from({ length: n }, () => random(2));
      const data = instance(bits, cycle);
      const order = Array.from({ length: data.labels.at(-1) + 1 }, (_, i) => i);
      const expected = directCount(data);
      for (const ordering of [order, shuffled(order)]) {
        const result = countOnTree(data, binaryTree(ordering));
        require(result.boundary.length === 0 && result.values[0] === expected, "Count mismatch");
      }
      cases++;
    }
  }
  const widths = [];
  for (let h = 1; h <= 3; h++) {
    for (const q of [1, 2]) {
      const { data, tree } = binaryFamily(h, q);
      const result = countOnTree(data, tree);
      const linear = bestLinearWidth(data);
      require(result.width <= 6*q + 2 && linear >= 2*q*Math.ceil(h/2), "Width bound failed");
      if (h >= 2) require(result.width === 6*q + 2, "Singleton width mismatch");
      if (data.bits.length <= 12) require(result.values[0] === directCount(data), "Family count mismatch");
      widths.push([h, q, result.width, linear]);
    }
  }
  const big = binaryFamily(9, 1, 2);
  const largeCount = countOnTree(big.data, big.tree);
  require(largeCount.boundary.length === 0 && largeCount.width === 8, "Large family width");
  require(largeCount.values[0] > 0n, "Paired visits must admit a zero-carry solution");
  return {
    cases, widths,
    large: {
      runs: big.data.labels.at(-1) + 1,
      columns: big.data.bits.length,
      width: largeCount.width,
      solutions: largeCount.values[0].toString(),
    },
  };
}



console.log(verify());
```

</details>
