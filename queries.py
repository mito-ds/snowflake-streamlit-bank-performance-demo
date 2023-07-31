def get_bank_income_query(bank_names):
    # Format the list of bank names as a comma-separated string
    bank_names_string = ", ".join([f"'{name}'" for name in bank_names])

    return f"""
SELECT TO_DATE(ts.date) AS date, ts.value, ts.unit, ts.variable_name, ent.NAME FROM
cybersyn.financial_institution_timeseries AS ts
JOIN cybersyn.financial_institution_entities AS ent on (ts.ID_RSSD = ent.ID_RSSD)
WHERE ent.NAME in ({bank_names_string})
AND ts.date >= '2022-01-01'
AND VARIABLE_NAME in ('Total deposits', 'Estimated Insured Deposits', 'Total Interest Income', 'Net Operating Income')
AND UNIT = 'USD'
"""

# Why am I only getting 3 banks? Something with my filtering?


big_banks_query = """SELECT ent.NAME
    FROM cybersyn.financial_institution_timeseries as ts
    JOIN cybersyn.financial_institution_entities AS ent on (ts.ID_RSSD = ent.ID_RSSD)
    WHERE ts.variable = 'ASSET'
      AND ts.value > 1E11
      AND ts.date = '2022-12-31'
    ORDER BY ts.value desc;
"""



