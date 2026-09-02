from flask import Blueprint, request, jsonify
from ..core.calculator import calculate_net_salary
from ..core.models import CalculationInput
from ..database.db import get_calculation_parameters

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json() or {}
    try:
        ral = float(data.get("ral", 30000.0))
        months = int(data.get("months", 13))
        region = data.get("region", "Lombardia")
        municipality = data.get("municipality", "Milano")

        calc_in = CalculationInput(
            ral=ral,
            months=months,
            region=region,
            municipality=municipality
        )
        result = calculate_net_salary(calc_in)
        return jsonify({
            "status": "success",
            "data": result.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": f"Dati non validi: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/parameters", methods=["GET"])
def api_parameters():
    params = get_calculation_parameters()
    return jsonify({
        "status": "success",
        "data": params
    }), 200
