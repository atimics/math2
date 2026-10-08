import Fidelity.Vendor.MahlerConjecture

/-!
# Bourgain–Milman with base `2/π` from the symmetric Mahler statement (family 087)

OpenAI's `OAI.SymmetricMahler.symmetric_mahler` states the symmetric Mahler
conjecture: for `n ≥ 1` and every compact, convex, origin-symmetric
`K ⊆ ℝⁿ` with nonempty interior, `vol(K)·vol(K°) ≥ 4ⁿ/n!`, where `K°` is the
coordinate polar.

`symmetric_mahler_gamma` derives the weaker, dimension-free form
`vol(K)·vol(K°) ≥ 2ⁿ / Γ(n/2+1)²` (weaker because `4ⁿ/n! ≥ 2ⁿ/Γ(n/2+1)²`).
Since `κₙ = π^{n/2}/Γ(n/2+1)` is the volume of the Euclidean unit ball (Mathlib's
`EuclideanSpace.volume_ball`), `2ⁿ/Γ(n/2+1)² = (2/π)ⁿ κₙ²` (`two_pow_div_Gamma_sq_eq`).
This is the Bourgain–Milman inequality `vol(K)vol(K°) ≥ cⁿ κₙ²` with `c = 2/π`,
the best possible base (the cube shows that no `c > 2/π` works for all `n`; that
optimality is not formalized here). The corpus mentions Bourgain–Milman only as
history and states no explicit constant.

The numerical input is `factorial_le_two_pow_mul_Gamma_sq`: `n! ≤ 2ⁿ Γ(n/2+1)²`
for every `n`. It is proved by two-step induction: the ratio
`2ⁿΓ(n/2+1)²/n!` is multiplied by `(n+2)/(n+1) ≥ 1` when `n` increases by 2,
and equals `1` at `n = 0` and `π/2` at `n = 1`. (This replaces the
duplication-formula route in the written derivation; no log-convexity is needed.)

Conditional on OpenAI's statement, which is taken as the hypothesis `h`.
-/

namespace Fidelity

open MeasureTheory

