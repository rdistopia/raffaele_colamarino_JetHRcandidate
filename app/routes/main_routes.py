from flask import Blueprint, render_template, request, flash
from ..core.calculator import calculate_net_salary
from ..core.models import CalculationInput
from ..database.db import get_calculation_parameters

main_bp = Blueprint("main", __name__)

def parse_currency(val_str: str) -> float:
    """
    Esegue il parsing flessibile degli importi inseriti dall'utente,
    supportando il formato italiano (es. 27.456,78 o 27456,78) e standard.
    """
    if not val_str:
        raise ValueError("Nessun valore inserito.")

    cleaned = str(val_str).strip().replace("€", "").replace(" ", "")

    if "." in cleaned and "," in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            # Formato italiano: 27.456,78 -> 27456.78
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            # Formato anglosassone: 27,456.78 -> 27456.78
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        # Solo virgola es. 27456,78
        cleaned = cleaned.replace(",", ".")
    elif "." in cleaned:
        parts = cleaned.split(".")
        if len(parts) == 2 and len(parts[1]) != 3:
            # Decimale con punto es. 27456.78 o 27456.5
            pass
        else:
            # Punto usato per le migliaia es. 30.000
            cleaned = cleaned.replace(".", "")

    return float(cleaned)

def format_currency_it(value: float) -> str:
    """Formatta un numero float nel formato italiano 27.456,78"""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@main_bp.route("/", methods=["GET", "POST"])
def index():
    params = get_calculation_parameters()
    result = None
    ral_val = 30000.0
    ral_display = "30.000,00"
    months_input = params.get("default_months", 13)

    if request.method == "POST":
        raw_ral = request.form.get("ral", "").strip()
        try:
            parsed_ral = parse_currency(raw_ral)
            if parsed_ral <= 0:
                flash("Inserisci una RAL maggiore di 0.", "danger")
            else:
                ral_val = parsed_ral
                ral_display = format_currency_it(ral_val)
                months_input = int(request.form.get("months", params.get("default_months", 13)))
                calc_in = CalculationInput(
                    ral=ral_val,
                    months=months_input,
                    region="Lombardia",
                    municipality="Milano"
                )
                result = calculate_net_salary(calc_in, parameters=params)
        except ValueError:
            flash("Valore RAL non valido. Inserisci un importo valido (es. 27.456,78).", "danger")
            ral_display = raw_ral

    return render_template(
        "calculator.html",
        result=result,
        ral_input=ral_val,
        ral_display=ral_display,
        months_input=months_input,
        params=params
    )
