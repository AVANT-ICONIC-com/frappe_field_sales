import frappe
from frappe.model.document import Document


class DailySalesSummary(Document):
	def before_insert(self):
		if not self.get("uuid"):
			self.uuid = frappe.generate_hash(length=10)

	def validate(self):
		if self.get("__islocal") and not self.get("uuid"):
			self.uuid = frappe.generate_hash(length=10)
