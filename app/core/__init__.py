"""
Core calculation engine for Jet HR RAL-to-Net prototype.
This package is pure Python and isolated from web frameworks.
"""

from .calculator import calculate_net_salary
from .models import CalculationInput, CalculationBreakdown
from .formatters import format_number_it, format_currency_it, format_percent_it

__all__ = [
    "calculate_net_salary",
    "CalculationInput",
    "CalculationBreakdown",
    "format_number_it",
    "format_currency_it",
    "format_percent_it"
]
