import os
import tempfile
import pytest
from app.database.db import (
    init_db,
    get_calculation_parameters,
    update_calculation_parameters,
    reset_db_to_seed
)

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(path)
    yield path
    if os.path.exists(path):
        os.remove(path)

def test_db_init_and_defaults(temp_db):
    params = get_calculation_parameters(db_path=temp_db)
    assert params["inps_employee_rate"] == 0.0919
    assert params["default_months"] == 13
    assert len(params["irpef_brackets"]) == 3
    assert params["municipal_settings"]["threshold"] == 23000.0
    assert params["municipal_settings"]["rate"] == 0.008

def test_update_and_reset_parameters(temp_db):
    # Modifica aliquota INPS, addizionale comunale e scaglioni IRPEF
    params = get_calculation_parameters(db_path=temp_db)
    first_irpef_id = params["irpef_brackets"][0]["id"]
    first_regional_id = params["regional_brackets"][0]["id"]

    update_calculation_parameters({
        "inps_employee_rate": 0.10,
        "default_months": 14,
        "municipal_rate": 0.01,
        "municipal_threshold": 25000.0,
        "irpef_brackets": [
            {"id": first_irpef_id, "min_income": 0.0, "max_income": 30000.0, "rate": 0.20}
        ],
        "regional_brackets": [
            {"id": first_regional_id, "min_income": 0.0, "max_income": 16000.0, "rate": 0.01}
        ]
    }, db_path=temp_db)

    updated = get_calculation_parameters(db_path=temp_db)
    assert updated["inps_employee_rate"] == 0.10
    assert updated["default_months"] == 14
    assert updated["municipal_settings"]["rate"] == 0.01
    assert updated["municipal_settings"]["threshold"] == 25000.0
    assert updated["irpef_brackets"][0]["max_income"] == 30000.0
    assert updated["irpef_brackets"][0]["rate"] == 0.20
    assert updated["regional_brackets"][0]["max_income"] == 16000.0
    assert updated["regional_brackets"][0]["rate"] == 0.01

    # Reset ai default
    reset_db_to_seed(db_path=temp_db)
    reset_params = get_calculation_parameters(db_path=temp_db)
    assert reset_params["inps_employee_rate"] == 0.0919
    assert reset_params["default_months"] == 13
    assert reset_params["municipal_settings"]["threshold"] == 23000.0
    assert reset_params["irpef_brackets"][0]["max_income"] == 28000.0
    assert reset_params["irpef_brackets"][0]["rate"] == 0.23
