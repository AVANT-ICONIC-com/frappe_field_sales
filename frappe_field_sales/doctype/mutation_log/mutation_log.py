import frappe
from frappe.model.document import Document


class MutationLog(Document):
	def validate(self):
		self._fetch_current_address_into_ro_fields()

	def _fetch_current_address_into_ro_fields(self):
		cur = getattr(self, "current_address", None)
		if not cur:
			for f in ("address_line_1_ro", "address_line_2_ro", "postal_code", "citytown", "stateprovince", "country"):
				self.set(f, None)
			return
		try:
			addr = frappe.get_doc("Address", cur)
		except Exception:
			return
		self.address_line_1_ro = (getattr(addr, "address_line1", None) or "") or ""
		self.address_line_2_ro = (getattr(addr, "address_line2", None) or "") or ""
		self.postal_code = (getattr(addr, "pincode", None) or "") or ""
		self.citytown = (getattr(addr, "city", None) or "") or ""
		self.stateprovince = (getattr(addr, "state", None) or "") or ""
		self.country = (getattr(addr, "country", None) or "") or ""
