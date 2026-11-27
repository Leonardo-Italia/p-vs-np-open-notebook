"""Exact finite checks for the research notebook. Run with Python 3.10+."""

from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
from random import Random

from run_counting import count_by_runs


# Paths are listed in graph order, with column labels relative to each block.
IDENTITIES = {
    0: ((0, 4, 3, 1, 2), 10, ((10,), (17, 24))),
    1: ((0, 1, 3, 4, 5, 6, 2), 85, ((3, 10, 24, 48), (48, 96, 68))),
}
BRIDGE = ((0, 3, 2, 5, 1, 4), 21, (9, 12))
CLOSURE = ((0, 2, 3, 1, 5, 4, 6), 85, (5, 80))
A0 = ((0, 0, 0, 2), (2, 1, 1, 0), (0, -1, 1, 2), (-2, 1, 1, 0))
A1 = tuple((row[3], row[1], row[2], row[0]) for row in A0)
D0 = ((0, 2, -2, 2), (1, 1, 1, 0), (0, -2, 2, 0), (-1, 1, 1, 0))
D1 = tuple((row[3], row[1], row[2], row[0]) for row in D0)


def bit(integer, index):
    return (integer >> index) & 1


def weights(edges):
    return [(1 << u) + (1 << v) for u, v in edges]


def target(bits):
    return sum(value << i for i, value in enumerate(bits))


def add_block(bits, pattern, separator=True):
    start = len(bits)
    bits.extend(pattern)
    if separator:
        bits.append(0)
    return start


def core(clauses):
    """Reduce a nonempty positive exact-one 3-CNF to a forest of paths."""
    bits, edges = [], []
    occurrences = {}
    for clause_index, clause in enumerate(clauses):
        for literal_index, name in enumerate(clause):
            occurrences.setdefault(name, []).append(3 * clause_index + literal_index)
    ports = {}
    for positions in occurrences.values():
        k = len(positions)
        start = add_block(bits, [0] * k + [1, 1])
        ports.update((position, start + j) for j, position in enumerate(positions))
        edges.extend(((start, start + k + 1), (start + k, start + k + 1)))
    for clause_index in range(len(clauses)):
        col = add_block(bits, (0, 1))
        cap = add_block(bits, (0, 1, 1))
        i = 3 * clause_index
        edges.extend(
            ((col, ports[i]), (col + 1, ports[i + 1]), (col + 1, ports[i + 2]),
             (col, cap), (cap, cap + 2), (cap + 1, cap + 2))
        )
    return bits, edges


def path_ends(size, edges):
    adjacent = [[] for _ in range(size)]
    for u, v in edges:
        adjacent[u].append(v)
        adjacent[v].append(u)
    assert all(len(neighbors) <= 2 for neighbors in adjacent)
    seen, paths = set(), []
    for start, neighbors in enumerate(adjacent):
        if start in seen or len(neighbors) > 1:
            continue
        current = start
        while current is not None:
            seen.add(current)
            last = current
            current = next((v for v in adjacent[current] if v not in seen), None)
        paths.append((start, last))
    assert len(seen) == size, "the components must be paths, including singletons"
    return paths


def alternating_cycle(original_bits, original_edges):
    """Insert carry identities, then connect the path components into one cycle."""
    bits, edges, translated = [], [], []

    def insert(path, local_target, tails=()):
        start = add_block(bits, (bit(local_target, j) for j in range(len(path))), False)
        order = [start + j for j in path]
        if tails:
            order = [tails[0], *order, tails[1]]
        edges.extend(zip(order, order[1:]))

    for value in original_bits:
        if bits and bits[-1] == value:
            path, local_target, _ = IDENTITIES[1 - value]
            insert(path, local_target)
        translated.append(len(bits))
        bits.append(value)
    edges.extend((translated[u], translated[v]) for u, v in original_edges)
    paths = path_ends(len(bits), edges)
    for (_, end), (start, _) in zip(paths, paths[1:]):
        insert(*BRIDGE[:2], (end, start))
    insert(*CLOSURE[:2], (paths[-1][1], paths[0][0]))
    return bits, edges


