import Fidelity.Vendor.SharpLogRamsey
import Fidelity.Vendor.RamseyFive

/-!
# Consecutive off-diagonal Ramsey numbers (family 170)

OpenAI's `OAI.SharpLogRamsey.main` (comparator `SharpLogRamsey.lean`) states, for each
fixed `s ≥ 6`:

* `MainBounds s`: there is `C > 0` such that for every `ε > 0`, eventually
  `t^{s-1}/(log t)^{(s-2)+ε} ≤ r(s,t) ≤ C t^{s-1}/(log t)^{s-2}`;
* `MainLimit s`: `((s-1) log t − log r(s,t)) / log log t → s − 2`.

`OAI.SharpRamseyFive.main` (comparator `RamseyFive.lean`) states the same for `s = 5`,
with its own `ramsey`, defined through `G.IsNIndepSet` instead of `Gᶜ.IsNClique`;
`ramseyFive_ramsey_eq` shows the two `ramsey` functions coincide.

Subtracting the limit statements for `s + 1` and `s` gives the growth of the ratio of
consecutive Ramsey numbers:

* `ramsey_log_ratio` (`s ≥ 6`) and `ramsey_log_ratio_five` (`s = 5`):
  `(log t − (log r(s+1,t) − log r(s,t))) / log log t → 1`, i.e.
  `r(s+1,t)/r(s,t) = t/(log t)^{1+o(1)}`;
* `ramsey_ratio_tendsto_atTop` (`s ≥ 6`) and `ramsey_ratio_five_tendsto_atTop` (`s = 5`):
  `r(s+1,t)/r(s,t) → ∞`. This uses `MainBounds` (with `ε = 1` in the lower bound for
  `s + 1`), giving `r(s+1,t)/r(s,t) ≥ t/(C (log t)²)` eventually.

What is new: the corpus gives each `r(s,t)` separately and does not compare
consecutive `s`. The ratio statements are checked here against OpenAI's exact
normalization (natural-number subtraction in the exponents, `Real.rpow` in the lower
bound, all natural `t`).

Conditional on OpenAI's statements, which are taken as the hypotheses `h` (and `h5`).
-/

namespace Fidelity

open Filter Topology

/-! ## The two `ramsey` functions agree -/

theorem ramseyFive_ramseyProperty_iff (s t N : ℕ) :
    OAI.SharpRamseyFive.RamseyProperty s t N ↔ OAI.SharpLogRamsey.RamseyProperty s t N := by
  constructor
  · intro hP G
    rcases hP G with ⟨A, hA⟩ | ⟨B, hB⟩
    · exact Or.inl ⟨A, hA⟩
    · exact Or.inr ⟨B, by simpa using hB⟩
  · intro hP G
    rcases hP G with ⟨A, hA⟩ | ⟨B, hB⟩
    · exact Or.inl ⟨A, hA⟩
    · exact Or.inr ⟨B, by simpa using hB⟩

/-- `OAI.SharpRamseyFive.ramsey` and `OAI.SharpLogRamsey.ramsey` are the same function. -/
theorem ramseyFive_ramsey_eq (s t : ℕ) :
    OAI.SharpRamseyFive.ramsey s t = OAI.SharpLogRamsey.ramsey s t := by
  have hset : {n : ℕ | OAI.SharpRamseyFive.RamseyProperty s t n} =
      {N : ℕ | OAI.SharpLogRamsey.RamseyProperty s t N} := by
    ext N
    exact ramseyFive_ramseyProperty_iff s t N
  unfold OAI.SharpRamseyFive.ramsey OAI.SharpLogRamsey.ramsey
  rw [hset]

/-! ## (a) The logarithmic ratio -/

