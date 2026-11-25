"""Exact Subset Sum counting on a single selection cycle, by target runs."""

from itertools import groupby


IDENTITY = (0, 1)
DEGREE_WIRES = ((0, -1), (1, 0), (-1, 1))


def compose(left, right):
    """Read the two partial wire maps from left to right."""
    return tuple(-1 if bit < 0 else right[bit] for bit in left)


class Fragment:
    """Balanced product of the degree maps of one cyclic fragment."""

    def __init__(self, vertices, incoming, outgoing):
        self.vertices = vertices
        self.incoming = incoming
        self.outgoing = outgoing
        self.offset = 1 << (len(vertices) - 1).bit_length()
        self.tree = [IDENTITY] * (2 * self.offset)
        self.tree[self.offset:self.offset + len(vertices)] = [DEGREE_WIRES[1]] * len(vertices)
        for node in range(self.offset - 1, 0, -1):
            self.tree[node] = compose(self.tree[2 * node], self.tree[2 * node + 1])

    def assign(self, position, degree):
        node = self.offset + position
        self.tree[node] = DEGREE_WIRES[degree]
        while node > 1:
            node //= 2
            self.tree[node] = compose(self.tree[2 * node], self.tree[2 * node + 1])


def cycle_fragments(cycle, run_of, run_count):
    by_run = [[] for _ in range(run_count)]
    cut = next((i for i, v in enumerate(cycle) if run_of[cycle[i - 1]] != run_of[v]), None)
    if cut is None:
        by_run[0].append(Fragment(cycle, None, None))
        return by_run
    rotated = cycle[cut:] + cycle[:cut]
    previous = rotated[-1]
    for run, block in groupby(rotated, key=run_of.__getitem__):
        vertices = tuple(block)
        by_run[run].append(Fragment(vertices, previous, vertices[-1]))
        previous = vertices[-1]
    return by_run


def run_options(vertices, target_bit, fragments):
    """Yield boundary carries and fragment maps, updating at most two vertices."""
    locations = {
        vertex: (fragment, position)
        for fragment in fragments
        for position, vertex in enumerate(fragment.vertices)
    }
    free_carry = 1 - target_bit
    pinned_degree = 2 * target_bit
    yield free_carry, free_carry, tuple(fragment.tree[1] for fragment in fragments)
    previous = None
    for vertex in vertices:
        if previous is not None:
            fragment, position = locations[previous]
            fragment.assign(position, pinned_degree)
        fragment, position = locations[vertex]
        fragment.assign(position, 2 - pinned_degree)
        yield target_bit, free_carry, tuple(fragment.tree[1] for fragment in fragments)
        previous = vertex
    fragment, position = locations[previous]
    fragment.assign(position, pinned_degree)
    yield target_bit, target_bit, tuple(fragment.tree[1] for fragment in fragments)


def bit(mask, position):
    return (mask >> position) & 1


def agrees(mask, fixed, pairs):
    return (all(bit(mask, i) == value for i, value in fixed)
            and all(mapping[bit(mask, i)] == bit(mask, j) for i, j, mapping in pairs))


def invert(mapping):
    return tuple(next((i for i, out in enumerate(mapping) if out == b), -1)
                 for b in (0, 1))


def add_option(old, updated, old_positions, new_positions, fragments, mappings, carry_pins):
    old_pairs, new_pairs, mixed_pairs = [], [], []
    for fragment, mapping in zip(fragments, mappings):
        left, right = fragment.incoming, fragment.outgoing
        if left in old_positions and right in old_positions:
            old_pairs.append((old_positions[left], old_positions[right], mapping))
        elif left in new_positions and right in new_positions:
            new_pairs.append((new_positions[left], new_positions[right], mapping))
        elif left in old_positions:
            mixed_pairs.append((old_positions[left], new_positions[right], mapping))
        else:
            mixed_pairs.append((old_positions[right], new_positions[left], invert(mapping)))

    old_pins, new_pins = [], []
    for wire, value in carry_pins:
        if wire is None:
            if value != 0:
                return
        elif wire in old_positions:
            old_pins.append((old_positions[wire], value))
        else:
            new_pins.append((new_positions[wire], value))

    retained = [(i, new_positions[wire]) for wire, i in old_positions.items()
                if wire in new_positions]
    projection = sum(1 << j for _, j in retained)
    projection += sum(1 << j for _, j, _ in mixed_pairs)
    marginal = [0] * len(updated)
    for mask, count in enumerate(old):
        if not count or not agrees(mask, old_pins, old_pairs):
            continue
        next_mask = sum(bit(mask, i) << j for i, j in retained)
        for i, j, mapping in mixed_pairs:
            value = mapping[bit(mask, i)]
            if value < 0:
                break
            next_mask |= value << j
        else:
            marginal[next_mask] += count

    for mask in range(len(updated)):
        count = marginal[mask & projection]
        if count and agrees(mask, new_pins, new_pairs):
            updated[mask] += count


def count_by_runs(bits, cycle, run_order=None):
    """Count subsets for binary target columns, least significant first.

    Cycle vertices are bit positions. The weight of an edge joining i and j
    is 2**i + 2**j. Run indices are in bit order. The optional run_order is
    a permutation giving the order in which full target runs are processed.
    """
    bits, cycle = tuple(bits), tuple(cycle)
    size = len(bits)
    if size < 3 or any(value not in (0, 1) for value in bits):
        raise ValueError("Expected at least three binary target columns")
    if len(cycle) != size or set(cycle) != set(range(size)):
        raise ValueError("Cycle must visit each target column exactly once")

    runs = [tuple(vertices) for _, vertices in groupby(range(size), key=bits.__getitem__)]
    order = tuple(range(len(runs))) if run_order is None else tuple(run_order)
    if len(order) != len(runs) or set(order) != set(range(len(runs))):
        raise ValueError("Run order must be a permutation of the target runs")
    run_of = [0] * size
    for i, run in enumerate(runs):
        for vertex in run:
            run_of[vertex] = i
    by_run = cycle_fragments(cycle, run_of, len(runs))

    if len(runs) == 1:
        options = run_options(runs[0], bits[0], by_run[0])
        return sum(sum(bit_value == out for bit_value, out in enumerate(mappings[0]))
                   for entering, exiting, mappings in options if entering == exiting == 0)

    old_counts = [1]
    frontier = ()
    for i in order:
        run, fragments = runs[i], by_run[i]
        before = size + i - 1 if i > 0 else None
        after = size + i if i < len(runs) - 1 else None
        incident = tuple(wire for fragment in fragments for wire in (fragment.incoming, fragment.outgoing))
        incident += tuple(wire for wire in (before, after) if wire is not None)
        incident_set = set(incident)
        old_positions = {wire: index for index, wire in enumerate(frontier)}
        frontier = (tuple(wire for wire in frontier if wire not in incident_set)
                    + tuple(wire for wire in incident if wire not in old_positions))
        new_positions = {wire: index for index, wire in enumerate(frontier)}
        updated_counts = [0] * (1 << len(frontier))

        for entering, exiting, maps in run_options(run, bits[run[0]], fragments):
            add_option(old_counts, updated_counts, old_positions, new_positions, fragments, maps,
                       ((before, entering), (after, exiting)))
        old_counts = updated_counts

    return old_counts[0]
