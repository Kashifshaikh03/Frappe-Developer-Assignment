# Copyright (c) 2025, kashif  and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee"},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
        {"label": "Old Regime Tax", "fieldname": "old_tax", "fieldtype": "Currency"},
        {"label": "New Regime Tax", "fieldname": "new_tax", "fieldtype": "Currency"},
        {"label": "Preferred Regime", "fieldname": "preferred", "fieldtype": "Data"},
    ]

    data = []

    # Step 1: Get active employees only
    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "employee_name", "custom_tax_regime_preference"]
    )

    for emp in employees:
        # Step 2: Check if the employee has Salary Structure Assignment
        assigned_structures = frappe.get_all(
            "Salary Structure Assignment",
            filters={"employee": emp.name, "docstatus": 1},
            fields=["salary_structure"]
        )

        # Skip if employee has no structure assigned
        if not assigned_structures:
            continue

        # Extract salary structure names
        structures = [s.salary_structure for s in assigned_structures]

        # Process only if either Old or New Regime Structure assigned
        if "Old Regime Structure" in structures or "New Regime Structure" in structures:
            old_tax = calculate_tax(emp.name, "Old Regime Structure")
            new_tax = calculate_tax(emp.name, "New Regime Structure")

            data.append({
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "old_tax": old_tax,
                "new_tax": new_tax,
                "preferred": emp.custom_tax_regime_preference
            })

    return columns, data


def calculate_tax(employee, structure):
    """Fetch total deduction (tax) from submitted Salary Slips for the given structure."""
    slips = frappe.get_all(
        "Salary Slip",
        filters={"employee": employee, "salary_structure": structure, "docstatus": 1},
        fields=["total_deduction"]
    )

    total = 0
    for slip in slips:
        total += slip.total_deduction or 0
    return total
