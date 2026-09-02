from typing import List, Dict, Any, Tuple

def calculate_progressive_tax(income: float, brackets: List[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Calcola l'imposta progressiva a scaglioni.
    Ogni elemento di brackets deve contenere:
      - 'min_income': float
      - 'max_income': float | None
      - 'rate': float (es. 0.23 per 23%)
    """
    total_tax = 0.0
    breakdown = []

    for b in brackets:
        min_inc = float(b["min_income"])
        max_inc = float(b["max_income"]) if b["max_income"] is not None else float("inf")
        rate = float(b["rate"])

        if income > min_inc:
            taxable_slice = min(income, max_inc) - min_inc
            tax_slice = taxable_slice * rate
            total_tax += tax_slice

            def _fmt_k(val: float) -> str:
                return f"{val:,.0f}".replace(",", ".")

            label = f"Fino a {_fmt_k(max_inc)} €" if max_inc != float("inf") else f"Oltre {_fmt_k(min_inc)} €"
            if min_inc > 0 and max_inc != float("inf"):
                label = f"Da {_fmt_k(min_inc)} € a {_fmt_k(max_inc)} €"

            breakdown.append({
                "label": label,
                "taxable_amount": round(taxable_slice, 2),
                "rate_percent": round(rate * 100, 2),
                "tax_amount": round(tax_slice, 2)
            })

    return round(total_tax, 2), breakdown

def calculate_municipal_tax(income: float, threshold: float = 23000.0, rate: float = 0.008) -> float:
    """
    Calcola l'addizionale comunale secondo la metodologia documentata da Jet HR:
    - Sotto la soglia di esenzione (es. 23.000 €): 0 €
    - Sopra la soglia: aliquota applicata sulla quota eccedente la soglia.
    """
    if income <= threshold:
        return 0.0
    taxable_excess = income - threshold
    return round(taxable_excess * rate, 2)
