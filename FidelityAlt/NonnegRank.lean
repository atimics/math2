import FidelityAlt.Vendor.MatchingPSD

/-!
# Nonnegative rank of the perfect-matching slack matrix (family 126)

OpenAI's `OAI.PerfectMatchingPSD.MainClaim` (comparator `MatchingPSD.lean`) states
that the PSD rank `psdRank n` of the slack matrix `S_n` of the perfect-matching
polytope of `K_n` (rows: edge constraints `x_e ≥ 0` and odd-cut constraints
`x(δ(U)) ≥ 1`; columns: perfect matchings) eventually exceeds every power `n^C`,
uniformly over even `n`.

A **nonnegative factorization of size `r`** is `S_n = A·B` with `A ≥ 0` of size
`rows × r` and `B ≥ 0` of size `r × matchings` (`HasNonnegFactorization`). Putting
the rows of `A` and the columns of `B` on the diagonals of `r × r` matrices turns it
into a PSD factorization of the same order, since
`tr(diag(a)·diag(b)) = ∑ⱼ aⱼbⱼ` and `diag(a) ⪰ 0 ⟺ a ≥ 0`
(`hasFactorization_of_hasNonnegFactorization`). So `psdRank ≤ rank₊`, and OpenAI's
statement gives a superpolynomial lower bound on the nonnegative rank of `S_n`
(`nonnegRank_lower_bound`). By Yannakakis's theorem (not formalized here) the
nonnegative rank of a slack matrix is the LP extension complexity, so this is the
nonnegative-rank form of Rothvoss's theorem.

What is new: the corpus states only the PSD-rank bound. The comparison
`psdRank ≤ rank₊` is folklore; it is checked here against OpenAI's exact `slack`,
`HasFactorization` and `psdRank` (including the `0 < r` convention in `psdRank`).

**Build note.** `MatchingPSD.lean` and `MatchingAffineLift.lean` both declare
`OAI.PerfectMatchingPSD.Edge`, `IsPerfectMatching` and `PerfectMatching`, so this file
cannot be imported together with `Fidelity.ExtensionComplexity`.

Conditional on OpenAI's statement, which is taken as the hypothesis `h`.
-/

namespace FidelityAlt

/-- A nonnegative factorization of order `r` of OpenAI's perfect-matching slack
matrix. -/
def HasNonnegFactorization (n r : ℕ) : Prop :=
  ∃ (A : OAI.PerfectMatchingPSD.Row n → Fin r → ℝ)
    (B : OAI.PerfectMatchingPSD.PerfectMatching n → Fin r → ℝ),
    (∀ i j, 0 ≤ A i j) ∧ (∀ M j, 0 ≤ B M j) ∧
    ∀ i M, OAI.PerfectMatchingPSD.slack i M = ∑ j, A i j * B M j

/-- **A nonnegative factorization is a (diagonal) PSD factorization of the same order.** -/
theorem hasFactorization_of_hasNonnegFactorization {n r : ℕ}
    (h : HasNonnegFactorization n r) : OAI.PerfectMatchingPSD.HasFactorization n r := by
  obtain ⟨A, B, hA, hB, hS⟩ := h
  refine ⟨fun i => Matrix.diagonal (A i), fun M => Matrix.diagonal (B M),
    fun i => ?_, fun M => ?_, fun i M => ?_⟩
  · exact Matrix.posSemidef_diagonal_iff.mpr (hA i)
  · exact Matrix.posSemidef_diagonal_iff.mpr (hB M)
  · show OAI.PerfectMatchingPSD.slack i M =
      Matrix.trace (Matrix.diagonal (A i) * Matrix.diagonal (B M))
    rw [Matrix.diagonal_mul_diagonal, Matrix.trace_diagonal]
    exact hS i M

/-- A factorization of order `0` (all slacks zero) pads to one of order `1`. -/
theorem psdFactorization_one_of_zero {n : ℕ}
    (h : OAI.PerfectMatchingPSD.HasFactorization n 0) :
    OAI.PerfectMatchingPSD.HasFactorization n 1 := by
  obtain ⟨_, _, -, -, hS⟩ := h
  refine ⟨fun _ => 0, fun _ => 0, fun _ => Matrix.PosSemidef.zero,
    fun _ => Matrix.PosSemidef.zero, fun i M => ?_⟩
  have h0 : Matrix.trace ((0 : Matrix (Fin 1) (Fin 1) ℝ) * 0) = 0 := by
    rw [mul_zero, Matrix.trace_zero]
  rw [hS i M, Matrix.trace_fin_zero]
  exact h0.symm

/-- `psdRank n ≤ r` whenever a PSD factorization of positive order `r` exists. -/
theorem psdRank_le_of_hasFactorization {n r : ℕ} (hr : 0 < r)
    (h : OAI.PerfectMatchingPSD.HasFactorization n r) :
    OAI.PerfectMatchingPSD.psdRank n ≤ r := by
  unfold OAI.PerfectMatchingPSD.psdRank
  exact Nat.sInf_le ⟨hr, h⟩

/-- **Superpolynomial nonnegative rank of the perfect-matching slack matrix.** If OpenAI's
PSD-rank statement holds, then for every `C > 0` there is `n₀ ≥ 4` such that for every
even `n ≥ n₀`, every nonnegative factorization of the slack matrix has order `r > n^C`. -/
theorem nonnegRank_lower_bound (h : OAI.PerfectMatchingPSD.MainClaim) :
    ∀ C : ℝ, 0 < C → ∃ n₀ : ℕ, 4 ≤ n₀ ∧
      ∀ n : ℕ, n₀ ≤ n → Even n → ∀ r : ℕ,
        HasNonnegFactorization n r → (n : ℝ) ^ C < (r : ℝ) := by
  intro C hC
  obtain ⟨n₀, hn₀, hmain⟩ := h C hC
  refine ⟨n₀, hn₀, fun n hn he r hr => ?_⟩
  have hbound := hmain n hn he
  have hF := hasFactorization_of_hasNonnegFactorization hr
  rcases Nat.eq_zero_or_pos r with hr0 | hpos
  · subst hr0
    exfalso
    have h1 : OAI.PerfectMatchingPSD.psdRank n ≤ 1 :=
      psdRank_le_of_hasFactorization Nat.one_pos (psdFactorization_one_of_zero hF)
    have hn1 : (1 : ℝ) ≤ (n : ℝ) := by
      have : 1 ≤ n := by omega
      exact_mod_cast this
    have hpow : (1 : ℝ) ≤ (n : ℝ) ^ C := Real.one_le_rpow hn1 hC.le
    have h1' : (OAI.PerfectMatchingPSD.psdRank n : ℝ) ≤ 1 := by exact_mod_cast h1
    linarith
  · have hle : OAI.PerfectMatchingPSD.psdRank n ≤ r := psdRank_le_of_hasFactorization hpos hF
    have hle' : (OAI.PerfectMatchingPSD.psdRank n : ℝ) ≤ (r : ℝ) := by exact_mod_cast hle
    linarith

end FidelityAlt
