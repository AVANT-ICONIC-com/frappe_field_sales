import json
from typing import Any

import frappe
from frappe.utils import getdate


CART_TYPES = ("verkaufVorOrt", "telefonVerkauf", "musterbestellung")


def get_item_code_from_artikel_id(artikel_id: int) -> str:
	rows = frappe.db.sql(
		"""
		SELECT i.name FROM `tabItem` i
		WHERE MOD(
			CONV(SUBSTRING(CAST(SHA(CONCAT(i.name)) AS CHAR), 1, 16), 16, 10),
			9007199254740991
		) = %s
		LIMIT 1
		""",
		(artikel_id,),
		as_dict=True,
	)
	if not rows:
		frappe.throw(f"No Item found for artikelId={artikel_id}")
	return rows[0]["name"]


def get_default_company() -> str:
	company = frappe.db.get_value("Global Defaults", None, "default_company")
	if company:
		return company
	companies = frappe.get_all("Company", pluck="name", limit=1)
	if companies:
		return companies[0]
	frappe.throw("No Company found. Daily Sales Summary requires a company.")


def get_sales_person_for_payload(payload: dict[str, Any]) -> str | None:
	user_id = payload.get("userEmail")
	if not user_id:
		return None
	rows = frappe.db.sql(
		"""
		SELECT sp.name FROM `tabSales Person` sp
		INNER JOIN `tabEmployee` e ON e.name = sp.employee
		WHERE e.user_id = %s
		LIMIT 1
		""",
		(user_id,),
		as_dict=True,
	)
	return rows[0]["name"] if rows else None


def make_sales_order_for_cart(
	entry: dict[str, Any], cart_items: list[dict[str, Any]], payload: dict[str, Any]
) -> str | None:
	if not cart_items:
		return None
	kunde = entry.get("kunde") or {}
	customer = kunde.get("id") or kunde.get("name")
	if not customer:
		frappe.throw(
			f"Entry {entry.get('localId')}: cannot create Sales Order without kunde.id or kunde.name"
		)
	items = [
		{"item_code": get_item_code_from_artikel_id(item["artikelId"]), "qty": item.get("quantity") or 1}
		for item in cart_items
	]
	order_date = getdate(entry.get("dateTime") or payload.get("tag"))
	sales_order = frappe.get_doc(
		{
			"doctype": "Sales Order",
			"customer": customer,
			"transaction_date": order_date,
			"delivery_date": order_date,
			"items": items,
		}
	)
	sales_order.insert(ignore_permissions=True)
	return sales_order.name


def make_daily_sales_summary(payload: dict[str, Any], created_sales_orders: list[dict[str, Any]]) -> str:
	orders_by_entry: dict[Any, dict[str, str]] = {}
	for row in created_sales_orders:
		orders_by_entry.setdefault(row.get("entryLocalId"), {})[row["cartType"]] = row["salesOrder"]

	sales_person = get_sales_person_for_payload(payload)
	sales_report = []
	for entry in payload.get("entries", []):
		entry_orders = orders_by_entry.get(entry.get("localId"), {})
		sales_report.append(
			{
				"party_type": "Customer",
				"party": (entry.get("kunde") or {}).get("id"),
				"sales_person": sales_person,
				"event": None,
				"report_title": entry.get("title"),
				"report_text": entry.get("text"),
				"demo_given": 1 if (entry.get("checklist") or {}).get("Demo") else 0,
				"on_site_sale": entry_orders.get("verkaufVorOrt"),
				"phone_sale": entry_orders.get("telefonVerkauf"),
				"sample_order": entry_orders.get("musterbestellung"),
			}
		)

	notes = [
		f"Upload UUID: {payload.get('rapportId')}",
		f"User ID: {payload.get('userId')}",
		f"User Email: {payload.get('userEmail')}",
	]
	summary = frappe.get_doc(
		{
			"doctype": "Daily Sales Summary",
			"naming_series": "DSS-.YYYY.-",
			"date": getdate(payload.get("tag")),
			"company": get_default_company(),
			"sent_by_email": 0,
			"uuid": payload.get("rapportId"),
			"notes": "<br>".join(note for note in notes if note),
			"sales_report": sales_report,
		}
	)
	summary.insert(ignore_permissions=True)
	return summary.name


@frappe.whitelist(allow_guest=False)
def upload_daily_sales_summary(payload: dict[str, Any] | str | None = None) -> dict[str, Any]:
	"""Create the upload's Sales Orders and Daily Sales Summary."""
	if payload is None:
		payload = frappe.request.get_json()
	elif isinstance(payload, str):
		payload = json.loads(payload)
	if not isinstance(payload, dict):
		frappe.throw("Daily Sales Summary payload must be a JSON object")

	created_sales_orders = []
	for entry in payload.get("entries", []):
		carts = entry.get("carts") or {}
		for cart_type in CART_TYPES:
			sales_order = make_sales_order_for_cart(entry, carts.get(cart_type) or [], payload)
			if sales_order:
				created_sales_orders.append(
					{
						"entryLocalId": entry.get("localId"),
						"entryRapportId": entry.get("rapportId"),
						"cartType": cart_type,
						"salesOrder": sales_order,
					}
				)

	daily_sales_summary = make_daily_sales_summary(payload, created_sales_orders)
	return {
		"payload": payload,
		"created_sales_orders": created_sales_orders,
		"daily_sales_summary": daily_sales_summary,
	}
