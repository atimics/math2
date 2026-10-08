import Fidelity.Vendor.OrdinaryTwoPointCorrelations

/-!
# Liouville sign agreement along affine forms (family 007)

OpenAI's `OAI.OrdinaryTwoPointCorrelations.liouville_log_saving` bounds the
affine Liouville correlation `∑_{n ≤ X} λ(a₁n+b₁) λ(a₂n+b₂)` by
`C·X/(log X)^c`. Since `λ = ±1`, the number of `n ≤ X` with
`λ(a₁n+b₁) = λ(a₂n+b₂)` is `⌊X⌋/2 + O(X/(log X)^c)`.

`λ(m) = (-1)^{Ω(m)}`, so (by `liouville_eq_iff_parity`) this counts the `n` for
which `Ω(a₁n+b₁)` and `Ω(a₂n+b₂)` have the same parity. For example, `Ω(n)`
and `Ω(n+1)` agree in parity for half of all `n`, with a power-of-log rate.
The corpus states the correlation bound but not this density.

Conditional on OpenAI's statement, which is taken as the hypothesis `h`.
-/

namespace Fidelity

open ArithmeticFunction

/-- `λ(m) = ±1` for `m ≠ 0`. -/
theorem liouville_eq_one_or_neg_one {m : ℕ} (hm : m ≠ 0) :
    liouville m = 1 ∨ liouville m = -1 := by
  rw [liouville_apply hm]
  exact neg_one_pow_eq_or ℤ _

