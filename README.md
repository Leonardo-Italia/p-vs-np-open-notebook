# P vs NP — Open Research Notebook

This public, AI-led notebook documents an investigation of the P versus NP problem. Its long-term goal is to resolve whether P equals NP. It presents intermediate results, proof drafts, and computational checks.

## Research notes

| Note | Subject | Executable evidence in this repository |
|---|---|---|
| [01 — Alternating target](research/01-alternating-target.md) | Parsimonious reduction to Subset Sum on one cycle with an alternating target | Carry equivalence checked in Lean, plus exhaustive local tables and exact counts on 165 formulas |
| [02 — Counting and parameters](research/02-counting-and-parameters.md) | Carry algorithms, parameterized classifications, and conditional ETH bounds | Carry-based counts compared with integer subset search on 240 instances |
| [03 — Matchgate representations](research/03-matchgate-representations.md) | Open-chain compression and representation-specific lower bounds | 32 local coefficients, 67,648 matchgate identities, and the transformed-triangle rank certificate |
| [04 — Fixed weights and proof complexity](research/04-fixed-weights-and-proofs.md) | Target-only circuit compilation and a separation between resolution, sum of squares, and cutting planes | Checks of shared local blocks; full transfer arguments are given in the note |
| [05 — Isolated forbidden tuples](research/05-local-constraint-arity.md) | Sharp limits for local paths and cycles with unary required degrees | Exact gadget counts and a finite search for the shortest cycle |
| [06 — Counting by run cutwidth](research/06-run-cutwidth.md) | Exact counting by contraction across run boundaries | 440 exhaustive and 240 sampled instances in two processing orders |
| [07 — Counting with trees of runs](research/07-run-trees.md) | Exact counting by tree contraction and a logarithmic width separation | 270 exact comparisons and six optimal linear width checks |
| [08 — Dual rank on one cycle](research/08-connected-dual-rank.md) | Exponential matchgate rank for the equality signature on one alternating-target cycle | Eight port orders and 4,160 projected coefficients |
| [Technical appendix (PDF)](research/technical-appendix.pdf) | Expanded selector gadgets, matchgate arguments, and circuit constructions | Historical experiments are identified in the text |

The notes identify working proof drafts, finite checks, and formally verified results. Independent proof review has not been recorded.

The appendix is maintained in [LaTeX](research/technical-appendix.tex). Its [index](research/technical-drafts.md) maps the note links to sections of the PDF. To rebuild it with a standard TeX Live or MiKTeX installation, run from the repository root

```sh
cd research
pdflatex -halt-on-error technical-appendix.tex
pdflatex -halt-on-error technical-appendix.tex
```

## Formal verification in Lean

The carry equivalence in Note 01 is checked for arbitrary finite lists of binary columns with at most two selected ones per column. A valid weighted sum is equivalent to a unique binary carry chain whose initial and final carries are zero.

With [Lean installed](https://lean-lang.org/install/), run from the repository root

```sh
cd lean
lake build
```

[The statement](lean/OpenNotebook/CarryStatement.lean), [the proof](lean/OpenNotebook/CarryProof.lean), and [the build audit](lean/OpenNotebook.lean) are separate. The audit rejects any transitive axiom dependency outside the standard allowlist. The build pins Lean 4.36.0 and uses its standard library. The verification layout was inspired by [open-goat/pequalnp-proofs](https://github.com/open-goat/pequalnp-proofs/tree/ce4640f1c1e3dd02fde6086bd4151aca518af8d3).

## Run the checks

From the repository root, with Python 3.10 or newer, run

```sh
python verify.py
```

The checker uses the Python standard library. It stops on the first discrepancy. The expected summary is

```text
Alternating target: 165 formulas; 74 positive; up to 658 columns
Carry counting: 240 instances; 86 with multiple cycles; 4566 schedules
Open chain: 67648 matchgate identities
Dual triangle: cumulative ranks modulo 1009 = [1, 13, 63, 64]
Connected dual: 8 port orders; 4160 projected coefficients
Local constraints: 132 gadget assignments; shortest cycle 6 columns
Run frontiers: 440 exhaustive and 240 sampled instances in two orders
```

## Attribution

Leonardo initiated and directed the investigation and maintains the notebook. OpenAI's ChatGPT/Codex developed the mathematical constructions, proof drafts, and verification code. The idea of publishing a public notebook was discussed with Google Gemini. The notes cite the outside theorems on which their arguments depend.

Cite the [notebook](CITATION.cff) and link to the exact commit when referring to a specific version of a result.

## Publication policy

Forks are welcome. Contributions to the official repository are closed. We may cite or build on independently published work, including forks. When we use external work, we credit its authors, link to the exact version we used, and document what we verified.
