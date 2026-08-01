import json
from unittest.mock import MagicMock, patch

from frappe.tests.utils import FrappeTestCase

from frappe_field_sales.api import daily_sales_summary as api


class TestDailySalesSummaryUpload(FrappeTestCase):
	def setUp(self):
		self.payload = {
			"tag": "2026-07-26",
			"rapportId": "upload-1",
			"userId": "user-1",
			"userEmail": "sales@example.com",
			"entries": [{
				"localId": "entry-1",
				"rapportId": "rapport-1",
				"dateTime": "2026-07-25 10:30:00",
				"kunde": {"id": "CUSTOMER-1", "name": "Customer One"},
				"title": "Visit",
				"text": "Successful visit",
				"checklist": {"Demo": True},
				"carts": {
					"verkaufVorOrt": [{"artikelId": 101, "quantity": 2}],
					"telefonVerkauf": [],
					"musterbestellung": [{"artikelId": 202}],
				},
			}],
		}

	@patch.object(api, "make_daily_sales_summary", return_value="DSS-2026-00001")
	@patch.object(api, "make_sales_order_for_cart")
	def test_upload_creates_orders_and_summary(self, make_order, make_summary):
		make_order.side_effect = ["SO-ON-SITE", None, "SO-SAMPLE"]
		result = api.upload_daily_sales_summary(json.dumps(self.payload))
		self.assertEqual(result["daily_sales_summary"], "DSS-2026-00001")
		self.assertEqual([row["cartType"] for row in result["created_sales_orders"]], ["verkaufVorOrt", "musterbestellung"])
		make_summary.assert_called_once_with(self.payload, result["created_sales_orders"])

	@patch.object(api, "get_item_code_from_artikel_id", side_effect=["ITEM-1", "ITEM-2"])
	@patch.object(api.frappe, "get_doc")
	def test_sales_order_maps_payload(self, get_doc, get_item):
		doc = MagicMock()
		doc.name = "SO-1"
		get_doc.return_value = doc
		result = api.make_sales_order_for_cart(
			self.payload["entries"][0],
			[{"artikelId": 101, "quantity": 3}, {"artikelId": 202}],
			self.payload,
		)
		self.assertEqual(result, "SO-1")
		order = get_doc.call_args.args[0]
		self.assertEqual(order["customer"], "CUSTOMER-1")
		self.assertEqual(order["items"], [{"item_code": "ITEM-1", "qty": 3}, {"item_code": "ITEM-2", "qty": 1}])
		self.assertEqual(str(order["transaction_date"]), "2026-07-25")
		doc.insert.assert_called_once_with(ignore_permissions=True)

	@patch.object(api, "get_default_company", return_value="Test Company")
	@patch.object(api, "get_sales_person_for_payload", return_value="Sales Person 1")
	@patch.object(api.frappe, "get_doc")
	def test_summary_links_party_and_orders(self, get_doc, get_sales_person, get_company):
		doc = MagicMock()
		doc.name = "DSS-1"
		get_doc.return_value = doc
		orders = [
			{"entryLocalId": "entry-1", "cartType": "verkaufVorOrt", "salesOrder": "SO-1"},
			{"entryLocalId": "entry-1", "cartType": "musterbestellung", "salesOrder": "SO-2"},
		]
		self.assertEqual(api.make_daily_sales_summary(self.payload, orders), "DSS-1")
		summary = get_doc.call_args.args[0]
		row = summary["sales_report"][0]
		self.assertEqual((row["party_type"], row["party"]), ("Customer", "CUSTOMER-1"))
		self.assertEqual((row["on_site_sale"], row["sample_order"]), ("SO-1", "SO-2"))
		self.assertEqual(row["demo_given"], 1)
		doc.insert.assert_called_once_with(ignore_permissions=True)

	@patch.object(api.frappe.db, "get_value", return_value=None)
	@patch.object(api.frappe, "get_all", return_value=["Fallback Company"])
	def test_default_company_fallback(self, get_all, get_value):
		self.assertEqual(api.get_default_company(), "Fallback Company")

	@patch.object(api.frappe.db, "sql", return_value=[])
	def test_unknown_artikel_id_throws(self, sql):
		with self.assertRaises(Exception):
			api.get_item_code_from_artikel_id(999)
