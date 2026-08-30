import hashlib

import frappe


JAVASCRIPT_MAX_SAFE_INTEGER = (1 << 53) - 1
ITEM_CODE_HASH_SQL = "CONV(SUBSTRING(CAST(SHA(i.name) AS CHAR), 1, 16), 16, 10)"


def get_artikel_id(item_code: str) -> int:
	"""Map an Item code to the ID used by JavaScript clients."""
	hash_prefix = hashlib.sha1(item_code.encode()).hexdigest()[:16]
	return int(hash_prefix, 16) % JAVASCRIPT_MAX_SAFE_INTEGER


def get_item_code_from_artikel_id(artikel_id: int) -> str:
	rows = frappe.db.sql(
		f"""
		SELECT i.name FROM `tabItem` i
		WHERE MOD({ITEM_CODE_HASH_SQL}, %s) = %s
		LIMIT 1
		""",
		(JAVASCRIPT_MAX_SAFE_INTEGER, artikel_id),
		as_dict=True,
	)
	if not rows:
		frappe.throw(f"No Item found for artikelId={artikel_id}")
	return rows[0]["name"]