def assert_cycle(bits, edges):
    size = len(bits)
    assert size >= 6 and size % 2 == 0
    assert bits == [j % 2 for j in range(size)]
    assert len(edges) == len(set(map(frozenset, edges))) == size
    adjacent = [set() for _ in bits]
    for u, v in edges:
        assert u != v
        adjacent[u].add(v)
        adjacent[v].add(u)
    assert all(len(neighbors) == 2 for neighbors in adjacent)
    pending, seen = [0], {0}
    for u in pending:
        for v in adjacent[u] - seen:
            seen.add(v)
            pending.append(v)
    assert len(seen) == size
    assert target(bits) == 2 * ((1 << size) - 1) // 3
    assert max(weights(edges)) < target(bits)


def count_subsets(items, total):
    """Independent exact integer search with suffix bounds."""
    items = sorted(items, reverse=True)
    suffix = [0] * (len(items) + 1)
    for i in range(len(items) - 1, -1, -1):
        suffix[i] = items[i] + suffix[i + 1]
    memo = {}

    def count(i, remaining):
        if remaining == 0:
            return 1
        if remaining < 0 or remaining > suffix[i]:
            return 0
        key = (i, remaining)
        if key not in memo:
            memo[key] = count(i + 1, remaining) + count(i + 1, remaining - items[i])
        return memo[key]

    return count(0, total)


def count_formula(clauses):
    names = sorted(set().union(*map(set, clauses)))
    return sum(
        all(sum(assignment[v] for v in clause) == 1 for clause in clauses)
        for values in product((0, 1), repeat=len(names))
        for assignment in (dict(zip(names, values)),)
    )


def check_block_tables():
    for path, local_target, configurations in (*IDENTITIES.values(), BRIDGE, CLOSURE):
        is_identity = (path, local_target, configurations) in IDENTITIES.values()
        items = weights(zip(path, path[1:]))
        if not is_identity:
            items = [1 << path[0], *items, 1 << path[-1]]
        for incoming in (0, 1):
            for outgoing in (0, 1):
                required = local_target + (outgoing << len(path)) - incoming
                found = [
                    tuple(w for w, chosen in zip(items, bits) if chosen)
                    for bits in product((0, 1), repeat=len(items))
                    if sum(w * chosen for w, chosen in zip(items, bits)) == required
                ]
                if is_identity and incoming == outgoing:
                    expected = [configurations[incoming]]
                elif not is_identity and incoming == outgoing == 0:
                    expected = [configurations]
                else:
                    expected = []
                assert found == expected, (path, incoming, outgoing, found)


def check_alternating_reduction():
    check_block_tables()
    atoms = list(combinations_with_replacement(range(3), 3))
    formulas = [(a,) for a in atoms] + list(combinations_with_replacement(atoms, 2))
    rng = Random(73501)
    formulas.extend(
        tuple(tuple(rng.randrange(6) for _ in range(3)) for _ in range(rng.randint(3, 5)))
        for _ in range(100)
    )
    positive, max_columns = 0, 0
    for formula in formulas:
        original_bits, original_edges = core(formula)
        bits, edges = alternating_cycle(original_bits, original_edges)
        assert_cycle(bits, edges)
        expected = count_formula(formula)
        assert count_subsets(weights(original_edges), target(original_bits)) == expected
        assert count_subsets(weights(edges), target(bits)) == expected, formula
        positive += bool(expected)
        max_columns = max(max_columns, len(bits))
    return len(formulas), positive, max_columns


def degree_vectors(bits):
    def visit(i, carry, degrees):
        if i == len(bits):
            if not carry:
                yield degrees
            return
        for following in (0, 1):
            degree = bits[i] + 2 * following - carry
            if 0 <= degree <= 2:
                yield from visit(i + 1, following, (*degrees, degree))

    return visit(0, 0, ())


