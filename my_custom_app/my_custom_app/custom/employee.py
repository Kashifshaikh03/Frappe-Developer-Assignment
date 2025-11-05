import frappe
from frappe.utils import nowdate
from frappe.utils.pdf import get_pdf

def before_save(doc, method=None):
    """Auto-manage lifecycle based on joining, probation, and exit"""
    today = nowdate()

    # --- Auto Confirm ---
    if doc.custom_probation_date and not doc.custom_exit_date:
        if doc.custom_probation_date <= today:
            doc.custom_lifecycle_status = "Confirmed"
            doc.status = "Active"

    # --- Auto Exit ---
    if doc.custom_exit_date:
        if doc.custom_exit_date <= today:
            doc.custom_lifecycle_status = "Exited"
            doc.status = "Left"

    # --- Default Joining ---
    if not doc.custom_lifecycle_status:
        doc.custom_lifecycle_status = "Joining"
        doc.status = "Active"


def after_save(doc, method=None):
    """Auto-generate Experience Letter (PDF) when employee exits"""
    if doc.custom_lifecycle_status == "Exited" or doc.status == "Left":
        try:
            print_format_name = "Standard"
            html = frappe.get_print("Employee", doc.name, print_format_name)
            pdf_data = get_pdf(html)

            file = frappe.get_doc({
                "doctype": "File",
                "file_name": f"Employee_Exit_{doc.name}.pdf",
                "attached_to_doctype": "Employee",
                "attached_to_name": doc.name,
                "is_private": 1,
                "content": pdf_data,
                "decode": False
            })
            file.insert(ignore_permissions=True)
            frappe.msgprint("✅ Employee Exit PDF auto-generated and attached.")
        except Exception as e:
            frappe.log_error(message=str(e), title="Employee Exit PDF Generation Failed")
