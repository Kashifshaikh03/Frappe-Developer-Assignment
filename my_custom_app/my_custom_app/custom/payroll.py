import frappe

def set_salary_structure_based_on_regime(doc, method):
    """Automatically set salary structure and fetch investment declarations"""
    for row in doc.employees:
        emp = frappe.get_doc("Employee", row.employee)
        regime = emp.custom_tax_regime_preference or "New Regime"

        structure = (
            "Old Regime Structure"
            if regime == "Old Regime"
            else "New Regime Structure"
        )
        row.salary_structure = structure

        investment = frappe.db.get_value(
            "Employee Investment Declaration",
            {"employee": row.employee},
            ["section_80c", "section_80d", "other_exemptions"],
            as_dict=True
        )

        total_investment = 0
        if investment:
            total_investment = (
                (investment.section_80c or 0)
                + (investment.section_80d or 0)
                + (investment.other_exemptions or 0)
            )

        # Store this in child table (optional but visible in DB)
        row.total_investment = total_investment
