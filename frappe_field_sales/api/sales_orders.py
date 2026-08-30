from typing import Any

import frappe

from frappe_field_sales.api.item_ids import (
	JAVASCRIPT_MAX_SAFE_INTEGER,
	get_item_code_from_artikel_id,
)


SALES_ORDER_FIELDS = [
	"name",
	"customer",
	"customer_name",
	"transaction_date",
	"delivery_date",
	"status",
	"grand_total",
	"currency",
	"docstatus",
]


@frappe.whitelist(allow_guest=False)
def get_sales_orders_for_item(numericId: int | str) -> list[dict[str, Any]]:
	"""Return Sales Orders containing the item identified by ``numericId``."""
	try:
		numeric_id = int(numericId)
	except (TypeError, ValueError, OverflowError):
		frappe.throw("numericId must be an integer")

	if numeric_id < 0 or numeric_id > JAVASCRIPT_MAX_SAFE_INTEGER:
		frappe.throw(f"numericId must be between 0 and {JAVASCRIPT_MAX_SAFE_INTEGER}")

	item_code = get_item_code_from_artikel_id(numeric_id)
	order_names = frappe.get_all(
		"Sales Order Item",
		filters={
			"parenttype": "Sales Order",
			"parentfield": "items",
			"item_code": item_code,
		},
		pluck="parent",
	)
	order_names = list(dict.fromkeys(order_names))
	if not order_names:
		return []

	return frappe.get_all(
		"Sales Order",
		filters={"name": ["in", order_names]},
		fields=SALES_ORDER_FIELDS,
		order_by="transaction_date desc, modified desc",
	)