/-- For nonzero `m, m'`, `λ(m) = λ(m')` iff `Ω(m)` and `Ω(m')` have the same parity. -/
theorem liouville_eq_iff_parity {m m' : ℕ} (hm : m ≠ 0) (hm' : m' ≠ 0) :
    liouville m = liouville m' ↔ (Even (cardFactors m) ↔ Even (cardFactors m')) := by
  rw [liouville_apply hm, liouville_apply hm']
  rcases Nat.even_or_odd (cardFactors m) with h1 | h1 <;>
    rcases Nat.even_or_odd (cardFactors m') with h2 | h2
  · rw [h1.neg_one_pow, h2.neg_one_pow]
    exact ⟨fun _ => ⟨fun _ => h2, fun _ => h1⟩, fun _ => rfl⟩
  · rw [h1.neg_one_pow, h2.neg_one_pow]
    refine ⟨fun h => absurd h (by norm_num), fun h => absurd (h.1 h1) ?_⟩
    exact Nat.not_even_iff_odd.mpr h2
  · rw [h1.neg_one_pow, h2.neg_one_pow]
    refine ⟨fun h => absurd h (by norm_num), fun h => absurd (h.2 h2) ?_⟩
    exact Nat.not_even_iff_odd.mpr h1
  · rw [h1.neg_one_pow, h2.neg_one_pow]
    refine ⟨fun _ => ⟨fun h => absurd h (Nat.not_even_iff_odd.mpr h1),
      fun h => absurd h (Nat.not_even_iff_odd.mpr h2)⟩, fun _ => rfl⟩

/-- For `x, y ∈ {1, -1}`: `2·[x = y] = 1 + x·y`. -/
theorem indicator_mul_two {x y : ℤ} (hx : x = 1 ∨ x = -1) (hy : y = 1 ∨ y = -1) :
    (if x = y then (1 : ℤ) else 0) * 2 = 1 + x * y := by
  rcases hx with rfl | rfl <;> rcases hy with rfl | rfl <;> norm_num

private theorem affine_ne_zero {a b n : ℕ} (ha : 0 < a) (hn : 1 ≤ n) : a * n + b ≠ 0 :=
  (lt_of_lt_of_le (Nat.mul_pos ha hn) (Nat.le_add_right _ _)).ne'

/-- **Liouville sign agreement has density 1/2, with a power-of-log rate.** -/
theorem liouville_agreement_density
    (h : type_of% @OAI.OrdinaryTwoPointCorrelations.liouville_log_saving) :
    ∃ c : ℝ, 0 < c ∧ ∀ a₁ a₂ b₁ b₂ : ℕ, 0 < a₁ → 0 < a₂ → a₁ * b₂ ≠ a₂ * b₁ →
      ∃ C : ℝ, 0 < C ∧ ∀ X : ℝ, 3 ≤ X →
        |((Finset.filter (fun n => liouville (a₁ * n + b₁) = liouville (a₂ * n + b₂))
              (Finset.Icc 1 ⌊X⌋₊)).card : ℝ) - (⌊X⌋₊ : ℝ) / 2|
          ≤ C * X / Real.rpow (Real.log X) c := by
  obtain ⟨c, hc, hmain⟩ := h
  refine ⟨c, hc, fun a₁ a₂ b₁ b₂ ha₁ ha₂ hdet => ?_⟩
  obtain ⟨C, hC, hbound⟩ := hmain a₁ a₂ b₁ b₂ ha₁ ha₂ hdet
  refine ⟨C, hC, fun X hX => ?_⟩
  have hf : ∀ n ∈ Finset.Icc 1 ⌊X⌋₊,
      liouville (a₁ * n + b₁) = 1 ∨ liouville (a₁ * n + b₁) = -1 := fun n hn =>
    liouville_eq_one_or_neg_one (affine_ne_zero ha₁ (Finset.mem_Icc.mp hn).1)
  have hg : ∀ n ∈ Finset.Icc 1 ⌊X⌋₊,
      liouville (a₂ * n + b₂) = 1 ∨ liouville (a₂ * n + b₂) = -1 := fun n hn =>
    liouville_eq_one_or_neg_one (affine_ne_zero ha₂ (Finset.mem_Icc.mp hn).1)
  -- 2 · #{agree} = N + ∑ λλ'
  have hcount :
      ((Finset.filter (fun n => liouville (a₁ * n + b₁) = liouville (a₂ * n + b₂))
          (Finset.Icc 1 ⌊X⌋₊)).card : ℤ) * 2
        = (⌊X⌋₊ : ℤ) + ∑ n ∈ Finset.Icc 1 ⌊X⌋₊,
            liouville (a₁ * n + b₁) * liouville (a₂ * n + b₂) := by
    rw [Finset.natCast_card_filter, Finset.sum_mul,
      Finset.sum_congr rfl (fun n hn => indicator_mul_two (hf n hn) (hg n hn)),
      Finset.sum_add_distrib, Finset.sum_const, Nat.card_Icc, nsmul_eq_mul, mul_one]
    simp
  -- the correlation sum is that integer sum, cast to ℂ
  have hsum : OAI.TwoPointCorrelations.affineSum OAI.TwoPointCorrelations.liouville
      OAI.TwoPointCorrelations.liouville a₁ a₂ b₁ b₂ ⌊X⌋₊
        = ((∑ n ∈ Finset.Icc 1 ⌊X⌋₊,
            liouville (a₁ * n + b₁) * liouville (a₂ * n + b₂) : ℤ) : ℂ) := by
    unfold OAI.TwoPointCorrelations.affineSum OAI.TwoPointCorrelations.liouville
    push_cast
    try rfl
  have hb := hbound X hX
  rw [hsum, Complex.norm_intCast] at hb
  have hR :
      ((Finset.filter (fun n => liouville (a₁ * n + b₁) = liouville (a₂ * n + b₂))
          (Finset.Icc 1 ⌊X⌋₊)).card : ℝ) * 2
        = (⌊X⌋₊ : ℝ) + ((∑ n ∈ Finset.Icc 1 ⌊X⌋₊,
            liouville (a₁ * n + b₁) * liouville (a₂ * n + b₂) : ℤ) : ℝ) := by
    exact_mod_cast hcount
  have hhalf :
      ((Finset.filter (fun n => liouville (a₁ * n + b₁) = liouville (a₂ * n + b₂))
          (Finset.Icc 1 ⌊X⌋₊)).card : ℝ) - (⌊X⌋₊ : ℝ) / 2
        = ((∑ n ∈ Finset.Icc 1 ⌊X⌋₊,
            liouville (a₁ * n + b₁) * liouville (a₂ * n + b₂) : ℤ) : ℝ) / 2 := by
    linarith
  rw [hhalf, abs_div, abs_two]
  have h0 : 0 ≤ |((∑ n ∈ Finset.Icc 1 ⌊X⌋₊,
      liouville (a₁ * n + b₁) * liouville (a₂ * n + b₂) : ℤ) : ℝ)| := abs_nonneg _
  linarith

end Fidelity
