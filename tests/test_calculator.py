import pytest
from app.core.calculator import calculate_net_salary
from app.core.models import CalculationInput

def test_jet_hr_official_example_30k():
    """
    Verifica che il motore di calcolo riproduca con precisione al centesimo
    l'esempio ufficiale documentato nell'Help Center di Jet HR per RAL 30.000 € a Milano.
    """
    calc_in = CalculationInput(
        ral=30000.0,
        months=13,
        region="Lombardia",
        municipality="Milano"
    )

    # Parametri conformi all'Help Center Jet HR
    params = {
        "inps_employee_rate": 0.0919,
        "default_months": 13,
        "irpef_brackets": [
            {"bracket_order": 1, "min_income": 0.0, "max_income": 28000.0, "rate": 0.23},
            {"bracket_order": 2, "min_income": 28000.0, "max_income": 50000.0, "rate": 0.35},
            {"bracket_order": 3, "min_income": 50000.0, "max_income": None, "rate": 0.43}
        ],
        "regional_brackets": [
            {"bracket_order": 1, "min_income": 0.0, "max_income": 15000.0, "rate": 0.0123},
            {"bracket_order": 2, "min_income": 15000.0, "max_income": 28000.0, "rate": 0.0158},
            {"bracket_order": 3, "min_income": 28000.0, "max_income": 50000.0, "rate": 0.0172},
            {"bracket_order": 4, "min_income": 50000.0, "max_income": None, "rate": 0.0173}
        ],
        "municipal_settings": {
            "threshold": 23000.0,
            "rate": 0.008
        },
        "deductions_settings": {
            "base_max_deduction": 1955.0,
            "tier1_limit": 15000.0,
            "tier2_limit": 28000.0,
            "tier3_limit": 50000.0,
            "tier2_base": 1910.0,
            "tier2_factor": 1190.0,
            "bonus_25_35k": 65.0
        }
    }

    res = calculate_net_salary(calc_in, parameters=params)

    # Step 1: Imponibile Fiscale
    assert res.inps_contributions == 2757.00
    assert res.taxable_income == 27243.00

    # Step 2: Imposte Lorde
    assert res.irpef_gross == 6265.89
    assert res.regional_tax == 377.94
    assert res.municipal_tax == 33.94
    assert abs(res.gross_taxes_total - 6677.76) <= 0.02

    # Step 3: Detrazioni
    assert res.deductions_amount == 2044.29

    # Step 4: Imposta Netta
    assert res.net_tax_effective == pytest.approx(4633.46, abs=0.05)

    # Step 5: Netto Annuale e Mensile
    assert res.net_annual == pytest.approx(22609.54, abs=0.05)
    assert res.net_monthly == round(res.net_annual / 13, 2)
