import Mathlib
import Corollaries

/-!
# Stable finiteness fails over every field of characteristic two (family 197)

OpenAI's `KaplanskyDirectFiniteness` comparator (`OAIHyp.KaplanskyMainClaim`) gives a
finite field `K` of characteristic two, a finitely generated group `G` and
`a, b ∈ K[G]` with `ab = 1 ≠ ba`. `Corollaries.directFiniteness_transfer` moves
this to every field containing `K`. This file reaches every field `L` of
characteristic two, including `𝔽₂ = ZMod 2`, at the cost of passing to matrices:

* `exists_injective_ringHom_matrix`: `K` embeds in `M_m(L)`, `m = [K : 𝔽₂]`
  (left multiplication on an `𝔽₂`-basis, then `𝔽₂ → L`);
* `matrixLift`: an injective ring map `K[G] → M_m(L[G])`,
  `∑ c_g g ↦ ∑ χ(c_g) g`;
* `not_isStablyFiniteRing_of_kaplansky`: the images of `a, b` satisfy
  `AB = 1 ≠ BA` in `M_m(L[G])`, so `L[G]` is not stably finite;
* `not_isStablyFiniteRing_zmod_two_of_kaplansky`: in particular `𝔽₂[G]`.

The comparator states the failure only over its own `K`. Conditional on OpenAI's
statement, which is taken as the hypothesis `h`.
-/

namespace Fidelity

section MatrixLift

variable {K L G : Type} [Field K] [Field L] [Group G] {m : ℕ}

/-- Matrices with entries in `L ⊆ L[G]` commute with scalar matrices. -/
theorem commute_map_diagonal (A : Matrix (Fin m) (Fin m) L) (s : MonoidAlgebra L G) :
    Commute (A.map (MonoidAlgebra.singleOneRingHom : L →+* MonoidAlgebra L G))
      (Matrix.diagonal fun _ => s) := by
  show _ * _ = _ * _
  ext i j
  rw [Matrix.mul_diagonal, Matrix.diagonal_mul, Matrix.map_apply]
  exact (MonoidAlgebra.single_commute (fun g => Commute.one_left g)
    (fun r => Commute.all (A i j) r) s).eq

/-- The ring map `K[G] → M_m(L[G])`, `∑ c_g g ↦ ∑ χ(c_g) g`, induced by
`χ : K →+* M_m(L)`. -/
noncomputable def matrixLift (χ : K →+* Matrix (Fin m) (Fin m) L) :
    MonoidAlgebra K G →+* Matrix (Fin m) (Fin m) (MonoidAlgebra L G) :=
  MonoidAlgebra.liftNCRingHom
    ((MonoidAlgebra.singleOneRingHom : L →+* MonoidAlgebra L G).mapMatrix.comp χ)
    ((Matrix.scalar (Fin m) : MonoidAlgebra L G →+* _).toMonoidHom.comp (MonoidAlgebra.of L G))
    (fun x y => commute_map_diagonal (χ x) (MonoidAlgebra.of L G y))

/-- Coefficients of `matrixLift χ x`: entry `(i, j)` at `h` is `χ(x_h)_{ij}`. -/
theorem matrixLift_coeff (χ : K →+* Matrix (Fin m) (Fin m) L) (x : MonoidAlgebra K G)
    (i j : Fin m) (h : G) :
    (matrixLift χ x i j).coeff h = χ (x.coeff h) i j := by
  induction x using MonoidAlgebra.induction_linear with
  | zero =>
    simp only [map_zero, Matrix.zero_apply, MonoidAlgebra.coeff_zero, Finsupp.coe_zero,
      Pi.zero_apply]
  | add x y hx hy =>
    simp only [map_add, Matrix.add_apply, MonoidAlgebra.coeff_add, Finsupp.coe_add,
      Pi.add_apply, hx, hy]
  | single g c =>
    have e : matrixLift χ (MonoidAlgebra.single g c)
        = (χ c).map (MonoidAlgebra.singleOneRingHom : L →+* MonoidAlgebra L G) *
          Matrix.diagonal (fun _ => MonoidAlgebra.single g (1 : L)) :=
      MonoidAlgebra.liftNCRingHom_single _ _ _ _ _
    have hφ : (MonoidAlgebra.singleOneRingHom : L →+* MonoidAlgebra L G) (χ c i j)
        = MonoidAlgebra.single 1 (χ c i j) := rfl
    rw [e, Matrix.mul_diagonal, Matrix.map_apply, hφ, MonoidAlgebra.single_mul_single,
      one_mul, mul_one, MonoidAlgebra.coeff_single, MonoidAlgebra.coeff_single]
    by_cases hgh : g = h
    · subst hgh
      rw [Finsupp.single_eq_same, Finsupp.single_eq_same]
    · rw [Finsupp.single_eq_of_ne' hgh, Finsupp.single_eq_of_ne' hgh, map_zero,
        Matrix.zero_apply]

