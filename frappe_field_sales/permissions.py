# Copyright (c) 2025, AVANT ICONIC and contributors
# For license information, please see license.txt

import frappe


def get_sales_visit_permission_query_conditions(user, doctype=None):
	return _company_permission_condition(user, "Sales Visit", "company")


def get_mutation_log_permission_query_conditions(user, doctype=None):
	return _company_permission_condition(user, "Mutation Log", "company")


def get_daily_sales_summary_permission_query_conditions(user, doctype=None):
	return _company_permission_condition(user, "Daily Sales Summary", "company")


def get_vehicle_log_permission_query_conditions(user, doctype=None):
	return _company_permission_condition(user, "Vehicle Log", "custom_company")


def _company_permission_condition(user, doctype, company_field):
	if not user:
		user = frappe.session.user
	user_perms = frappe.get_user_permissions(user=user)
	allowed = user_perms.get("Company")
	if not allowed:
		return ""
	companies = [p.get("doc") for p in allowed if p.get("doc")]
	if not companies:
		return ""
	escaped = ", ".join(frappe.db.escape(c) for c in companies)
	return f"`tab{doctype}`.`{company_field}` in ({escaped})"


def set_default_company(doc, method=None):
	if doc.get("__islocal") and not doc.get("company") and hasattr(doc, "company"):
		doc.company = frappe.defaults.get_user_default("company")
	if doc.get("__islocal") and not doc.get("custom_company") and hasattr(doc, "custom_company"):
		doc.custom_company = frappe.defaults.get_user_default("company")
