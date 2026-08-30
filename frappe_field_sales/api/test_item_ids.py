from unittest.mock import patch

from frappe.tests.utils import FrappeTestCase

from frappe_field_sales.api import item_ids


class TestItemIds(FrappeTestCase):
	def test_artikel_id_is_deterministic_and_javascript_safe(self):
		artikel_id = item_ids.get_artikel_id("ITEM-ABC")

		# Fixed vector also guards parity with MariaDB's SHA()/CONV() expression.
		self.assertEqual(artikel_id, 731360863466654)
		self.assertEqual(artikel_id, item_ids.get_artikel_id("ITEM-ABC"))
		self.assertGreaterEqual(artikel_id, 0)
		self.assertLessEqual(artikel_id, item_ids.JAVASCRIPT_MAX_SAFE_INTEGER)

	def test_hashes_are_roughly_evenly_distributed(self):
		bucket_counts = [0] * 16
		for number in range(1600):
			artikel_id = item_ids.get_artikel_id(f"ITEM-{number}")
			bucket = artikel_id * len(bucket_counts) // item_ids.JAVASCRIPT_MAX_SAFE_INTEGER
			bucket_counts[bucket] += 1

		self.assertLess(max(bucket_counts) - min(bucket_counts), 50)

	@patch.object(item_ids.frappe.db, "sql", return_value=[{"name": "ITEM-ABC"}])
	def test_reverse_lookup_uses_same_mapping(self, sql):
		artikel_id = item_ids.get_artikel_id("ITEM-ABC")

		self.assertEqual(item_ids.get_item_code_from_artikel_id(artikel_id), "ITEM-ABC")
		self.assertEqual(sql.call_args.args[1], (item_ids.JAVASCRIPT_MAX_SAFE_INTEGER, artikel_id))
