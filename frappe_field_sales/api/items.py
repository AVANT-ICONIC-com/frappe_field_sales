import json
from typing import Any

import frappe


STATUS_BACK_ORDERED = "backOrdered"
STATUS_NOT_ORDERED_FROM_SUPPLIER = "notOrderedFromSupplier"
STATUS_AVAILABLE = "available"
STATUS_STRICTLY_DO_NOT_ORDER = "strictlyDoNotOrder"
STATUS_DO_NOT_ORDER = "doNotOrder"


@frappe.whitelist(allow_guest=False)
def get_aussendienst_items(numericIdFilter=None):
	numeric_ids = None
	if numericIdFilter:
		try:
			raw = json.loads(numericIdFilter) if isinstance(numericIdFilter, str) else numericIdFilter
			numeric_ids = [int(x) for x in raw] if raw else None
		except (TypeError, ValueError):
			pass

	item_meta = frappe.get_meta("Item")
	has_numeric_id = bool(item_meta.get_field("numeric_id"))

	filters: dict[str, Any] = {"disabled": 0}
	if numeric_ids is not None and has_numeric_id:
		filters["numeric_id"] = ["in", [str(n) for n in numeric_ids]]
	elif numeric_ids is not None:
		filters["name"] = ["in", [str(n) for n in numeric_ids]]

	fields = [
		"name", "item_code", "item_name", "description", "image", "stock_uom",
		"end_of_life",
	]
	if item_meta.get_field("numeric_id"):
		fields.append("numeric_id")
	if item_meta.get_field("back_ordered"):
		fields.append("back_ordered")
	if item_meta.get_field("do_not_order"):
		fields.append("do_not_order")
	if item_meta.get_field("collection_stop"):
		fields.append("collection_stop")

	items = frappe.get_all("Item", filters=filters, fields=fields)

	result = []
	for item in items:
		item_doc = frappe._dict(item)
		result.append(_build_erp_next_item(item_doc))
	return result


def _build_erp_next_item(item_doc):
	item_code = item_doc.get("item_code") or item_doc.get("name") or ""
	numeric_id = item_doc.get("numeric_id") or item_code
	status = _derive_status(item_doc)
	default_price, default_currency = _get_default_price(item_code)
	prices = _get_item_prices(item_code)
	attachments = _get_item_attachments(item_code)
	actual_qty, projected_qty = _get_bin_qty(item_code)
	image_uri = None
	if item_doc.get("image"):
		utils = getattr(frappe, "utils", None)
		if utils:
			image_uri = utils.get_url(item_doc.image)

	return {
		"itemCode": item_code,
		"description": (item_doc.get("description") or item_doc.get("item_name") or item_code) or "",
		"imageUri": image_uri,
		"unit": item_doc.get("stock_uom") or "",
		"actualQty": actual_qty,
		"projectedQty": projected_qty,
		"supplierCount": 0,
		"blockedCount": 0,
		"defaultPrice": default_price,
		"defaultCurrency": default_currency,
		"endOfLife": (item_doc.get("end_of_life") or "").strip() or "",
		"numericId": str(numeric_id),
		"status": status,
		"prices": prices,
		"attachments": attachments,
	}


def _derive_status(item_doc):
	back_ordered = item_doc.get("back_ordered")
	do_not_order = item_doc.get("do_not_order")
	collection_stop = item_doc.get("collection_stop")
	if back_ordered:
		return STATUS_BACK_ORDERED
	if do_not_order and collection_stop:
		return STATUS_STRICTLY_DO_NOT_ORDER
	if do_not_order:
		return STATUS_DO_NOT_ORDER
	if collection_stop:
		return STATUS_NOT_ORDERED_FROM_SUPPLIER
	return STATUS_AVAILABLE


def _get_default_price(item_code):
	try:
		rate = frappe.db.get_value(
			"Item Price",
			{"item_code": item_code},
			"price_list_rate",
			order_by="modified desc",
		)
		currency = frappe.db.get_value(
			"Item Price",
			{"item_code": item_code},
			"currency",
			order_by="modified desc",
		)
		if rate is not None and isinstance(rate, (int, float)):
			return (float(rate), currency or None)
	except Exception:
		pass
	return (None, None)


def _get_item_prices(item_code):
	prices = []
	try:
		for row in frappe.get_all(
			"Item Price",
			filters={"item_code": item_code},
			fields=["price_list", "price_list_rate", "currency", "uom"],
			order_by="modified desc",
		):
			rate_val = row.get("price_list_rate")
			rate_num = float(rate_val) if isinstance(rate_val, (int, float)) else 0.0
			prices.append({
				"priceList": row.get("price_list") or "",
				"rate": rate_num,
				"currency": row.get("currency") or "",
				"uom": row.get("uom") or "",
			})
	except Exception:
		pass
	return prices


def _get_item_attachments(item_code):
	attachments = []
	try:
		for f in frappe.get_all(
			"File",
			filters={"attached_to_doctype": "Item", "attached_to_name": item_code},
			fields=["file_name", "file_url", "is_private"],
			order_by="creation desc",
		):
			attachments.append({
				"fileName": f.get("file_name") or "",
				"fileUrl": f.get("file_url") or "",
				"isPrivate": 1 if f.get("is_private") else 0,
				"attachedToField": None,
			})
	except Exception:
		pass
	return attachments


def _get_bin_qty(item_code):
	try:
		actual = frappe.db.get_value(
			"Bin",
			{"item_code": item_code},
			"actual_qty",
			order_by="modified desc",
		)
		projected = frappe.db.get_value(
			"Bin",
			{"item_code": item_code},
			"projected_qty",
			order_by="modified desc",
		)
		if actual is not None or projected is not None:
			a = float(actual) if isinstance(actual, (int, float)) else 0.0
			p = float(projected) if isinstance(projected, (int, float)) else 0.0
			return (a, p)
	except Exception:
		pass
	return (0.0, 0.0)