/-- `n! ≤ 2ⁿ Γ(n/2 + 1)²` for every natural number `n`. -/
theorem factorial_le_two_pow_mul_Gamma_sq (n : ℕ) :
    (n.factorial : ℝ) ≤ 2 ^ n * Real.Gamma ((n : ℝ) / 2 + 1) ^ 2 := by
  -- the step `k ↦ k + 2`
  have step : ∀ k : ℕ,
      (k.factorial : ℝ) ≤ 2 ^ k * Real.Gamma ((k : ℝ) / 2 + 1) ^ 2 →
      ((k + 1 + 1).factorial : ℝ) ≤
        2 ^ (k + 1 + 1) * Real.Gamma (((k + 1 + 1 : ℕ) : ℝ) / 2 + 1) ^ 2 := by
    intro k hk
    have hx : (0 : ℝ) < (k : ℝ) / 2 + 1 := by positivity
    have hk0 : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
    have hG : Real.Gamma (((k + 1 + 1 : ℕ) : ℝ) / 2 + 1)
        = ((k : ℝ) / 2 + 1) * Real.Gamma ((k : ℝ) / 2 + 1) := by
      rw [← Real.Gamma_add_one hx.ne']
      congr 1
      push_cast
      ring
    have hX : (0 : ℝ) ≤ 2 ^ k * Real.Gamma ((k : ℝ) / 2 + 1) ^ 2 := by positivity
    rw [hG]
    calc ((k + 1 + 1).factorial : ℝ)
        = ((k : ℝ) + 2) * ((k : ℝ) + 1) * (k.factorial : ℝ) := by
          rw [Nat.factorial_succ, Nat.factorial_succ]
          push_cast
          ring
      _ ≤ ((k : ℝ) + 2) * ((k : ℝ) + 1) * (2 ^ k * Real.Gamma ((k : ℝ) / 2 + 1) ^ 2) :=
          mul_le_mul_of_nonneg_left hk (by positivity)
      _ ≤ ((k : ℝ) + 2) * ((k : ℝ) + 2) * (2 ^ k * Real.Gamma ((k : ℝ) / 2 + 1) ^ 2) :=
          mul_le_mul_of_nonneg_right
            (mul_le_mul_of_nonneg_left (by linarith) (by linarith)) hX
      _ = 2 ^ (k + 1 + 1) * (((k : ℝ) / 2 + 1) * Real.Gamma ((k : ℝ) / 2 + 1)) ^ 2 := by
          ring
  -- base cases `n = 0` and `n = 1`
  have h0 : ((0 : ℕ).factorial : ℝ) ≤ 2 ^ 0 * Real.Gamma (((0 : ℕ) : ℝ) / 2 + 1) ^ 2 := by
    norm_num [Real.Gamma_one]
  have h1 : ((1 : ℕ).factorial : ℝ) ≤ 2 ^ 1 * Real.Gamma (((1 : ℕ) : ℝ) / 2 + 1) ^ 2 := by
    rw [Nat.factorial_one, Nat.cast_one,
      Real.Gamma_add_one (by norm_num : (1 : ℝ) / 2 ≠ 0), Real.Gamma_one_half_eq, mul_pow,
      Real.sq_sqrt Real.pi_pos.le]
    have e : (2 : ℝ) ^ 1 * ((1 / 2) ^ 2 * Real.pi) = Real.pi / 2 := by ring
    linarith [Real.two_le_pi]
  have hpair : ∀ k : ℕ,
      ((k.factorial : ℝ) ≤ 2 ^ k * Real.Gamma ((k : ℝ) / 2 + 1) ^ 2) ∧
      (((k + 1).factorial : ℝ) ≤
        2 ^ (k + 1) * Real.Gamma (((k + 1 : ℕ) : ℝ) / 2 + 1) ^ 2) := by
    intro k
    induction k with
    | zero => exact ⟨h0, h1⟩
    | succ k ih => exact ⟨ih.2, step k ih.1⟩
  exact (hpair n).1

/-- `2ⁿ/Γ(n/2+1)² = (2/π)ⁿ κₙ²` with `κₙ = √πⁿ/Γ(n/2+1)`, the volume of the Euclidean
unit ball in Mathlib's `EuclideanSpace.volume_ball`. -/
theorem two_pow_div_Gamma_sq_eq (n : ℕ) :
    (2 : ℝ) ^ n / Real.Gamma ((n : ℝ) / 2 + 1) ^ 2
      = (2 / Real.pi) ^ n * (Real.sqrt Real.pi ^ n / Real.Gamma ((n : ℝ) / 2 + 1)) ^ 2 := by
  have hπ : Real.pi ^ n ≠ 0 := pow_ne_zero n Real.pi_pos.ne'
  have hs : (Real.sqrt Real.pi ^ n) ^ 2 = Real.pi ^ n := by
    rw [← pow_mul, mul_comm n 2, pow_mul, Real.sq_sqrt Real.pi_pos.le]
  rw [div_pow (Real.sqrt Real.pi ^ n), hs, div_pow (2 : ℝ) Real.pi n, div_mul_div_comm,
    mul_comm ((2 : ℝ) ^ n) (Real.pi ^ n), mul_div_mul_left _ _ hπ]

/-- **Bourgain–Milman with base `2/π`.** If OpenAI's symmetric Mahler statement holds,
then every compact, convex, origin-symmetric `K ⊆ ℝⁿ` (`n ≥ 1`) with nonempty
interior satisfies `vol(K)·vol(K°) ≥ 2ⁿ/Γ(n/2+1)² = (2/π)ⁿ κₙ²`. -/
theorem symmetric_mahler_gamma
    (h : type_of% @OAI.SymmetricMahler.symmetric_mahler)
    {n : ℕ} (hn : 1 ≤ n) {K : Set (Fin n → ℝ)} (hK : IsCompact K) (hconv : Convex ℝ K)
    (hsym : ∀ x ∈ K, -x ∈ K) (hint : (interior K).Nonempty) :
    (2 : ℝ) ^ n / Real.Gamma ((n : ℝ) / 2 + 1) ^ 2 ≤
      (volume K).toReal * (volume (OAI.SymmetricMahler.coordinatePolar K)).toReal := by
  refine le_trans ?_ (h hn hK hconv hsym hint)
  have hΓ : 0 < Real.Gamma ((n : ℝ) / 2 + 1) ^ 2 :=
    pow_pos (Real.Gamma_pos_of_pos (by positivity)) 2
  have hF : (0 : ℝ) < (n.factorial : ℝ) := by exact_mod_cast Nat.factorial_pos n
  rw [div_le_div_iff₀ hΓ hF]
  calc (2 : ℝ) ^ n * (n.factorial : ℝ)
      ≤ 2 ^ n * (2 ^ n * Real.Gamma ((n : ℝ) / 2 + 1) ^ 2) :=
        mul_le_mul_of_nonneg_left (factorial_le_two_pow_mul_Gamma_sq n) (by positivity)
    _ = 4 ^ n * Real.Gamma ((n : ℝ) / 2 + 1) ^ 2 := by
        rw [← mul_assoc, ← mul_pow]
        norm_num

/-- The same bound in the form `(2/π)ⁿ κₙ²`, `κₙ = √πⁿ/Γ(n/2+1)`. -/
theorem symmetric_mahler_bourgainMilman
    (h : type_of% @OAI.SymmetricMahler.symmetric_mahler)
    {n : ℕ} (hn : 1 ≤ n) {K : Set (Fin n → ℝ)} (hK : IsCompact K) (hconv : Convex ℝ K)
    (hsym : ∀ x ∈ K, -x ∈ K) (hint : (interior K).Nonempty) :
    (2 / Real.pi) ^ n * (Real.sqrt Real.pi ^ n / Real.Gamma ((n : ℝ) / 2 + 1)) ^ 2 ≤
      (volume K).toReal * (volume (OAI.SymmetricMahler.coordinatePolar K)).toReal := by
  rw [← two_pow_div_Gamma_sq_eq n]
  exact symmetric_mahler_gamma h hn hK hconv hsym hint

end Fidelity
