import OpenNotebook.CarryStatement
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option warningAsError true

namespace OpenNotebook

private theorem bitBound (bit : Bool) : bit.toNat ≤ 1 := by
  cases bit <;> decide

private theorem bitOfEqualValues {a b : Bool} (h : a.toNat = b.toNat) : a = b := by
  cases a <;> cases b <;> simp_all [Bool.toNat]

private theorem chainImpliesSum (columns : List Column) (incoming : Bool)
    (carries : List Bool) (valid : CarryChain columns incoming carries) :
    selectedValue columns + incoming.toNat = targetValue columns := by
  induction columns generalizing incoming carries with
  | nil =>
      cases carries with
      | nil =>
          change incoming = false at valid
          subst incoming
          rfl
      | cons _ _ =>
          exact False.elim valid
  | cons column rest ih =>
      cases carries with
      | nil =>
          exact False.elim valid
      | cons outgoing carries =>
          have step := valid.1
          have tail := ih outgoing carries valid.2
          change column.selected + 2 * selectedValue rest + incoming.toNat =
            column.target.toNat + 2 * targetValue rest
          omega

private theorem sumImpliesChain (columns : List Column) (incoming : Bool)
    (bounded : ∀ column ∈ columns, column.selected ≤ 2)
    (sum : selectedValue columns + incoming.toNat = targetValue columns) :
    ∃ carries : List Bool, CarryChain columns incoming carries := by
  induction columns generalizing incoming with
  | nil =>
      refine ⟨[], ?_⟩
      cases incoming with
      | false => rfl
      | true => simp [selectedValue, targetValue, Bool.toNat] at sum
  | cons column rest ih =>
      have headBound : column.selected ≤ 2 := bounded column (by simp)
      have tailBound : ∀ c ∈ rest, c.selected ≤ 2 :=
        fun c member => bounded c (List.mem_cons_of_mem _ member)
      have inBound := bitBound incoming
      have targetBound := bitBound column.target
      change column.selected + 2 * selectedValue rest + incoming.toNat =
        column.target.toNat + 2 * targetValue rest at sum
      by_cases unchanged : column.selected + incoming.toNat = column.target.toNat
      · have tailSum : selectedValue rest + false.toNat = targetValue rest := by
          change selectedValue rest + 0 = targetValue rest
          omega
        obtain ⟨carries, valid⟩ := ih false tailBound tailSum
        exact ⟨false :: carries, ⟨unchanged, valid⟩⟩
      · have step : column.selected + incoming.toNat = column.target.toNat + 2 := by
          omega
        have tailSum : selectedValue rest + true.toNat = targetValue rest := by
          change selectedValue rest + 1 = targetValue rest
          omega
        obtain ⟨carries, valid⟩ := ih true tailBound tailSum
        exact ⟨true :: carries, ⟨step, valid⟩⟩

private theorem chainUnique (columns : List Column) (incoming : Bool) (a b : List Bool)
    (ha : CarryChain columns incoming a) (hb : CarryChain columns incoming b) : a = b := by
  induction columns generalizing incoming a b with
  | nil =>
      cases a with
      | nil =>
          cases b with
          | nil => rfl
          | cons _ _ => exact False.elim hb
      | cons _ _ => exact False.elim ha
  | cons _ _ ih =>
      cases a with
      | nil => exact False.elim ha
      | cons nextA restA =>
          cases b with
          | nil => exact False.elim hb
          | cons nextB restB =>
              have stepA := ha.1
              have stepB := hb.1
              have equalValues : nextA.toNat = nextB.toNat := by omega
              have equalBits : nextA = nextB := bitOfEqualValues equalValues
              subst nextB
              have sameTail := ih nextA restA restB ha.2 hb.2
              rw [sameTail]

theorem carryEquivalence : CarryEquivalence := by
  intro columns bounded
  constructor
  · intro sum
    obtain ⟨carries, valid⟩ := sumImpliesChain columns false bounded
      (by simpa [Bool.toNat] using sum)
    exact ⟨carries, valid, fun other h => chainUnique columns false other carries h valid⟩
  · intro ⟨carries, valid, _⟩
    simpa [Bool.toNat] using chainImpliesSum columns false carries valid

end OpenNotebook
