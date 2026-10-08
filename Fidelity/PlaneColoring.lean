import Fidelity.Vendor.EuclideanFiveColor
import Fidelity.Vendor.PlaneColoring

/-!
# The chromatic number of the plane is 6 or 7 (family 158)

Family 158 has two comparators, in two different formulations of the plane:

* `EuclideanFiveColor.lean`: `OAI.EuclideanFiveColor.no_proper_five_coloring` says no
  `coloring : ℂ → Fin 5` gives different colors to points with `‖z − w‖ = 1`;
* `PlaneColoring.lean`: `OAI.Problem160.properColoring_seven` says
  `OAI.Problem160.ProperColoring 7`: some `c : EuclideanSpace ℝ (Fin 2) → Fin 7` gives
  different colors to points at `dist = 1`.

`complex_properColoring_iff` shows the two notions of proper `k`-coloring agree for
every `k`, through the isometry `Complex.orthonormalBasisOneI.repr : ℂ ≃ₗᵢ[ℝ] ℝ²`
(`z ↦ (re z, im z)`). With monotonicity in `k` (`plane_properColoring_mono`), the two
comparators together give:

* `plane_not_properColoring_le_five`: no proper coloring of `ℝ²` with `≤ 5` colors;
* `planeChromaticNumber_eq_six_or_seven`: the least `k` with a proper `k`-coloring of
  `ℝ²` is `6` or `7`;
* `complexChromaticNumber_eq_planeChromaticNumber` and
  `complexChromaticNumber_eq_six_or_seven`: the same for `ℂ`.

What is new: the corpus states the lower and upper bounds as separate theorems, in
different models of the plane; the conclusion `χ(ℝ²) ∈ {6, 7}` needs both and is not
stated. It is checked here against OpenAI's exact definitions.

Conditional on OpenAI's statements, which are taken as the hypotheses `h5` and `h7`.
-/

namespace Fidelity

/-- The two comparators' notions of a proper `k`-coloring (of `ℂ` with `‖z − w‖ = 1`, and
of `EuclideanSpace ℝ (Fin 2)` with `dist x y = 1`) agree. -/
theorem complex_properColoring_iff (k : ℕ) :
    (∃ c : ℂ → Fin k, OAI.EuclideanFiveColor.ProperColoring k c) ↔
      OAI.Problem160.ProperColoring k := by
  constructor
  · rintro ⟨c, hc⟩
    refine ⟨fun x => c (Complex.orthonormalBasisOneI.repr.symm x), fun x y hxy => ?_⟩
    have hd : ‖Complex.orthonormalBasisOneI.repr.symm x -
        Complex.orthonormalBasisOneI.repr.symm y‖ = 1 := by
      rw [← Complex.dist_eq, LinearIsometryEquiv.dist_map]
      exact hxy
    exact hc _ _ hd
  · rintro ⟨c, hc⟩
    refine ⟨fun z => c (Complex.orthonormalBasisOneI.repr z), fun z w hzw => ?_⟩
    have hd : dist (Complex.orthonormalBasisOneI.repr z)
        (Complex.orthonormalBasisOneI.repr w) = 1 := by
      rw [LinearIsometryEquiv.dist_map, Complex.dist_eq]
      exact hzw
    exact hc _ _ hd

/-- A proper `k`-coloring is a proper `m`-coloring for `k ≤ m`. -/
theorem plane_properColoring_mono {k m : ℕ} (hkm : k ≤ m)
    (h : OAI.Problem160.ProperColoring k) : OAI.Problem160.ProperColoring m := by
  obtain ⟨c, hc⟩ := h
  refine ⟨fun x => Fin.castLE hkm (c x), fun x y hxy hxyc => hc x y hxy ?_⟩
  exact Fin.castLE_injective hkm hxyc

