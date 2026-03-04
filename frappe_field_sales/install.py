import frappe


def after_install():
	_add_lead_custom_fields()
	_add_item_custom_fields()


def _add_lead_custom_fields():
	dt = "Lead"
	fields = [
		{"fieldname": "next_visit_date", "fieldtype": "Date", "label": "Next Visit Date", "insert_after": "status"},
		{"fieldname": "next_visit_comment", "fieldtype": "Small Text", "label": "Next Visit Comment", "insert_after": "next_visit_date"},
		{"fieldname": "customer_notes", "fieldtype": "Text Editor", "label": "Customer Notes", "insert_after": "next_visit_comment"},
		{"fieldname": "preferred_language", "fieldtype": "Data", "label": "Preferred Language", "insert_after": "customer_notes"},
		{"fieldname": "revenue_total", "fieldtype": "Currency", "label": "Revenue Total", "insert_after": "preferred_language", "options": "currency"},
	]
	for f in fields:
		_add_custom_field_if_missing(dt, f)


def _add_item_custom_fields():
	dt = "Item"
	fields = [
		{"fieldname": "title_french", "fieldtype": "Data", "label": "Title (French)", "insert_after": "item_name"},
		{"fieldname": "description_french", "fieldtype": "Text Editor", "label": "Description (French)", "insert_after": "description"},
		{"fieldname": "sales_arguments_german", "fieldtype": "Small Text", "label": "Sales Arguments (German)", "insert_after": "description_french"},
		{"fieldname": "sales_arguments_french", "fieldtype": "Small Text", "label": "Sales Arguments (French)", "insert_after": "sales_arguments_german"},
		{"fieldname": "back_ordered", "fieldtype": "Check", "label": "Back Ordered", "insert_after": "sales_arguments_french", "default": "0"},
		{"fieldname": "do_not_order", "fieldtype": "Check", "label": "Do Not Order", "insert_after": "back_ordered", "default": "0"},
		{"fieldname": "collection_stop", "fieldtype": "Check", "label": "Collection Stop", "insert_after": "do_not_order", "default": "0"},
	]
	for f in fields:
		_add_custom_field_if_missing(dt, f)


def _add_custom_field_if_missing(dt, field_def):
	fieldname = field_def["fieldname"]
	if frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fieldname}):
		return
	doc = frappe.get_doc({
		"doctype": "Custom Field",
		"dt": dt,
		"fieldname": fieldname,
		"fieldtype": field_def["fieldtype"],
		"label": field_def["label"],
		"insert_after": field_def.get("insert_after"),
		"options": field_def.get("options"),
		"default": field_def.get("default"),
	})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