/-- `matrixLift χ` is injective when `χ` is. -/
theorem matrixLift_injective (χ : K →+* Matrix (Fin m) (Fin m) L)
    (hχ : Function.Injective χ) :
    Function.Injective (matrixLift χ : MonoidAlgebra K G →+* _) := by
  refine (injective_iff_map_eq_zero _).2 fun x hx => ?_
  apply MonoidAlgebra.ext
  apply Finsupp.ext
  intro h
  have hzero : χ (x.coeff h) = 0 := by
    ext i j
    rw [← matrixLift_coeff χ x i j h, hx]
    simp only [Matrix.zero_apply, MonoidAlgebra.coeff_zero, Finsupp.coe_zero, Pi.zero_apply]
  simp only [MonoidAlgebra.coeff_zero, Finsupp.coe_zero, Pi.zero_apply]
  exact hχ (hzero.trans (map_zero χ).symm)

end MatrixLift

/-- A finite field of characteristic two embeds in `M_m(L)` for every field `L` of
characteristic two, with `m = [K : 𝔽₂]`. -/
theorem exists_injective_ringHom_matrix (K L : Type) [Field K] [Fintype K] [CharP K 2]
    [Field L] [CharP L 2] :
    ∃ (m : ℕ) (χ : K →+* Matrix (Fin m) (Fin m) L), Function.Injective χ := by
  letI : Algebra (ZMod 2) K := ZMod.algebra K 2
  let B := Module.finBasis (ZMod 2) K
  refine ⟨Module.finrank (ZMod 2) K,
    (ZMod.castHom (dvd_refl 2) L).mapMatrix.comp (Algebra.leftMulMatrix B).toRingHom, ?_⟩
  intro x y hxy
  have h1 : (Algebra.leftMulMatrix B x).map (ZMod.castHom (dvd_refl 2) L)
      = (Algebra.leftMulMatrix B y).map (ZMod.castHom (dvd_refl 2) L) := hxy
  exact Algebra.leftMulMatrix_injective B
    (Matrix.map_injective (ZMod.castHom_injective (n := 2) L) h1)

/-- **Stable finiteness fails in characteristic two.** If OpenAI's Kaplansky
statement holds, its group `G` has `L[G]` not stably finite for every field `L` of
characteristic two. -/
theorem not_isStablyFiniteRing_of_kaplansky (h : OAIHyp.KaplanskyMainClaim) :
    ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
      ∀ (L : Type) [Field L] [CharP L 2], ¬ IsStablyFiniteRing (MonoidAlgebra L G) := by
  obtain ⟨K, iK, fK, cK, G, iG, gG, a, b, hab, hba⟩ := h
  refine ⟨G, iG, gG, fun L _ _ hSF => hba ?_⟩
  obtain ⟨m, χ, hχ⟩ := exists_injective_ringHom_matrix K L
  have h1 : matrixLift (G := G) χ a * matrixLift (G := G) χ b = 1 := by
    rw [← map_mul, hab, map_one]
  have h2 : matrixLift (G := G) χ b * matrixLift (G := G) χ a = 1 :=
    (hSF.isDedekindFiniteMonoid m).mul_eq_one_symm h1
  apply matrixLift_injective (G := G) χ hχ
  rw [map_mul, h2, map_one]

/-- In particular `𝔽₂[G]` is not stably finite. -/
theorem not_isStablyFiniteRing_zmod_two_of_kaplansky (h : OAIHyp.KaplanskyMainClaim) :
    ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
      ¬ IsStablyFiniteRing (MonoidAlgebra (ZMod 2) G) := by
  obtain ⟨G, iG, gG, hL⟩ := not_isStablyFiniteRing_of_kaplansky h
  exact ⟨G, iG, gG, hL (ZMod 2)⟩

end Fidelity
