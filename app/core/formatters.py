from typing import Any, Optional

def format_number_it(value: Any, decimals: int = 2) -> str:
    """
    Formatta un valore numerico secondo lo standard italiano:
    - Punto (.) per separatore delle migliaia
    - Virgola (,) per separatore dei decimali
    Esempio:
      27456.78 -> "27.456,78"
      30000 -> "30.000,00" (se decimals=2)
      15000 -> "15.000" (se decimals=0)
    """
    if value is None:
        return "0," + ("0" * decimals) if decimals > 0 else "0"

    try:
        val_float = float(value)
    except (ValueError, TypeError):
        return str(value)

    # Formattazione en standard: 27,456.78
    formatted_en = f"{val_float:,.{decimals}f}"
    # Inversione per standard italiano: 27.456,78
    return formatted_en.replace(",", "X").replace(".", ",").replace("X", ".")

def format_currency_it(value: Any) -> str:
    """Formatta come valuta con 2 decimali e simbolo €: '27.456,78 €'"""
    return f"{format_number_it(value, 2)} €"

def format_percent_it(value: Any, decimals: int = 2) -> str:
    """Formatta come percentuale con virgola per decimali: '9,19%'"""
    return f"{format_number_it(value, decimals)}%"
