# Copyright (c) 2025, kashif  and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}
    applicants = frappe.get_all(
        "Job Applicant",
        fields=["custom_source_of_application"]
    )

    data = {}
    for a in applicants:
        src = a.custom_source_of_application or "Not Specified"
        data[src] = data.get(src, 0) + 1

    return (
        [
            {
			"label": "Source of Application", 
			"fieldname": "custom_source_of_application", 
			"fieldtype": "Data", 
			"width": 250
			},

            {
			"label": "Total Applicants", 
			"fieldname": "total_applicants", 
			"fieldtype": "Int", 
			"width": 150
			},
        ],
        [{"custom_source_of_application": s, "total_applicants": c} for s, c in data.items()]
    )
