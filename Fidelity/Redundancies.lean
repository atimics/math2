import Fidelity.Vendor.OrdinaryTwoPointCorrelations
import Fidelity.Vendor.OrdinaryElliott
import Fidelity.Vendor.OstmannPrimes
import Fidelity.Vendor.OstmannComplete

/-!
# Redundant comparator statements (families 007 and 013)

OpenAI formalized some results twice, under different names, in separate
comparator files with separate proof developments. This file proves in the
kernel which of these *statements* follow from which. Every theorem takes
OpenAI's statement as a hypothesis (or states an implication between
statements); no `sorry`d comparator proof is used.

## 1. Corrected Elliott (family 007)

* `OrdinaryTwoPointCorrelations.lean` states `binary_corrected_elliott` with
  `OneBounded` only for `n > 0`, nonpretentiousness as
  "`K ≤ 𝔻(f, χ n^{it}; N)²` eventually, uniformly in `|t| ≤ N`", and the average
  `correlationSum / N`.
* `OrdinaryElliott.lean` states `binary_corrected_elliott` with `OneBounded` for
  all `n`, nonpretentiousness as "`inf_{|t| ≤ N} 𝔻(f, χ n^{it}; N) → ∞`", and the
  average `N⁻¹ * ∑`.

`twoPoint_binary_iff_ordinaryElliott` proves the two statements are
**equivalent**: the prime sums coincide, the two nonpretentiousness notions
are equivalent, and the value `f 0` never enters a shifted sum
(`zeroAtZero` repairs the stronger `OneBounded`). OpenAI proves them with two
independent developments (`OAI.NumberTheory.TwoPointCorrelations` and
`OAI.NumberTheory.OrdinaryCorrelations.Elliott`).

`binary_of_affine_corrected_elliott`: the affine comparator in the same file
implies the binary one (`a₁ = a₂ = 1`, `b = h`).

## 2. Ostmann's inverse Goldbach problem (family 013)

* `ostmann_main_iff_inverseGoldbach`: `OstmannPrimes.main` and
  `OstmannComplete.InverseGoldbach` are the same proposition (`Iff.rfl`).
