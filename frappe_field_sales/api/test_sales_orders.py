from unittest.mock import call, patch

from frappe.tests.utils import FrappeTestCase

from frappe_field_sales.api import sales_orders as api


class TestSalesOrdersForItem(FrappeTestCase):
	@patch.object(api, "get_item_code_from_artikel_id", return_value="ITEM-ABC")
	@patch.object(api.frappe, "get_all")
	def test_returns_orders_referenced_by_matching_items(self, get_all, get_item_code):
		orders = [{"name": "SO-2"}, {"name": "SO-1"}]
		get_all.side_effect = [["SO-2", "SO-1", "SO-2"], orders]

		result = api.get_sales_orders_for_item("731360863466654")

		self.assertEqual(result, orders)
		get_item_code.assert_called_once_with(731360863466654)
		self.assertEqual(
			get_all.call_args_list,
			[
				call(
					"Sales Order Item",
					filters={
						"parenttype": "Sales Order",
						"parentfield": "items",
						"item_code": "ITEM-ABC",
					},
					pluck="parent",
				),
				call(
					"Sales Order",
					filters={"name": ["in", ["SO-2", "SO-1"]]},
					fields=api.SALES_ORDER_FIELDS,
					order_by="transaction_date desc, modified desc",
				),
			],
		)

	@patch.object(api, "get_item_code_from_artikel_id", return_value="ITEM-ABC")
	@patch.object(api.frappe, "get_all", return_value=[])
	def test_returns_empty_list_without_matching_items(self, get_all, get_item_code):
		self.assertEqual(api.get_sales_orders_for_item(123), [])
		get_all.assert_called_once()

	@patch.object(api.frappe, "throw", side_effect=ValueError)
	def test_rejects_invalid_numeric_id(self, throw):
		with self.assertRaises(ValueError):
			api.get_sales_orders_for_item("not-a-number")
		throw.assert_called_once_with("numericId must be an integer")

	@patch.object(api.frappe, "throw", side_effect=ValueError)
	def test_rejects_unsafe_numeric_id(self, throw):
		with self.assertRaises(ValueError):
			api.get_sales_orders_for_item(api.JAVASCRIPT_MAX_SAFE_INTEGER + 1)
		throw.assert_called_once_with(
			f"numericId must be between 0 and {api.JAVASCRIPT_MAX_SAFE_INTEGER}"
		)
