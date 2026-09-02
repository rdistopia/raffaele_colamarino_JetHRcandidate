from typing import Dict, Any, Optional

def calculate_employment_deductions(income: float, config: Optional[Dict[str, Any]] = None) -> float:
    """
    Calcola le detrazioni per lavoro dipendente a tempo indeterminato (Art. 13 TUIR).
    Supporta la configurazione dinamica dei parametri da database.
    """
    if config is None:
        config = {
            "base_max_deduction": 1955.0,
            "tier1_limit": 15000.0,
            "tier2_limit": 28000.0,
            "tier3_limit": 50000.0,
            "tier2_base": 1910.0,
            "tier2_factor": 1190.0,
            "bonus_25_35k": 65.0
        }

    if income <= 0:
        return 0.0

    tier1 = config.get("tier1_limit", 15000.0)
    tier2 = config.get("tier2_limit", 28000.0)
    tier3 = config.get("tier3_limit", 50000.0)
    tier2_base = config.get("tier2_base", 1910.0)
    tier2_factor = config.get("tier2_factor", 1190.0)
    bonus = config.get("bonus_25_35k", 65.0)

    deduction = 0.0

    if income <= tier1:
        deduction = config.get("base_max_deduction", 1955.0)
    elif income <= tier2:
        prop = (tier2 - income) / (tier2 - tier1)
        deduction = tier2_base + (tier2_factor * prop)
        if 25000.0 < income <= 35000.0:
            deduction += bonus
    elif income <= tier3:
        prop = (tier3 - income) / (tier3 - tier2)
        deduction = tier2_base * prop
        if 25000.0 < income <= 35000.0:
            deduction += bonus
    else:
        deduction = 0.0

    return round(deduction, 2)