def cycle_penalty(cycle, degrees, seed):
    value, score = seed, 0
    for vertex in cycle:
        value = degrees[vertex] - value
        score += value * (value - 1)
    return score + (value - seed) ** 2


def check_cycle_counting():
    rng = Random(841)
    cases, multiple, schedules = 0, 0, 0
    for size in range(3, 13):
        for _ in range(24):
            vertices = list(range(size))
            rng.shuffle(vertices)
            cycles = [vertices]
            if size >= 6 and rng.randrange(2):
                cut = rng.randrange(3, size - 2)
                cycles = [vertices[:cut], vertices[cut:]]
            edges = [(v, cycle[(i + 1) % len(cycle)])
                     for cycle in cycles for i, v in enumerate(cycle)]
            wanted = rng.randrange(1 << size)
            found = 0
            for degrees in degree_vectors([bit(wanted, j) for j in range(size)]):
                schedules += 1
                scores = [(cycle_penalty(c, degrees, 0), cycle_penalty(c, degrees, 1))
                          for c in cycles]
                if sum(a * b for a, b in scores) == 0:
                    free = sum(a == b == 0 for a, b in scores)
                    assert free == sum(len(c) % 2 == 0 and all(degrees[v] == 1 for v in c)
                                       for c in cycles)
                    found += 1 << free
            assert found == count_subsets(weights(edges), wanted)
            cases += 1
            multiple += len(cycles) > 1
    return cases, multiple, schedules


def check_open_matchgates():
    for t, matrix in enumerate((A0, A1)):
        # Exterior coordinate order is incoming carry, the two choices, outgoing carry.
        phi = {0: 1, 4: 1, 3: 1, 10: 1, 7: 1, 14: -1}
        for c, d, slot in product(range(2), range(2), range(4)):
            lhs = sum(matrix[slot][ab] for ab in range(4)
                      if ab.bit_count() + c == t + 2 * d)
            index = c | (slot << 1) | (d << 3)
            assert lhs == 2 * phi.get(index ^ (1 if t else 8), 0)
    checked = 0
    for length in range(1, 4):
        for target_word in product((0, 1), repeat=length):
            v = []
            for state in range(1 << (2 * length)):
                dp = [1, 0]
                for i, t in enumerate(target_word):
                    row = (A0, A1)[t][(state >> (2 * i)) & 3]
                    dp = [
                        sum(dp[c] * sum(row[ab] for ab in range(4)
                                        if ab.bit_count() + c == t + 2 * d)
                            for c in (0, 1))
                        for d in (0, 1)
                    ]
                v.append(dp[0])
            for parity in (0, 1):
                signature = [x if i.bit_count() % 2 == parity else 0 for i, x in enumerate(v)]
                for a, b in product(range(len(v)), repeat=2):
                    different = a ^ b
                    value, sign = 0, 1
                    while different:
                        low_bit = different & -different
                        value += sign * signature[a ^ low_bit] * signature[b ^ low_bit]
                        different ^= low_bit
                        sign = -sign
                    assert value == 0
                    checked += 1
    return checked


def rank_mod(matrix_columns, modulus=1009):
    basis = {}
    for column in matrix_columns:
        v = [x % modulus for x in column]
        for i, a in enumerate(v):
            if not a:
                continue
            if i not in basis:
                inv = pow(a, -1, modulus)
                basis[i] = [x * inv % modulus for x in v]
                break
            w = basis[i]
            for j in range(i, len(v)):
                v[j] = (v[j] - a * w[j]) % modulus
    return len(basis)


