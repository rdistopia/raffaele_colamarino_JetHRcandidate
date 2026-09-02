from app.core.formatters import format_number_it, format_currency_it, format_percent_it

def test_italian_number_formatting():
    # Verifica punto per le migliaia e virgola per i decimali
    assert format_number_it(27456.78, 2) == "27.456,78"
    assert format_number_it(30000, 2) == "30.000,00"
    assert format_number_it(15000, 0) == "15.000"
    assert format_number_it(0, 2) == "0,00"

def test_italian_currency_formatting():
    assert format_currency_it(22609.54) == "22.609,54 €"
    assert format_currency_it(30000) == "30.000,00 €"
    assert format_currency_it(33.94) == "33,94 €"

def test_italian_percent_formatting():
    assert format_percent_it(9.19, 2) == "9,19%"
    assert format_percent_it(24.63, 1) == "24,6%"
    assert format_percent_it(0.8, 2) == "0,80%"
