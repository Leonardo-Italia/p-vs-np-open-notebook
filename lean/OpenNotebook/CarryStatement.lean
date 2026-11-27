set_option autoImplicit false
set_option warningAsError true

namespace OpenNotebook

/-- The selected summands contribute this many ones to a target column. -/
structure Column where
  selected : Nat
  target : Bool

/-- Value of the selected contributions, starting with the least significant column. -/
def selectedValue : List Column → Nat
  | [] => 0
  | column :: rest => column.selected + 2 * selectedValue rest

/-- Value of the target bits, starting with the least significant column. -/
def targetValue : List Column → Nat
  | [] => 0
  | column :: rest => column.target.toNat + 2 * targetValue rest

/-- One binary outgoing carry per column, with final carry zero. -/
def CarryChain : List Column → Bool → List Bool → Prop
  | [], incoming, [] => incoming = false
  | column :: rest, incoming, outgoing :: carries =>
      column.selected + incoming.toNat = column.target.toNat + 2 * outgoing.toNat ∧
      CarryChain rest outgoing carries
  | _, _, _ => False

/-- A valid weighted sum has exactly one binary carry chain with both ends zero. -/
def CarryEquivalence : Prop :=
  ∀ (columns : List Column), (∀ column ∈ columns, column.selected ≤ 2) →
    (selectedValue columns = targetValue columns ↔
      ∃ carries : List Bool, CarryChain columns false carries ∧
        ∀ other : List Bool, CarryChain columns false other → other = carries)

end OpenNotebook
