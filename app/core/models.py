from dataclasses import dataclass, asdict
from typing import Dict, Any, List

@dataclass
class CalculationInput:
    ral: float
    months: int = 13
    region: str = "Lombardia"
    municipality: str = "Milano"

@dataclass
class TaxBracketBreakdown:
    description: str
    taxable_amount: float
    rate: float
    tax_amount: float

@dataclass
class CalculationBreakdown:
    # Input
    ral: float
    months: int
    region: str
    municipality: str

    # Step 1: Contributi
    inps_rate: float
    inps_contributions: float
    taxable_income: float

    # Step 2: Imposta Lorda
    irpef_gross: float
    irpef_brackets: List[Dict[str, Any]]
    regional_tax: float
    regional_brackets: List[Dict[str, Any]]
    municipal_tax: float
    gross_taxes_total: float

    # Step 3: Detrazioni
    deductions_amount: float

    # Step 4: Imposta Netta
    net_tax_effective: float

    # Step 5: Netto
    net_annual: float
    net_monthly: float
    total_retained: float
    tax_wedge_percent: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