/-- **Ratio of consecutive Ramsey numbers, logarithmic form (`s ≥ 6`).** If OpenAI's
statement holds, then `(log t − (log r(s+1,t) − log r(s,t))) / log log t → 1`. -/
theorem ramsey_log_ratio (h : type_of% @OAI.SharpLogRamsey.main) {s : ℕ} (hs : 6 ≤ s) :
    Tendsto
      (fun t : ℕ => (Real.log (t : ℝ) -
          (Real.log (OAI.SharpLogRamsey.ramsey (s + 1) t : ℝ) -
            Real.log (OAI.SharpLogRamsey.ramsey s t : ℝ))) / Real.log (Real.log (t : ℝ)))
      atTop (𝓝 1) := by
  have h1 := (h (s + 1) (by omega)).2
  have h0 := (h s hs).2
  unfold OAI.SharpLogRamsey.MainLimit at h1 h0
  have hT := h1.sub h0
  have hlim : ((s + 1 - 2 : ℕ) : ℝ) - ((s - 2 : ℕ) : ℝ) = 1 := by
    rw [Nat.cast_sub (by omega : 2 ≤ s + 1), Nat.cast_sub (by omega : 2 ≤ s)]
    push_cast
    ring
  have hc1 : ((s + 1 - 1 : ℕ) : ℝ) = (s : ℝ) := by
    rw [Nat.add_sub_cancel]
  have hc0 : ((s - 1 : ℕ) : ℝ) = (s : ℝ) - 1 := by
    rw [Nat.cast_sub (by omega : 1 ≤ s), Nat.cast_one]
  rw [hlim] at hT
  refine hT.congr (fun t => ?_)
  show (((s + 1 - 1 : ℕ) : ℝ) * Real.log (t : ℝ) -
        Real.log (OAI.SharpLogRamsey.ramsey (s + 1) t : ℝ)) / Real.log (Real.log (t : ℝ)) -
      (((s - 1 : ℕ) : ℝ) * Real.log (t : ℝ) -
        Real.log (OAI.SharpLogRamsey.ramsey s t : ℝ)) / Real.log (Real.log (t : ℝ)) =
      (Real.log (t : ℝ) - (Real.log (OAI.SharpLogRamsey.ramsey (s + 1) t : ℝ) -
        Real.log (OAI.SharpLogRamsey.ramsey s t : ℝ))) / Real.log (Real.log (t : ℝ))
  rw [hc1, hc0]
  ring

/-- **The case `s = 5`**, from `RamseyFive.lean` (for `r(5,t)`) and `SharpLogRamsey.lean`
(for `r(6,t)`): `(log t − (log r(6,t) − log r(5,t))) / log log t → 1`. -/
theorem ramsey_log_ratio_five (h : type_of% @OAI.SharpLogRamsey.main)
    (h5 : type_of% @OAI.SharpRamseyFive.main) :
    Tendsto
      (fun t : ℕ => (Real.log (t : ℝ) -
          (Real.log (OAI.SharpLogRamsey.ramsey 6 t : ℝ) -
            Real.log (OAI.SharpLogRamsey.ramsey 5 t : ℝ))) / Real.log (Real.log (t : ℝ)))
      atTop (𝓝 1) := by
  have h1 := (h 6 le_rfl).2
  have h0 := h5.2
  unfold OAI.SharpLogRamsey.MainLimit at h1
  unfold OAI.SharpRamseyFive.SharpExponent at h0
  have hT := h1.sub h0
  have hlim : ((6 - 2 : ℕ) : ℝ) - 3 = 1 := by norm_num
  have hc : ((6 - 1 : ℕ) : ℝ) = 5 := by norm_num
  rw [hlim] at hT
  refine hT.congr (fun t => ?_)
  show (((6 - 1 : ℕ) : ℝ) * Real.log (t : ℝ) -
        Real.log (OAI.SharpLogRamsey.ramsey 6 t : ℝ)) / Real.log (Real.log (t : ℝ)) -
      (4 * Real.log (t : ℝ) -
        Real.log (OAI.SharpRamseyFive.ramsey 5 t : ℝ)) / Real.log (Real.log (t : ℝ)) =
      (Real.log (t : ℝ) - (Real.log (OAI.SharpLogRamsey.ramsey 6 t : ℝ) -
        Real.log (OAI.SharpLogRamsey.ramsey 5 t : ℝ))) / Real.log (Real.log (t : ℝ))
  rw [ramseyFive_ramsey_eq, hc]
  ring