* `twoInfiniteSummandsImpossible_of_inverseGoldbach`: the second theorem of
  `OstmannComplete.lean` follows from the first in a few lines (infinite sets
  are nontrivial; eventual agreement with the primes means finite symmetric
  difference). The converse needs Dirichlet's theorem plus a CRT argument
  (OpenAI's `FiniteSummands.lean`) and is not formalized here.
-/

namespace Fidelity

open Filter

/-! ## 1. Corrected Elliott -/

section Elliott

/-- The prime sum of `OrdinaryElliott` at `X = N` is the prime sum of
`OrdinaryTwoPointCorrelations` against the twist `χ(n) n^{it}`. -/
theorem distanceSq_eq_squaredDistance (f : ℕ → ℂ) {q : ℕ} (χ : DirichletCharacter ℂ q)
    (t : ℝ) (N : ℕ) :
    OAI.OrdinaryCorrelations.distanceSq f χ t (N : ℝ) =
      OAI.TwoPointCorrelations.squaredDistance f
        (OAI.TwoPointCorrelations.characterTwist χ t) N := by
  have hset : (Finset.Icc 2 ⌊(N : ℝ)⌋₊).filter Nat.Prime =
      OAI.TwoPointCorrelations.primesUpTo N := by
    rw [Nat.floor_natCast]
    ext p
    simp only [OAI.TwoPointCorrelations.primesUpTo, Finset.mem_filter, Finset.mem_Icc,
      Finset.mem_range]
    constructor
    · rintro ⟨⟨-, hpN⟩, hp⟩
      exact ⟨by omega, hp⟩
    · rintro ⟨hpN, hp⟩
      exact ⟨⟨hp.two_le, by omega⟩, hp⟩
  unfold OAI.OrdinaryCorrelations.distanceSq OAI.TwoPointCorrelations.squaredDistance
  exact Finset.sum_congr hset (fun p _ => rfl)

/-- `OrdinaryElliott`'s nonpretentiousness implies `OrdinaryTwoPointCorrelations`'s. -/
theorem uniformlyNonpretentious_twoPoint_of_ordinary {f : ℕ → ℂ}
    (hf : OAI.OrdinaryCorrelations.UniformlyNonpretentious f) :
    OAI.TwoPointCorrelations.UniformlyNonpretentious f := by
  intro q hq χ K
  filter_upwards [Filter.tendsto_atTop.mp (hf q hq χ) (Real.sqrt K + 1)] with N hN
  intro t ht
  have hmem : OAI.OrdinaryCorrelations.distance f χ t (N : ℝ) ∈
      (fun s : ℝ => OAI.OrdinaryCorrelations.distance f χ s (N : ℝ)) ''
        Set.Icc (-(N : ℝ)) (N : ℝ) :=
    Set.mem_image_of_mem (fun s : ℝ => OAI.OrdinaryCorrelations.distance f χ s (N : ℝ))
      (Set.mem_Icc.mpr (abs_le.mp ht))
  have hbdd : BddBelow ((fun s : ℝ => OAI.OrdinaryCorrelations.distance f χ s (N : ℝ)) ''
      Set.Icc (-(N : ℝ)) (N : ℝ)) := by
    refine ⟨0, ?_⟩
    rintro _ ⟨s, -, rfl⟩
    exact Real.sqrt_nonneg _
  have h1 : Real.sqrt K + 1 ≤ OAI.OrdinaryCorrelations.distance f χ t (N : ℝ) :=
    le_trans hN (csInf_le hbdd hmem)
  have h3 := distanceSq_eq_squaredDistance f χ t N
  have h4 : OAI.OrdinaryCorrelations.distance f χ t (N : ℝ) =
      Real.sqrt (OAI.OrdinaryCorrelations.distanceSq f χ t (N : ℝ)) := rfl
  by_contra hlt
  have hlt' : OAI.OrdinaryCorrelations.distanceSq f χ t (N : ℝ) < K := by
    rw [h3]
    exact not_le.mp hlt
  have h2 : Real.sqrt (OAI.OrdinaryCorrelations.distanceSq f χ t (N : ℝ)) ≤ Real.sqrt K :=
    Real.sqrt_le_sqrt hlt'.le
  linarith

/-- `OrdinaryTwoPointCorrelations`'s nonpretentiousness implies `OrdinaryElliott`'s. -/
theorem uniformlyNonpretentious_ordinary_of_twoPoint {f : ℕ → ℂ}
    (hf : OAI.TwoPointCorrelations.UniformlyNonpretentious f) :
    OAI.OrdinaryCorrelations.UniformlyNonpretentious f := by
  intro q hq χ
  refine Filter.tendsto_atTop.mpr (fun M => ?_)
  filter_upwards [hf q hq χ (M ^ 2)] with N hN
  have hN0 : (0 : ℝ) ≤ (N : ℝ) := Nat.cast_nonneg N
  have hne : (Set.Icc (-(N : ℝ)) (N : ℝ)).Nonempty :=
    Set.nonempty_Icc.mpr (by linarith)
  refine le_csInf (Set.Nonempty.image
    (fun s : ℝ => OAI.OrdinaryCorrelations.distance f χ s (N : ℝ)) hne) ?_
  rintro _ ⟨t, ht, rfl⟩
  have hK : M ^ 2 ≤ OAI.OrdinaryCorrelations.distanceSq f χ t (N : ℝ) := by
    rw [distanceSq_eq_squaredDistance]
    exact hN t (abs_le.mpr (Set.mem_Icc.mp ht))
  have h1 : |M| ≤ OAI.OrdinaryCorrelations.distance f χ t (N : ℝ) := by
    rw [← Real.sqrt_sq_eq_abs]
    exact Real.sqrt_le_sqrt hK
  exact le_trans (le_abs_self M) h1

/-- `f` with its value at `0` replaced by `0`. -/
noncomputable def zeroAtZero (f : ℕ → ℂ) (n : ℕ) : ℂ := if n = 0 then 0 else f n

theorem zeroAtZero_oneBounded {f : ℕ → ℂ} (hf : OAI.TwoPointCorrelations.OneBounded f) :
    OAI.OrdinaryCorrelations.OneBounded (zeroAtZero f) := by
  intro n
  by_cases hn : n = 0
  · have e : zeroAtZero f n = 0 := if_pos hn
    rw [e, norm_zero]
    exact zero_le_one
  · have e : zeroAtZero f n = f n := if_neg hn
    rw [e]
    exact hf n (Nat.pos_of_ne_zero hn)

theorem zeroAtZero_multiplicative {f : ℕ → ℂ}
    (hf : OAI.TwoPointCorrelations.Multiplicative f) :
    OAI.OrdinaryCorrelations.Multiplicative (zeroAtZero f) := by
  intro m n hm hn hmn
  have e1 : zeroAtZero f (m * n) = f (m * n) := if_neg (Nat.mul_pos hm hn).ne'
  have e2 : zeroAtZero f m = f m := if_neg hm.ne'
  have e3 : zeroAtZero f n = f n := if_neg hn.ne'
  rw [e1, e2, e3]
  exact hf m n hm hn hmn

theorem squaredDistance_zeroAtZero (f g : ℕ → ℂ) (N : ℕ) :
    OAI.TwoPointCorrelations.squaredDistance (zeroAtZero f) g N =
      OAI.TwoPointCorrelations.squaredDistance f g N := by
  unfold OAI.TwoPointCorrelations.squaredDistance
  refine Finset.sum_congr rfl (fun p hp => ?_)
  have hp' : p ∈ (Finset.range (N + 1)).filter Nat.Prime := hp
  have e : zeroAtZero f p = f p := if_neg (Finset.mem_filter.mp hp').2.ne_zero
  rw [e]

theorem zeroAtZero_uniformlyNonpretentious {f : ℕ → ℂ}
    (hf : OAI.TwoPointCorrelations.UniformlyNonpretentious f) :
    OAI.TwoPointCorrelations.UniformlyNonpretentious (zeroAtZero f) := by
  intro q hq χ K
  filter_upwards [hf q hq χ K] with N hN
  intro t ht
  rw [squaredDistance_zeroAtZero]
  exact hN t ht

theorem correlationSum_zeroAtZero (f₁ f₂ : ℕ → ℂ) (h₁ h₂ N : ℕ) :
    OAI.TwoPointCorrelations.correlationSum (zeroAtZero f₁) (zeroAtZero f₂) h₁ h₂ N =
      OAI.TwoPointCorrelations.correlationSum f₁ f₂ h₁ h₂ N := by
  unfold OAI.TwoPointCorrelations.correlationSum
  refine Finset.sum_congr rfl (fun n hn => ?_)
  have hn1 : 1 ≤ n := (Finset.mem_Icc.mp hn).1
  have e1 : zeroAtZero f₁ (n + h₁) = f₁ (n + h₁) := if_neg (show ¬(n + h₁ = 0) by omega)
  have e2 : zeroAtZero f₂ (n + h₂) = f₂ (n + h₂) := if_neg (show ¬(n + h₂ = 0) by omega)
  rw [e1, e2]

/-- **The `OrdinaryElliott` comparator follows from the `OrdinaryTwoPointCorrelations`
binary comparator.** -/
theorem ordinaryElliott_of_twoPoint :
    type_of% @OAI.OrdinaryTwoPointCorrelations.binary_corrected_elliott →
    type_of% @OAI.OrdinaryCorrelations.binary_corrected_elliott := by
  intro h f₁ f₂ hf₁ hf₂ hm₁ hm₂ hNP h₁ h₂ hne
  refine (h f₁ f₂ hm₁ hm₂ (fun n _ => hf₁ n) (fun n _ => hf₂ n)
    (hNP.imp uniformlyNonpretentious_twoPoint_of_ordinary
      uniformlyNonpretentious_twoPoint_of_ordinary) h₁ h₂ hne).congr (fun N => ?_)
  show OAI.TwoPointCorrelations.correlationSum f₁ f₂ h₁ h₂ N / (N : ℂ) =
    OAI.OrdinaryCorrelations.shiftAverage f₁ f₂ h₁ h₂ N
  rw [div_eq_inv_mul]
  rfl

/-- **The `OrdinaryTwoPointCorrelations` binary comparator follows from the
`OrdinaryElliott` comparator.** -/
theorem twoPoint_of_ordinaryElliott :
    type_of% @OAI.OrdinaryCorrelations.binary_corrected_elliott →
    type_of% @OAI.OrdinaryTwoPointCorrelations.binary_corrected_elliott := by
  intro h f₁ f₂ hm₁ hm₂ hf₁ hf₂ hNP h₁ h₂ hne
  refine (h (zeroAtZero f₁) (zeroAtZero f₂) (zeroAtZero_oneBounded hf₁)
    (zeroAtZero_oneBounded hf₂) (zeroAtZero_multiplicative hm₁)
    (zeroAtZero_multiplicative hm₂)
    (hNP.imp
      (fun hu => uniformlyNonpretentious_ordinary_of_twoPoint
        (zeroAtZero_uniformlyNonpretentious hu))
      (fun hu => uniformlyNonpretentious_ordinary_of_twoPoint
        (zeroAtZero_uniformlyNonpretentious hu)))
    h₁ h₂ hne).congr (fun N => ?_)
  show OAI.OrdinaryCorrelations.shiftAverage (zeroAtZero f₁) (zeroAtZero f₂) h₁ h₂ N =
    OAI.TwoPointCorrelations.correlationSum f₁ f₂ h₁ h₂ N / (N : ℂ)
  rw [← correlationSum_zeroAtZero f₁ f₂ h₁ h₂ N, div_eq_inv_mul]
  rfl

/-- **The two binary corrected-Elliott comparators are equivalent statements.** -/
theorem twoPoint_binary_iff_ordinaryElliott :
    type_of% @OAI.OrdinaryTwoPointCorrelations.binary_corrected_elliott ↔
    type_of% @OAI.OrdinaryCorrelations.binary_corrected_elliott :=
  ⟨ordinaryElliott_of_twoPoint, twoPoint_of_ordinaryElliott⟩

/-- The affine corrected-Elliott comparator implies the binary one
(`a₁ = a₂ = 1`, `b₁ = h₁`, `b₂ = h₂`). -/
theorem binary_of_affine_corrected_elliott :
    type_of% @OAI.OrdinaryTwoPointCorrelations.affine_corrected_elliott →
    type_of% @OAI.OrdinaryTwoPointCorrelations.binary_corrected_elliott := by
  intro h f₁ f₂ hm₁ hm₂ hf₁ hf₂ hNP h₁ h₂ hne
  refine (h f₁ f₂ hm₁ hm₂ hf₁ hf₂ hNP 1 1 h₁ h₂ Nat.one_pos Nat.one_pos
    (by omega)).congr (fun N => ?_)
  show OAI.TwoPointCorrelations.affineSum f₁ f₂ 1 1 h₁ h₂ N / (N : ℂ) =
    OAI.TwoPointCorrelations.correlationSum f₁ f₂ h₁ h₂ N / (N : ℂ)
  unfold OAI.TwoPointCorrelations.affineSum OAI.TwoPointCorrelations.correlationSum
  simp only [one_mul]

/-- The affine comparator implies the `OrdinaryElliott` comparator. -/
theorem ordinaryElliott_of_affine_corrected_elliott :
    type_of% @OAI.OrdinaryTwoPointCorrelations.affine_corrected_elliott →
    type_of% @OAI.OrdinaryCorrelations.binary_corrected_elliott :=
  fun h => ordinaryElliott_of_twoPoint (binary_of_affine_corrected_elliott h)

end Elliott

/-! ## 2. Ostmann's inverse Goldbach problem -/

section Ostmann

/-- `OstmannPrimes.main` and `OstmannComplete.InverseGoldbach` are the same
proposition (the second only spells out the `symmDiff` instances). -/
theorem ostmann_main_iff_inverseGoldbach :
    type_of% @OAI.Ostmann.main ↔ OAI.Ostmann.InverseGoldbach :=
  Iff.rfl

/-- **`OstmannComplete.twoInfiniteSummandsImpossible` follows from
`OstmannComplete.inverseGoldbach`.** Infinite summands are nontrivial, and
agreement with the primes from `N` on puts the symmetric difference inside
`[0, N)`. -/
theorem twoInfiniteSummandsImpossible_of_inverseGoldbach :
    OAI.Ostmann.InverseGoldbach → OAI.Ostmann.TwoInfiniteSummandsImpossible := by
  intro h A B hA hB hev
  obtain ⟨N, hN⟩ := hev
  refine h A B hA.nontrivial hB.nontrivial ((Set.finite_Iio N).subset ?_)
  intro n hn
  rw [Set.mem_Iio]
  by_contra hlt
  have hiff := hN n (not_lt.mp hlt)
  have hor : (n ∈ OAI.Ostmann.sumset A B ∧ n ∉ OAI.Ostmann.primes) ∨
      (n ∈ OAI.Ostmann.primes ∧ n ∉ OAI.Ostmann.sumset A B) := by
    first
      | exact Set.mem_symmDiff.mp hn
      | exact hn
  rcases hor with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact h2 (hiff.mp h1)
  · exact h2 (hiff.mpr h1)

/-- `OstmannPrimes.main` implies `OstmannComplete.TwoInfiniteSummandsImpossible`. -/
theorem twoInfiniteSummandsImpossible_of_ostmannMain :
    type_of% @OAI.Ostmann.main → OAI.Ostmann.TwoInfiniteSummandsImpossible :=
  fun h => twoInfiniteSummandsImpossible_of_inverseGoldbach
    (ostmann_main_iff_inverseGoldbach.mp h)

end Ostmann

end Fidelity