/-- The plane (as `EuclideanSpace ℝ (Fin 2)`) has no proper 5-coloring. -/
theorem plane_not_properColoring_five
    (h5 : type_of% @OAI.EuclideanFiveColor.no_proper_five_coloring) :
    ¬ OAI.Problem160.ProperColoring 5 :=
  fun hP => h5 ((complex_properColoring_iff 5).mpr hP)

/-- The plane has no proper coloring with at most 5 colors. -/
theorem plane_not_properColoring_le_five
    (h5 : type_of% @OAI.EuclideanFiveColor.no_proper_five_coloring) {k : ℕ} (hk : k ≤ 5) :
    ¬ OAI.Problem160.ProperColoring k :=
  fun hc => plane_not_properColoring_five h5 (plane_properColoring_mono hk hc)

/-- `ℂ` has a proper 7-coloring in the sense of `EuclideanFiveColor.lean`. -/
theorem complex_properColoring_seven
    (h7 : type_of% @OAI.Problem160.properColoring_seven) :
    ∃ c : ℂ → Fin 7, OAI.EuclideanFiveColor.ProperColoring 7 c :=
  (complex_properColoring_iff 7).mpr h7

/-- The chromatic number of the plane `EuclideanSpace ℝ (Fin 2)`: the least `k` with a
proper `k`-coloring (`OAI.Problem160.ProperColoring k`). -/
noncomputable def planeChromaticNumber : ℕ :=
  sInf {k : ℕ | OAI.Problem160.ProperColoring k}

/-- The chromatic number of `ℂ`, in the sense of `EuclideanFiveColor.lean`. -/
noncomputable def complexChromaticNumber : ℕ :=
  sInf {k : ℕ | ∃ c : ℂ → Fin k, OAI.EuclideanFiveColor.ProperColoring k c}

/-- **Hadwiger–Nelson: `χ(ℝ²) ∈ {6, 7}`.** If OpenAI's two plane-coloring statements
hold, the chromatic number of the plane is 6 or 7. -/
theorem planeChromaticNumber_eq_six_or_seven
    (h5 : type_of% @OAI.EuclideanFiveColor.no_proper_five_coloring)
    (h7 : type_of% @OAI.Problem160.properColoring_seven) :
    planeChromaticNumber = 6 ∨ planeChromaticNumber = 7 := by
  have hne : {k : ℕ | OAI.Problem160.ProperColoring k}.Nonempty := ⟨7, h7⟩
  have hle : planeChromaticNumber ≤ 7 := by
    unfold planeChromaticNumber
    exact Nat.sInf_le (show 7 ∈ {k : ℕ | OAI.Problem160.ProperColoring k} from h7)
  have hmem : OAI.Problem160.ProperColoring planeChromaticNumber := by
    unfold planeChromaticNumber
    exact Nat.sInf_mem hne
  have hge : 6 ≤ planeChromaticNumber := by
    by_contra hlt
    exact plane_not_properColoring_le_five h5 (by omega) hmem
  omega

/-- The two models of the plane have the same chromatic number. -/
theorem complexChromaticNumber_eq_planeChromaticNumber :
    complexChromaticNumber = planeChromaticNumber := by
  have hset : {k : ℕ | ∃ c : ℂ → Fin k, OAI.EuclideanFiveColor.ProperColoring k c} =
      {k : ℕ | OAI.Problem160.ProperColoring k} := by
    ext k
    exact complex_properColoring_iff k
  unfold complexChromaticNumber planeChromaticNumber
  rw [hset]

/-- **`χ(ℂ) ∈ {6, 7}`**, in the formulation of `EuclideanFiveColor.lean`. -/
theorem complexChromaticNumber_eq_six_or_seven
    (h5 : type_of% @OAI.EuclideanFiveColor.no_proper_five_coloring)
    (h7 : type_of% @OAI.Problem160.properColoring_seven) :
    complexChromaticNumber = 6 ∨ complexChromaticNumber = 7 := by
  rw [complexChromaticNumber_eq_planeChromaticNumber]
  exact planeChromaticNumber_eq_six_or_seven h5 h7

end Fidelity