/-! ## (b) The ratio tends to infinity -/

/-- `x / (log x)² → ∞`. -/
theorem tendsto_div_log_sq_atTop :
    Tendsto (fun x : ℝ => x / Real.log x ^ 2) atTop atTop := by
  have h0 : Tendsto (fun x : ℝ => Real.log x ^ 2 / x) atTop (𝓝[>] 0) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨?_, ?_⟩
    · refine (Real.tendsto_pow_log_div_mul_add_atTop 1 0 2 one_ne_zero).congr (fun x => ?_)
      simp only [one_mul, add_zero]
    · filter_upwards [eventually_gt_atTop (1 : ℝ)] with x hx
      exact Set.mem_Ioi.mpr (div_pos (pow_pos (Real.log_pos hx) 2) (by linarith))
  refine h0.inv_tendsto_nhdsGT_zero.congr (fun x => ?_)
  simp only [Pi.inv_apply, inv_div]

/-- Arithmetic core: from `T·a/(L²·b) ≤ R₁` and `0 < R₀ ≤ C·a/b`, get
`T/L²/C ≤ R₁/R₀`. -/
theorem ramsey_ratio_lower_aux {T L a b C R₁ R₀ : ℝ} (hT : 0 ≤ T) (hC : 0 < C)
    (h1 : T * a / (L ^ 2 * b) ≤ R₁) (hR₀ : 0 < R₀) (h0 : R₀ ≤ C * a / b) :
    T / L ^ 2 / C ≤ R₁ / R₀ := by
  rw [le_div_iff₀ hR₀]
  have hq : 0 ≤ T / L ^ 2 / C := div_nonneg (div_nonneg hT (sq_nonneg L)) hC.le
  calc T / L ^ 2 / C * R₀ ≤ T / L ^ 2 / C * (C * a / b) := mul_le_mul_of_nonneg_left h0 hq
    _ = T / L ^ 2 * (C⁻¹ * C) * (a / b) := by ring
    _ = T / L ^ 2 * (a / b) := by rw [inv_mul_cancel₀ hC.ne', mul_one]
    _ = T * a / (L ^ 2 * b) := by ring
    _ ≤ R₁ := h1

/-- If eventually `t·a(t)/((log t)²·b(t)) ≤ R₁(t)` and `0 < R₀(t) ≤ C·a(t)/b(t)`, then
`R₁/R₀ → ∞`. -/
theorem ramsey_tendsto_ratio_of_bounds {R₁ R₀ a b : ℕ → ℝ} {C : ℝ} (hC : 0 < C)
    (hev : ∀ᶠ t : ℕ in atTop,
      (t : ℝ) * a t / (Real.log (t : ℝ) ^ 2 * b t) ≤ R₁ t ∧ 0 < R₀ t ∧
        R₀ t ≤ C * a t / b t) :
    Tendsto (fun t => R₁ t / R₀ t) atTop atTop := by
  have hg : Tendsto (fun t : ℕ => (t : ℝ) / Real.log (t : ℝ) ^ 2 / C) atTop atTop :=
    (tendsto_div_log_sq_atTop.comp tendsto_natCast_atTop_atTop).atTop_div_const hC
  refine tendsto_atTop_mono' atTop ?_ hg
  filter_upwards [hev] with t ht
  exact ramsey_ratio_lower_aux (Nat.cast_nonneg t) hC ht.1 ht.2.1 ht.2.2

/-- **`r(s+1,t)/r(s,t) → ∞` (`s ≥ 6`).** If OpenAI's statement holds, then for every
`s ≥ 6` the ratio of consecutive off-diagonal Ramsey numbers tends to infinity. -/
theorem ramsey_ratio_tendsto_atTop (h : type_of% @OAI.SharpLogRamsey.main) {s : ℕ}
    (hs : 6 ≤ s) :
    Tendsto (fun t : ℕ => (OAI.SharpLogRamsey.ramsey (s + 1) t : ℝ) /
      (OAI.SharpLogRamsey.ramsey s t : ℝ)) atTop atTop := by
  obtain ⟨_, -, hb₁⟩ := (h (s + 1) (by omega)).1
  obtain ⟨C₀, hC₀, hb₀⟩ := (h s hs).1
  obtain ⟨t₁, ht₁⟩ := hb₁ 1 one_pos
  obtain ⟨t₀, ht₀⟩ := hb₀ 1 one_pos
  refine ramsey_tendsto_ratio_of_bounds
    (R₁ := fun t : ℕ => (OAI.SharpLogRamsey.ramsey (s + 1) t : ℝ))
    (R₀ := fun t : ℕ => (OAI.SharpLogRamsey.ramsey s t : ℝ))
    (a := fun t : ℕ => (t : ℝ) ^ (s - 1)) (b := fun t : ℕ => Real.log (t : ℝ) ^ (s - 2))
    hC₀ ?_
  filter_upwards [eventually_ge_atTop t₀, eventually_ge_atTop t₁, eventually_ge_atTop 2]
    with t ht0 ht1 ht2
  show (t : ℝ) * (t : ℝ) ^ (s - 1) / (Real.log (t : ℝ) ^ 2 * Real.log (t : ℝ) ^ (s - 2)) ≤
        (OAI.SharpLogRamsey.ramsey (s + 1) t : ℝ) ∧
      0 < (OAI.SharpLogRamsey.ramsey s t : ℝ) ∧
      (OAI.SharpLogRamsey.ramsey s t : ℝ) ≤
        C₀ * (t : ℝ) ^ (s - 1) / Real.log (t : ℝ) ^ (s - 2)
  have hT : (1 : ℝ) < (t : ℝ) := by
    have h2 : 1 < t := by omega
    exact_mod_cast h2
  have hL : 0 < Real.log (t : ℝ) := Real.log_pos hT
  obtain ⟨hlow1, -⟩ := ht₁ t ht1
  obtain ⟨hlow0, hup0⟩ := ht₀ t ht0
  have e1 : (t : ℝ) ^ (s + 1 - 1) = (t : ℝ) * (t : ℝ) ^ (s - 1) := by
    have hs1 : s + 1 - 1 = (s - 1) + 1 := by omega
    rw [hs1]
    ring
  have hn : ((s + 1 - 2 : ℕ) : ℝ) + 1 = (((s - 2) + 2 : ℕ) : ℝ) := by
    have h' : s + 1 - 2 + 1 = s - 2 + 2 := by omega
    have h'' := congrArg (Nat.cast : ℕ → ℝ) h'
    rw [Nat.cast_add, Nat.cast_one] at h''
    exact h''
  have e2 : Real.rpow (Real.log (t : ℝ)) (((s + 1 - 2 : ℕ) : ℝ) + 1) =
      Real.log (t : ℝ) ^ 2 * Real.log (t : ℝ) ^ (s - 2) := by
    rw [hn]
    exact (Real.rpow_natCast (Real.log (t : ℝ)) (s - 2 + 2)).trans (by ring)
  have hrp : 0 < Real.log (t : ℝ) ^ (((s - 2 : ℕ) : ℝ) + 1) := Real.rpow_pos_of_pos hL _
  have hpos0 : 0 < (t : ℝ) ^ (s - 1) /
      Real.rpow (Real.log (t : ℝ)) (((s - 2 : ℕ) : ℝ) + 1) :=
    div_pos (pow_pos (by linarith) _) hrp
  refine ⟨?_, lt_of_lt_of_le hpos0 hlow0, hup0⟩
  rw [← e1, ← e2]
  exact hlow1

/-- **`r(6,t)/r(5,t) → ∞`**, from `SharpLogRamsey.lean` (lower bound for `r(6,t)`) and
`RamseyFive.lean` (upper bound for `r(5,t)`). -/
theorem ramsey_ratio_five_tendsto_atTop (h : type_of% @OAI.SharpLogRamsey.main)
    (h5 : type_of% @OAI.SharpRamseyFive.main) :
    Tendsto (fun t : ℕ => (OAI.SharpLogRamsey.ramsey 6 t : ℝ) /
      (OAI.SharpLogRamsey.ramsey 5 t : ℝ)) atTop atTop := by
  obtain ⟨_, -, hb₁⟩ := (h 6 le_rfl).1
  obtain ⟨C₀, hC₀, hb₀⟩ := h5.1
  obtain ⟨t₁, ht₁⟩ := hb₁ 1 one_pos
  obtain ⟨t₀, ht₀⟩ := hb₀ 1 one_pos
  refine ramsey_tendsto_ratio_of_bounds
    (R₁ := fun t : ℕ => (OAI.SharpLogRamsey.ramsey 6 t : ℝ))
    (R₀ := fun t : ℕ => (OAI.SharpLogRamsey.ramsey 5 t : ℝ))
    (a := fun t : ℕ => (t : ℝ) ^ 4) (b := fun t : ℕ => Real.log (t : ℝ) ^ 3)
    hC₀ ?_
  filter_upwards [eventually_ge_atTop t₀, eventually_ge_atTop t₁, eventually_ge_atTop 2]
    with t ht0 ht1 ht2
  show (t : ℝ) * (t : ℝ) ^ 4 / (Real.log (t : ℝ) ^ 2 * Real.log (t : ℝ) ^ 3) ≤
        (OAI.SharpLogRamsey.ramsey 6 t : ℝ) ∧
      0 < (OAI.SharpLogRamsey.ramsey 5 t : ℝ) ∧
      (OAI.SharpLogRamsey.ramsey 5 t : ℝ) ≤ C₀ * (t : ℝ) ^ 4 / Real.log (t : ℝ) ^ 3
  have hT : (1 : ℝ) < (t : ℝ) := by
    have h2 : 1 < t := by omega
    exact_mod_cast h2
  have hL : 0 < Real.log (t : ℝ) := Real.log_pos hT
  obtain ⟨hlow1, -⟩ := ht₁ t ht1
  obtain ⟨hlow0, hup0⟩ := ht₀ t ht0
  rw [ramseyFive_ramsey_eq] at hlow0 hup0
  have e1 : (t : ℝ) ^ (6 - 1 : ℕ) = (t : ℝ) * (t : ℝ) ^ 4 := by
    have h5' : (6 - 1 : ℕ) = 4 + 1 := rfl
    rw [h5']
    ring
  have hn : ((6 - 2 : ℕ) : ℝ) + 1 = ((5 : ℕ) : ℝ) := by norm_num
  have e2 : Real.rpow (Real.log (t : ℝ)) (((6 - 2 : ℕ) : ℝ) + 1) =
      Real.log (t : ℝ) ^ 2 * Real.log (t : ℝ) ^ 3 := by
    rw [hn]
    exact (Real.rpow_natCast (Real.log (t : ℝ)) 5).trans (by ring)
  have hrp : 0 < Real.log (t : ℝ) ^ ((3 : ℝ) + 1) := Real.rpow_pos_of_pos hL _
  have hpos0 : 0 < (t : ℝ) ^ 4 / Real.rpow (Real.log (t : ℝ)) (3 + 1) :=
    div_pos (pow_pos (by linarith) _) hrp
  refine ⟨?_, lt_of_lt_of_le hpos0 hlow0, hup0⟩
  rw [← e1, ← e2]
  exact hlow1

end Fidelity
