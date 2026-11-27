import OpenNotebook.CarryProof
import Lean

set_option autoImplicit false
set_option warningAsError true

example : OpenNotebook.CarryEquivalence := OpenNotebook.carryEquivalence

open Lean Elab Command in
run_cmd do
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  let dependencies ← Lean.collectAxioms ``OpenNotebook.carryEquivalence
  for dependency in dependencies do
    unless allowed.contains dependency do
      throwError "Unexpected axiom dependency: {dependency}"

#print axioms OpenNotebook.carryEquivalence
