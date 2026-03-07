#!/usr/bin/env python3
"""Frozen Stage -1 / 0A configuration for the IQ sex-differences program."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

SIGN_CONVENTION = {
    "name": "female_minus_male",
    "definition": "Positive values favor females; negative values favor males.",
}

SMALLEST_EFFECT_SIZE_OF_INTEREST = 0.10

DECISION_THRESHOLDS = {
    "strong_within_family_persistence_share": 0.50,
    "sharp_attenuation_clerical_share": 0.40,
    "sharp_attenuation_nonclerical_ceiling": 0.20,
    "large_composite_movement_sd": 0.15,
    "weak_outcome_increment_partial_r2": 0.005,
    "weak_outcome_increment_std_coef": 0.05,
    "meaningful_heterogeneity_sd": 0.10,
}

ESTIMANDS = {
    "subtest_mean_gap": {
        "formula": "d = (mean_female - mean_male) / pooled_sd",
        "note": "Primary descriptive sign convention for all datasets.",
    },
    "within_family_gap": {
        "formula": "y_if = alpha_family + beta*female_i + gamma1*age_i + "
        "gamma2*older_sibs_i + epsilon_if",
        "note": "Primary NLSY79 fixed-effects estimand; cluster by HHID_1979.",
    },
    "composite_sensitivity": {
        "formula": "Gap movement across the frozen ICAR weight grid.",
    },
}

ICAR_COMPOSITE_GRID = {
    "equal_weights": {"vr": 0.25, "ln": 0.25, "mr": 0.25, "r3d": 0.25},
    "verbal_heavy": {"vr": 0.50, "ln": 0.20, "mr": 0.15, "r3d": 0.15},
    "matrix_heavy": {"vr": 0.15, "ln": 0.20, "mr": 0.45, "r3d": 0.20},
    "spatial_heavy": {"vr": 0.15, "ln": 0.15, "mr": 0.20, "r3d": 0.50},
}

ICAR = {
    "path": DATA_DIR / "icar" / "sapaICARData18aug2010thru20may2013.csv",
    "key_path": DATA_DIR / "icar" / "superKey60.tab",
    "row_count": 96958,
    "delimiter": ",",
    "min_answered_items_per_domain": 3,
    "sex": {"code": "gender", "male": 1, "female": 2},
    "age": "age",
    "weights": None,
    "estimation_mode": "sample_descriptive_unweighted",
    "domains": {
        "ln": [
            "LN.01",
            "LN.03",
            "LN.05",
            "LN.06",
            "LN.07",
            "LN.33",
            "LN.34",
            "LN.35",
            "LN.58",
        ],
        "mr": [
            "MR.43",
            "MR.44",
            "MR.45",
            "MR.46",
            "MR.47",
            "MR.48",
            "MR.50",
            "MR.53",
            "MR.54",
            "MR.55",
            "MR.56",
        ],
        "r3d": [f"R3D.{i:02d}" for i in range(1, 25)],
        "vr": [
            "VR.04",
            "VR.09",
            "VR.11",
            "VR.13",
            "VR.14",
            "VR.16",
            "VR.17",
            "VR.18",
            "VR.19",
            "VR.23",
            "VR.26",
            "VR.31",
            "VR.32",
            "VR.36",
            "VR.39",
            "VR.42",
        ],
    },
}

NLSY79 = {
    "path": DATA_DIR / "nlsy" / "nlsy79_all_1979-2022.zip",
    "zip_member": "nlsy79_all_1979-2022.csv",
    "delimiter": ",",
    "sex": {"code": "R0214800", "alias": "SAMPLE_SEX_1979", "male": 1, "female": 2},
    "id": {"code": "R0000100", "alias": "CASEID_1979"},
    "household_id": {"code": "R0000149", "alias": "HHID_1979"},
    "race": {"code": "R0214700", "alias": "SAMPLE_RACE_78SCRN"},
    "age": {
        "baseline": {"code": "R0000600", "alias": "AGE_1979"},
        "asvab_proxy": {"code": "R0410500", "alias": "AGE_1981"},
    },
    "birth_order_proxy": {"code": "R0009300", "alias": "OLDER_SIBS_1979"},
    "weights": {
        "cross_section_1979": {"code": "R0216101", "alias": "C_SAMPWEIGHT_1979"},
        "asvab_1981": {"code": "R0614700", "alias": "SAMPWEIGHT_ASVAB_1981"},
    },
    "estimation_mode": {
        "descriptive_primary": "weighted_with_R0614700",
        "family_fe_primary": "unweighted_sample_descriptive",
    },
    "primary_subtests": {
        "arithmetic_reasoning": {
            "code": "R0616200",
            "alias": "ASVAB-15_1981",
            "label": "Section 2 scale score",
        },
        "word_knowledge": {
            "code": "R0616400",
            "alias": "ASVAB-17_1981",
            "label": "Section 3 scale score",
        },
        "paragraph_comprehension": {
            "code": "R0616600",
            "alias": "ASVAB-19_1981",
            "label": "Section 4 scale score",
        },
        "numerical_operations": {
            "code": "R0616800",
            "alias": "ASVAB-21_1981",
            "label": "Section 5 scale score",
        },
        "coding_speed": {
            "code": "R0617000",
            "alias": "ASVAB-23_1981",
            "label": "Section 6 scale score",
        },
        "auto_shop": {
            "code": "R0617200",
            "alias": "ASVAB-25_1981",
            "label": "Section 7 scale score",
        },
        "math_knowledge": {
            "code": "R0617400",
            "alias": "ASVAB-27_1981",
            "label": "Section 8 scale score",
        },
        "mechanical_comprehension": {
            "code": "R0617600",
            "alias": "ASVAB-29_1981",
            "label": "Section 9 scale score",
        },
        "electronic_information": {
            "code": "R0617800",
            "alias": "ASVAB-31_1981",
            "label": "Section 10 scale score",
        },
    },
    "secondary_xrnd_scores": {
        "arithmetic_reasoning": "R0648309",
        "word_knowledge": "R0648343",
        "paragraph_comprehension": "R0648382",
        "math_knowledge": "R0648402",
    },
    "domain_composites": {
        "clerical_speed": ["numerical_operations", "coding_speed"],
        "verbal": ["word_knowledge", "paragraph_comprehension"],
        "quantitative": ["arithmetic_reasoning", "math_knowledge"],
        "mechanical": ["auto_shop", "mechanical_comprehension"],
        "mechanical_plus_electronic": [
            "auto_shop",
            "mechanical_comprehension",
            "electronic_information",
        ],
    },
    "pair_link_slots": [
        {"id": "R0000150", "relation": "R0000151", "sibling_marker": "R0000162"},
        {"id": "R0000152", "relation": "R0000153", "sibling_marker": "R0000163"},
        {"id": "R0000154", "relation": "R0000155", "sibling_marker": "R0000164"},
        {"id": "R0000156", "relation": "R0000157", "sibling_marker": "R0000165"},
        {"id": "R0000158", "relation": "R0000159", "sibling_marker": "R0000166"},
    ],
    "sibling_relationship_codes": {
        "brother": 6,
        "sister": 7,
    },
    "pair_rule": {
        "require_shared_household_id": True,
        "require_reciprocal_id_link": True,
        "accept_relation_codes": [6, 7],
        "accept_positive_sibling_marker": True,
        "primary_opposite_sex_only": True,
        "primary_max_age_gap_years": 4,
        "sensitivity_max_age_gap_years": 6,
        "primary_one_pair_per_household": True,
        "tie_break_rule": (
            "smallest_age_gap, then most_nonmissing_primary_subtests, "
            "then lowest_sorted_caseid"
        ),
    },
}

NLSY97 = {
    "path": DATA_DIR / "nlsy" / "nlsy97_all_1997-2023.zip",
    "zip_member": "nlsy97_all_1997-2023.csv",
    "delimiter": ",",
    "sex": {"code": "R0536300", "alias": "KEY!SEX_1997", "male": 1, "female": 2},
    "id": {"code": "R0000100", "alias": "PUBID_1997"},
    "weights": {
        "cross_section_1997": {"code": "R1236200", "alias": "CS_SAMPLING_WEIGHT_1997"}
    },
    "summary_scores": {
        "math_verbal_percentile": {
            "code": "R9829600",
            "alias": "ASVAB_MATH_VERBAL_SCORE_PCT_XRND",
        }
    },
    "ability_scores": {
        "general_science": {"pos": "R9705200", "neg": "R9706400"},
        "arithmetic_reasoning": {"pos": "R9705300", "neg": "R9706500"},
        "word_knowledge": {"pos": "R9705400", "neg": "R9706600"},
        "paragraph_comprehension": {"pos": "R9705500", "neg": "R9706700"},
        "numerical_operations": {"pos": "R9705600", "neg": "R9706800"},
        "coding_speed": {"pos": "R9705700", "neg": "R9706900"},
        "auto_information": {"pos": "R9705800", "neg": "R9707000"},
        "shop_information": {"pos": "R9705900", "neg": "R9707100"},
        "math_knowledge": {"pos": "R9706000", "neg": "R9707200"},
        "mechanical_comprehension": {"pos": "R9706100", "neg": "R9707300"},
        "electronic_information": {"pos": "R9706200", "neg": "R9707400"},
        "assembling_objects": {"pos": "R9706300", "neg": "R9707500"},
    },
    "stage_a_fields": {
        "avg_grade_recent": {"code": "R9700100", "kind": "categorical"},
        "science_experiment": {"code": "R9700600", "kind": "categorical"},
        "science_equipment": {"code": "R9700800", "kind": "categorical"},
        "shop_attention": {"code": "R9700900", "kind": "categorical"},
        "prev_taken": {"code": "R9701300", "kind": "categorical"},
        "computer_use": {"code": "R9702900", "kind": "categorical"},
        "computer_test": {"code": "R9703000", "kind": "categorical"},
        "effort": {"code": "R9703400", "kind": "categorical"},
        "room_comfort": {"code": "R9703500", "kind": "categorical"},
        "room_quiet": {"code": "R9703600", "kind": "categorical"},
        "numerical_operations_items_complete": {
            "code": "R9704400",
            "kind": "continuous",
        },
        "coding_speed_items_complete": {"code": "R9704500", "kind": "continuous"},
        "arithmetic_reasoning_post_variance": {
            "code": "R9707700",
            "kind": "continuous",
        },
        "math_knowledge_post_variance": {
            "code": "R9708200",
            "kind": "continuous",
        },
        "grade_fall_1997": {"code": "R9708800", "kind": "categorical"},
    },
    "estimation_mode": {
        "descriptive_primary": "weighted_with_R1236200",
        "ability_score_rule": "combine_pos_neg_into_signed_theta",
    },
}

PIAAC = {
    "paths": sorted((DATA_DIR / "piaac").glob("*.csv")),
    "delimiter_rules": {
        "p1_us": "pipe",
        "p1_non_us": "comma",
        "p2_all_current_files": "semicolon",
    },
    "estimation_mode": "population_weighted_with_plausible_values",
    "sex": {"code": "GENDER_R"},
    "id": {"code": "SEQID"},
    "age": {"code": "AGE_R", "fallback": "AGEG10LFS_T"},
    "education": ["EDCAT8", "EDCAT7", "EDCAT6"],
    "scores": {
        "literacy": [f"PVLIT{i}" for i in range(1, 11)],
        "numeracy": [f"PVNUM{i}" for i in range(1, 11)],
        "problem_solving": [f"PVPSL{i}" for i in range(1, 11)],
    },
    "weights": {
        "full_sample": "SPFWT0",
        "replicates": [f"SPFWT{i}" for i in range(1, 81)],
        "variance_method": "VEMETHOD",
        "variance_fay_factor": "VEFAYFAC",
        "variance_replicates": "VENREPS",
        "variance_stratum": "VARSTRAT",
        "variance_unit": "VARUNIT",
    },
}

DATASETS = {
    "icar": ICAR,
    "nlsy79": NLSY79,
    "nlsy97": NLSY97,
    "piaac": PIAAC,
}
