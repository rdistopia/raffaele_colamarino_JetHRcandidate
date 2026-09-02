from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database.db import (
    get_calculation_parameters,
    update_calculation_parameters,
    reset_db_to_seed
)

admin_bp = Blueprint("admin", __name__, url_prefix="/parametri")

def parse_rate(val_str: str) -> float:
    if not val_str:
        return 0.0
    cleaned = str(val_str).replace("%", "").strip().replace(",", ".")
    val = float(cleaned)
    return val / 100.0 if val > 1.0 else val

def parse_limit(val_str: str):
    if not val_str:
        return None
    cleaned = str(val_str).replace("€", "").strip().replace(".", "").replace(",", ".")
    if cleaned.lower() in ("", "nessun limite", "illimitato", "null", "none"):
        return None
    return float(cleaned)

@admin_bp.route("/", methods=["GET", "POST"])
def parameters_view():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "reset":
            reset_db_to_seed()
            flash("Parametri ripristinati con successo ai valori predefiniti Jet HR.", "success")
            return redirect(url_for("admin.parameters_view"))

        try:
            # 1. Global & Municipal settings
            raw_inps = request.form.get("inps_rate", "9.19")
            inps_rate = parse_rate(raw_inps)
            default_months = int(request.form.get("default_months", 13))

            raw_mun_rate = request.form.get("mun_rate", "0.8")
            mun_rate = parse_rate(raw_mun_rate)

            raw_mun_thresh = request.form.get("mun_threshold", "23000")
            mun_threshold = parse_limit(raw_mun_thresh) or 23000.0

            update_data = {
                "inps_employee_rate": inps_rate,
                "default_months": default_months,
                "municipal_rate": mun_rate,
                "municipal_threshold": mun_threshold
            }

            # 2. Scaglioni IRPEF Nazionali
            irpef_ids = request.form.getlist("irpef_id[]")
            if irpef_ids:
                irpef_list = []
                for b_id in irpef_ids:
                    min_val = parse_limit(request.form.get(f"irpef_min_{b_id}")) or 0.0
                    max_val = parse_limit(request.form.get(f"irpef_max_{b_id}"))
                    rate_val = parse_rate(request.form.get(f"irpef_rate_{b_id}"))
                    irpef_list.append({
                        "id": int(b_id),
                        "min_income": min_val,
                        "max_income": max_val,
                        "rate": rate_val
                    })
                update_data["irpef_brackets"] = irpef_list

            # 3. Scaglioni Addizionale Regionale Lombardia
            regional_ids = request.form.getlist("regional_id[]")
            if regional_ids:
                regional_list = []
                for r_id in regional_ids:
                    min_val = parse_limit(request.form.get(f"regional_min_{r_id}")) or 0.0
                    max_val = parse_limit(request.form.get(f"regional_max_{r_id}"))
                    rate_val = parse_rate(request.form.get(f"regional_rate_{r_id}"))
                    regional_list.append({
                        "id": int(r_id),
                        "min_income": min_val,
                        "max_income": max_val,
                        "rate": rate_val
                    })
                update_data["regional_brackets"] = regional_list

            update_calculation_parameters(update_data)
            flash("Tutti i parametri e gli scaglioni sono stati aggiornati con successo nel database.", "success")
        except Exception as e:
            flash(f"Errore durante l'aggiornamento dei parametri: {str(e)}", "danger")

        return redirect(url_for("admin.parameters_view"))

    params = get_calculation_parameters()
    return render_template("parameters.html", params=params)
