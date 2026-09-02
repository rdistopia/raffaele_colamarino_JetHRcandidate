from typing import Dict, Any, Optional
from .models import CalculationInput, CalculationBreakdown
from .taxes import calculate_progressive_tax, calculate_municipal_tax
from .deductions import calculate_employment_deductions

def calculate_net_salary(
    calc_input: CalculationInput,
    parameters: Optional[Dict[str, Any]] = None
) -> CalculationBreakdown:
    """
    Esegue il calcolo completo della retribuzione netta da RAL secondo i 5 step di Jet HR.
    """
    ral = float(calc_input.ral)
    months = int(calc_input.months) if calc_input.months > 0 else 13
    region = calc_input.region
    municipality = calc_input.municipality

    if parameters is None:
        from ..database.db import get_calculation_parameters
        parameters = get_calculation_parameters(region=region, municipality=municipality)

    # --------------------------------------------------------------------------
    # STEP 1: Contributi a carico del dipendente (IVS) e Imponibile Fiscale
    # --------------------------------------------------------------------------
    inps_rate = float(parameters.get("inps_employee_rate", 0.0919))
    inps_contributions = round(ral * inps_rate, 2)
    taxable_income = round(ral - inps_contributions, 2)

    # --------------------------------------------------------------------------
    # STEP 2: Calcola le imposte da pagare (Imposta Lorda)
    # --------------------------------------------------------------------------
    irpef_brackets = parameters.get("irpef_brackets", [])
    irpef_gross, irpef_breakdown = calculate_progressive_tax(taxable_income, irpef_brackets)

    regional_brackets = parameters.get("regional_brackets", [])
    regional_tax, regional_breakdown = calculate_progressive_tax(taxable_income, regional_brackets)

    mun_settings = parameters.get("municipal_settings", {"threshold": 23000.0, "rate": 0.008})
    municipal_tax = calculate_municipal_tax(
        taxable_income,
        threshold=float(mun_settings.get("threshold", 23000.0)),
        rate=float(mun_settings.get("rate", 0.008))
    )

    gross_taxes_total = round(irpef_gross + regional_tax + municipal_tax, 2)

    # --------------------------------------------------------------------------
    # STEP 3: Calcola le detrazioni da lavoro dipendente
    # --------------------------------------------------------------------------
    deduction_config = parameters.get("deductions_settings", {})
    deductions_amount = calculate_employment_deductions(taxable_income, deduction_config)

    # --------------------------------------------------------------------------
    # STEP 4: Calcola l'imposta effettiva da pagare (Imposta Netta)
    # --------------------------------------------------------------------------
    net_tax_effective = max(0.0, round(gross_taxes_total - deductions_amount, 2))

    # --------------------------------------------------------------------------
    # STEP 5: Ottieni il netto (annuale e mensile)
    # --------------------------------------------------------------------------
    net_annual = round(taxable_income - net_tax_effective, 2)
    net_monthly = round(net_annual / months, 2)
    total_retained = round(ral - net_annual, 2)
    wedge_percent = round((total_retained / ral) * 100, 2) if ral > 0 else 0.0

    return CalculationBreakdown(
        ral=ral,
        months=months,
        region=region,
        municipality=municipality,
        inps_rate=inps_rate,
        inps_contributions=inps_contributions,
        taxable_income=taxable_income,
        irpef_gross=irpef_gross,
        irpef_brackets=irpef_breakdown,
        regional_tax=regional_tax,
        regional_brackets=regional_breakdown,
        municipal_tax=municipal_tax,
        gross_taxes_total=gross_taxes_total,
        deductions_amount=deductions_amount,
        net_tax_effective=net_tax_effective,
        net_annual=net_annual,
        net_monthly=net_monthly,
        total_retained=total_retained,
        tax_wedge_percent=wedge_percent
    )