def clifford_word(values, word):
    for operator in reversed(word):
        mask = 1 << (operator // 2)
        prefix = (mask << (operator % 2)) - 1
        values = [(-1 if ((j ^ mask) & prefix).bit_count() % 2 else 1) * values[j ^ mask]
                  for j in range(len(values))]
    return values


def check_triangle_rank():
    # D is 4 A^{-T}; check the normalization before evaluating the closed triangle.
    for a, d in ((A0, D0), (A1, D1)):
        for i, j in product(range(4), repeat=2):
            assert sum(a[k][i] * d[k][j] for k in range(4)) == 4 * (i == j)
    vectors = []
    for state in range(64):
        total = 0
        for assignment in range(8):
            term = 1
            for i, matrix in enumerate((D1, D1, D0)):
                local_choice = bit(assignment, i) + 2 * bit(assignment, (i - 1) % 3)
                term *= matrix[(state >> (2 * i)) & 3][local_choice]
            total += term
        vectors.append(total)
    assert sum(x * x for x in vectors) == 2616
    columns, ranks = [], []
    for degree in range(4):
        columns.extend(clifford_word(vectors, w) for w in combinations(range(12), degree))
        ranks.append(rank_mod(columns))
    assert ranks == [1, 13, 63, 64], ranks
    return ranks


def check_local_constraints():
    cases = 0
    examples = (
        ((2, 2, 2), (1, 1, 1), 1),
        ((3, 4, 5), (1, 2, 3), 1),
        ((2,) * 6, (1,) * 6, 2),
    )
    for sizes, forbidden, group_size in examples:
        for values in product(*(range(size) for size in sizes)):
            matches = tuple(value == blocked for value, blocked in zip(values, forbidden))
            a, b, c = (
                all(matches[i:i + group_size]) for i in range(0, len(matches), group_size)
            )
            degrees = (int(a), 1 - b, 1 - a, int(b), 1 - c, 1 - c)
            solutions = sum(
                all(wires[j - 1] + wires[j] == degree for j, degree in enumerate(degrees))
                for wires in product((0, 1), repeat=len(degrees))
            )
            assert solutions == (values != forbidden), (values, solutions)
            cases += 1
    return cases


def smallest_forbidden_triple_cycle():
    assignments = tuple(product((0, 1), repeat=3))
    degree_profiles = {
        tuple(table[assignment[variable]] for assignment in assignments)
        for variable in range(3)
        for table in product(range(3), repeat=2)
    }
    dead = (-1, -1)
    frontier = {((0, 1),) * len(assignments)}
    for length in range(1, 7):
        advanced = set()
        for state in frontier:
            for profile in degree_profiles:
                updated = tuple(
                    tuple(degree - bit if bit != -1 and 0 <= degree - bit <= 1 else -1
                          for bit in wire_map)
                    for wire_map, degree in zip(state, profile)
                )
                # An allowed assignment with neither entering bit feasible
                # cannot be recovered by adding columns.
                if dead not in updated[:-1]:
                    advanced.add(updated)
        frontier = advanced
        if length >= 3:
            for state in frontier:
                accepted = tuple(zero == 0 or one == 1 for zero, one in state)
                if all(accepted[:-1]) and not accepted[-1]:
                    return length
    raise AssertionError("No cycle for the isolated forbidden triple through length six")


def check_connected_dual_rank():
    # Pair indices are x + 2*y in the local port order.
    caps = ((0, 2, -1, 0), (0, 2, 1, 0))
    projected = tuple(
        tuple(sum(cap[k] * D0[k][p] for k in range(4)) for p in range(4))
        for cap in caps
    )
    assert projected == ((2, 4, 0, 0), (2, 0, 4, 0))

    def port_index(incoming, outgoing, swapped):
        if swapped:
            return outgoing + 2 * incoming
        return incoming + 2 * outgoing

    def column(matrix, row, swapped):
        return tuple(matrix[row][port_index(a, b, swapped)]
                     for b, a in product((0, 1), repeat=2))

    def active_columns(state, swaps):
        return tuple(column(matrix, (state >> (2 * j)) & 3, swaps[j])
                     for j, matrix in enumerate((D1, D0, D1)))

    vectors = {}
    for swaps in product((0, 1), repeat=3):
        values = []
        for state in range(64):
            first, second, third = active_columns(state, swaps)
            value = sum(
                first[2 * a] * second[a + 2 * b] * third[b + 2 * c] * (1 + c)
                for a, b, c in product((0, 1), repeat=3)
            )
            values.append(value)
        prior_words = []
        ranks = []
        for degree in range(4):
            prior_words.extend(clifford_word(values, word)
                               for word in combinations(range(12), degree))
            ranks.append(rank_mod(prior_words))
        assert ranks == [1, 13, 63, 64], (swaps, ranks)
        vectors[swaps] = values

    def cycle_trace(factors):
        result = (1, 0, 0, 1)
        for factor in factors:
            result = tuple(
                sum(result[a + 2 * k] * factor[k + 2 * b] for k in (0, 1))
                for b, a in product((0, 1), repeat=2)
            )
        return result[0] + result[3]

    patterns = (
        ((0, (0, 0, 0)),),
        ((0, (0, 0, 1)), (1, (1, 0, 1))),
    )
    compared = 0
    for pattern in patterns:
        for states in product(range(64), repeat=len(pattern)):
            factors, expected = [], 1
            for (sep_swap, swaps), state in zip(pattern, states):
                factors.append(tuple(projected[sep_swap][port_index(a, b, sep_swap)]
                                     for b, a in product((0, 1), repeat=2)))
                factors.extend(active_columns(state, swaps))
                expected *= 2 * vectors[swaps][state]
            assert cycle_trace(factors) == expected, (pattern, states)
            compared += 1

    for blocks in range(1, 6):
        size = 4 * blocks
        edges = [(j, (j + 1) % size) for j in range(size)]
        alternating = 2 * ((1 << size) - 1) // 3
        assert count_subsets(weights(edges), alternating) == (2 if blocks % 3 == 0 else 0)
    return len(vectors), compared


def check_run_frontiers():
    rng = Random(757)

    def check(cycle, wanted):
        size = len(cycle)
        target_bits = [bit(wanted, i) for i in range(size)]
        edges = [(v, cycle[(i + 1) % size]) for i, v in enumerate(cycle)]
        expected = count_subsets(weights(edges), wanted)
        runs = 1 + sum(a != b for a, b in zip(target_bits, target_bits[1:]))
        order = list(range(runs))
        rng.shuffle(order)
        assert count_by_runs(target_bits, cycle) == expected, (target_bits, cycle)
        assert count_by_runs(target_bits, cycle, order) == expected, (target_bits, cycle, order)

    exhaustive = 0
    for size in range(3, 6):
        for tail in permutations(range(1, size)):
            cycle = (0, *tail)
            if cycle[1] > cycle[-1]:
                continue  # A cycle and its reversal have the same weights.
            for wanted in range(1 << size):
                check(cycle, wanted)
                exhaustive += 1

    sampled = 0
    for size in range(3, 13):
        for _ in range(24):
            cycle = list(range(size))
            rng.shuffle(cycle)
            check(cycle, rng.randrange(1 << size))
            sampled += 1
    return exhaustive, sampled


def main():
    formula_count, positive, largest = check_alternating_reduction()
    print(f"Alternating target: {formula_count} formulas; {positive} positive; up to {largest} columns")
    cases, multiple, schedules = check_cycle_counting()
    print(f"Carry counting: {cases} instances; {multiple} with multiple cycles; {schedules} schedules")
    print(f"Open chain: {check_open_matchgates()} matchgate identities")
    print(f"Dual triangle: cumulative ranks modulo 1009 = {check_triangle_rank()}")
    port_orders, projected_coefficients = check_connected_dual_rank()
    print(f"Connected dual: {port_orders} port orders; {projected_coefficients} projected coefficients")
    local_cases = check_local_constraints()
    smallest = smallest_forbidden_triple_cycle()
    assert smallest == 6, smallest
    print(f"Local constraints: {local_cases} gadget assignments; shortest cycle {smallest} columns")
    exhaustive, sampled = check_run_frontiers()
    print(f"Run frontiers: {exhaustive} exhaustive and {sampled} sampled instances in two orders")


if __name__ == "__main__":
    main()
