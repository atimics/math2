import Fidelity.Vendor.MatchingAffineLift

/-!
# LP extension complexity of the perfect-matching polytope (family 126)

OpenAI's `OAI.PerfectMatchingPSD.affine_lift_lower_bound` (comparator
`MatchingAffineLift.lean`) states: for every `C > 0` there is `n₀ ≥ 4` such that for
even `n ≥ n₀`, if the perfect-matching polytope `P_n ⊆ ℝ^E` is an affine image
`T(L ∩ S^r_+)` of an affine slice of the cone of `r × r` positive semidefinite
matrices, then `n^C < r`.

An **LP lift of size `r`** (an `ℝ^r_+`-lift in the sense of Gouveia–Parrilo–Thomas)
is an affine subspace `L ⊆ ℝ^r` and an affine map `π : ℝ^r → ℝ^E` with
`π(L ∩ ℝ^r_{≥0}) = P_n` (`HasLPLift`). The diagonal embedding `y ↦ diag(y)` maps
`ℝ^r_{≥0}` onto the diagonal PSD matrices, so every LP lift of size `r` is a PSD lift
of size `r` (`hasAffineLift_of_hasLPLift`: take `diag(L)` and `π ∘ diag⁻¹`, where
`diag⁻¹` reads off the diagonal). Hence (`lp_lift_lower_bound`) OpenAI's statement
implies a superpolynomial lower bound on the size of every LP lift of `P_n`:
a Rothvoss-type lower bound on LP extension complexity.

What is new: the corpus states only the semidefinite bound. The implication
"PSD lifts are at least as small as LP lifts" is folklore (the nonnegative orthant is
a slice of the PSD cone), but the corpus does not draw the LP consequence and it is
checked here against OpenAI's exact `HasAffineLift` and `matchingPolytope`. The
equivalence of `ℝ^r_+`-lifts with extensions by `r` linear inequalities
(Yannakakis, Gouveia–Parrilo–Thomas) is not formalized here.

Conditional on OpenAI's statement, which is taken as the hypothesis `h`.
-/

namespace Fidelity

/-- An LP lift (`ℝ^r_+`-lift) of the perfect-matching polytope of size `r`: an affine
subspace `L ⊆ ℝ^r` and an affine map `π : ℝ^r → ℝ^E` with `π(L ∩ ℝ^r_{≥0}) = P_n`. -/
def HasLPLift (n r : ℕ) : Prop :=
  ∃ (L : AffineSubspace ℝ (Fin r → ℝ))
    (π : (Fin r → ℝ) →ᵃ[ℝ] (OAI.PerfectMatchingPSD.Edge n → ℝ)),
    π '' {y | y ∈ L ∧ ∀ i, 0 ≤ y i} = OAI.PerfectMatchingPSD.matchingPolytope n

/-- The diagonal embedding `ℝ^r → ℝ^{r×r}`, `y ↦ diag(y)`, as an affine map. -/
noncomputable def lpDiagEmbed (r : ℕ) : (Fin r → ℝ) →ᵃ[ℝ] Matrix (Fin r) (Fin r) ℝ :=
  (Matrix.diagonalLinearMap (n := Fin r) (R := ℝ) (α := ℝ)).toAffineMap

/-- Reading off the diagonal, `X ↦ (X i i)ᵢ`, as an affine map. -/
noncomputable def lpDiagRead (r : ℕ) : Matrix (Fin r) (Fin r) ℝ →ᵃ[ℝ] (Fin r → ℝ) :=
  (Matrix.diagLinearMap (n := Fin r) (R := ℝ) (α := ℝ)).toAffineMap

theorem lpDiagEmbed_apply {r : ℕ} (y : Fin r → ℝ) : lpDiagEmbed r y = Matrix.diagonal y :=
  rfl

theorem lpDiagRead_apply {r : ℕ} (X : Matrix (Fin r) (Fin r) ℝ) :
    lpDiagRead r X = Matrix.diag X :=
  rfl

/-- `π ∘ diag⁻¹ ∘ diag = π`. -/
theorem lpDiag_comp_apply {r : ℕ} {V : Type} [AddCommGroup V] [Module ℝ V]
    (π : (Fin r → ℝ) →ᵃ[ℝ] V) (y : Fin r → ℝ) :
    (π.comp (lpDiagRead r)) (lpDiagEmbed r y) = π y := by
  rw [AffineMap.comp_apply, lpDiagEmbed_apply, lpDiagRead_apply, Matrix.diag_diagonal]

/-- **Every LP lift is a PSD lift of the same size.** -/
theorem hasAffineLift_of_hasLPLift {n r : ℕ} (hlp : HasLPLift n r) :
    OAI.PerfectMatchingPSD.HasAffineLift n r := by
  obtain ⟨L, π, hπ⟩ := hlp
  refine ⟨L.map (lpDiagEmbed r), π.comp (lpDiagRead r), ?_⟩
  rw [← hπ]
  ext x
  constructor
  · rintro ⟨X, ⟨hX, hpsd⟩, rfl⟩
    obtain ⟨y, hy, rfl⟩ := AffineSubspace.mem_map.mp hX
    rw [lpDiagEmbed_apply, Matrix.posSemidef_diagonal_iff] at hpsd
    exact ⟨y, ⟨hy, hpsd⟩, (lpDiag_comp_apply π y).symm⟩
  · rintro ⟨y, ⟨hy, hnn⟩, rfl⟩
    refine ⟨lpDiagEmbed r y, ⟨AffineSubspace.mem_map.mpr ⟨y, hy, rfl⟩, ?_⟩,
      lpDiag_comp_apply π y⟩
    rw [lpDiagEmbed_apply, Matrix.posSemidef_diagonal_iff]
    exact hnn

/-- **Superpolynomial LP extension complexity of the perfect-matching polytope.**
If OpenAI's affine-lift statement holds, then for every `C > 0` there is `n₀ ≥ 4` such
that for every even `n ≥ n₀`, every LP lift of the perfect-matching polytope of `K_n`
has size `r > n^C`. -/
theorem lp_lift_lower_bound
    (h : type_of% @OAI.PerfectMatchingPSD.affine_lift_lower_bound) :
    ∀ C : ℝ, 0 < C → ∃ n₀ : ℕ, 4 ≤ n₀ ∧
      ∀ n : ℕ, n₀ ≤ n → Even n → ∀ r : ℕ, HasLPLift n r → (n : ℝ) ^ C < (r : ℝ) := by
  intro C hC
  obtain ⟨n₀, hn₀, hmain⟩ := h C hC
  exact ⟨n₀, hn₀, fun n hn he r hr => hmain n hn he r (hasAffineLift_of_hasLPLift hr)⟩

end Fidelity
