import Fidelity.Vendor.ErdosReciprocal

/-!
# Green–Tao from the Erdős reciprocal-progression statement (family 159)

OpenAI's `OAI.Erdos3.ReciprocalProgressionTheorem` (comparator `ErdosReciprocal.lean`)
states Erdős's reciprocal-sum conjecture: if `A ⊆ ℕ` and `∑_{n ∈ A} 1/n` diverges
(`¬ Summable (reciprocalTerm A)`), then `A` contains an arithmetic progression of
every length `k` with positive common difference (`HasAP A k`).

Mathlib proves Euler's theorem that `∑_p 1/p` diverges
(`not_summable_one_div_on_primes`). Combining the two gives the Green–Tao theorem:

* `primes_hasAP`: the primes satisfy OpenAI's `HasAP` for every `k`;
* `green_tao`: for every `k` there are `a` and `d > 0` with `a, a+d, …, a+(k−1)d` all
  prime;
* `green_tao_above`: the progression can be taken with first term `> N`, for any `N`
  (the primes above `N` still have divergent reciprocal sum);
* `green_tao_infinite`: for each `k`, infinitely many `a` start a `k`-term progression
  of primes.

What is new: the paper (introduction) remarks in prose that its bounds recover
Green–Tao, but the comparator states only the general reciprocal-sum theorem. Here the
specialization to the primes, including the infinitely-many form, is checked in Lean
against OpenAI's exact definitions (`reciprocalTerm`, `HasAP`).

Conditional on OpenAI's statement, which is taken as the hypothesis `h`.
-/

namespace Fidelity

/-- `reciprocalTerm A n = 1/n` for `n ∈ A`. -/
theorem erdos3_reciprocalTerm_of_mem {A : Set ℕ} {n : ℕ} (hn : n ∈ A) :
    OAI.Erdos3.reciprocalTerm A n = (n : ℝ)⁻¹ := by
  unfold OAI.Erdos3.reciprocalTerm
  exact if_pos hn

/-- `reciprocalTerm A n = 0` for `n ∉ A`. -/
theorem erdos3_reciprocalTerm_of_notMem {A : Set ℕ} {n : ℕ} (hn : n ∉ A) :
    OAI.Erdos3.reciprocalTerm A n = 0 := by
  unfold OAI.Erdos3.reciprocalTerm
  exact if_neg hn

/-- On the primes, OpenAI's `reciprocalTerm` is the indicator used in Mathlib's
`not_summable_one_div_on_primes`. -/
theorem erdos3_reciprocalTerm_primes :
    OAI.Erdos3.reciprocalTerm {p : ℕ | p.Prime} =
      Set.indicator {p : ℕ | p.Prime} (fun n : ℕ => (1 : ℝ) / n) := by
  funext n
  by_cases hp : n ∈ {p : ℕ | p.Prime}
  · rw [erdos3_reciprocalTerm_of_mem hp]
    exact ((Set.indicator_of_mem hp (fun m : ℕ => (1 : ℝ) / m)).trans (one_div (n : ℝ))).symm
  · rw [erdos3_reciprocalTerm_of_notMem hp]
    exact (Set.indicator_of_notMem hp (fun m : ℕ => (1 : ℝ) / m)).symm

/-- The primes have divergent reciprocal sum, in OpenAI's normalization. -/
theorem erdos3_not_summable_primes :
    ¬ Summable (OAI.Erdos3.reciprocalTerm {p : ℕ | p.Prime}) := by
  rw [erdos3_reciprocalTerm_primes]
  exact not_summable_one_div_on_primes

/-- The primes satisfy OpenAI's `HasAP` for every length `k`. -/
theorem primes_hasAP (h : OAI.Erdos3.ReciprocalProgressionTheorem) (k : ℕ) :
    OAI.Erdos3.HasAP {p : ℕ | p.Prime} k :=
  h {p : ℕ | p.Prime} erdos3_not_summable_primes k

/-- **Green–Tao.** If OpenAI's reciprocal-progression statement holds, the primes
contain arbitrarily long arithmetic progressions. -/
theorem green_tao (h : OAI.Erdos3.ReciprocalProgressionTheorem) (k : ℕ) :
    ∃ a d : ℕ, 0 < d ∧ ∀ i < k, (a + i * d).Prime := by
  obtain ⟨a, d, hd, hap⟩ := primes_hasAP h k
  exact ⟨a, d, hd, fun i hi => hap i hi⟩

/-- The primes above `N` still have divergent reciprocal sum. -/
theorem erdos3_not_summable_primes_above (N : ℕ) :
    ¬ Summable (OAI.Erdos3.reciprocalTerm {p : ℕ | p.Prime ∧ N < p}) := by
  intro hs
  apply not_summable_one_div_on_primes
  refine (summable_nat_add_iff (N + 1)).mp ?_
  refine ((summable_nat_add_iff (N + 1)).mpr hs).congr (fun n => ?_)
  show OAI.Erdos3.reciprocalTerm {p : ℕ | p.Prime ∧ N < p} (n + (N + 1)) =
    Set.indicator {p : ℕ | p.Prime} (fun m : ℕ => (1 : ℝ) / m) (n + (N + 1))
  have hm : N < n + (N + 1) := by omega
  by_cases hp : (n + (N + 1)).Prime
  · have hA : n + (N + 1) ∈ {p : ℕ | p.Prime ∧ N < p} := ⟨hp, hm⟩
    have hP : n + (N + 1) ∈ {p : ℕ | p.Prime} := hp
    rw [erdos3_reciprocalTerm_of_mem hA]
    exact ((Set.indicator_of_mem hP (fun m : ℕ => (1 : ℝ) / m)).trans
      (one_div ((n + (N + 1) : ℕ) : ℝ))).symm
  · have hA : n + (N + 1) ∉ {p : ℕ | p.Prime ∧ N < p} := fun h' => hp h'.1
    have hP : n + (N + 1) ∉ {p : ℕ | p.Prime} := hp
    rw [erdos3_reciprocalTerm_of_notMem hA]
    exact (Set.indicator_of_notMem hP (fun m : ℕ => (1 : ℝ) / m)).symm

/-- **Green–Tao, beyond any bound.** For every `k` and `N` there is a `k`-term
progression of primes with positive difference and first term `> N`. -/
theorem green_tao_above (h : OAI.Erdos3.ReciprocalProgressionTheorem) (k N : ℕ) :
    ∃ a d : ℕ, 0 < d ∧ N < a ∧ ∀ i < k, (a + i * d).Prime := by
  obtain ⟨a, d, hd, hap⟩ := h _ (erdos3_not_summable_primes_above N) (k + 1)
  have h0 : (a + 0 * d).Prime ∧ N < a + 0 * d := hap 0 (Nat.succ_pos k)
  rw [zero_mul, add_zero] at h0
  refine ⟨a, d, hd, h0.2, fun i hi => ?_⟩
  have hi' : (a + i * d).Prime ∧ N < a + i * d := hap i (by omega)
  exact hi'.1

/-- **Infinitely many progressions.** For each `k`, infinitely many `a` start a
`k`-term arithmetic progression of primes with positive difference. -/
theorem green_tao_infinite (h : OAI.Erdos3.ReciprocalProgressionTheorem) (k : ℕ) :
    {a : ℕ | ∃ d : ℕ, 0 < d ∧ ∀ i < k, (a + i * d).Prime}.Infinite := by
  refine Set.infinite_of_forall_exists_gt (fun N => ?_)
  obtain ⟨a, d, hd, hN, hap⟩ := green_tao_above h k N
  exact ⟨a, ⟨d, hd, hap⟩, hN⟩

end Fidelity
