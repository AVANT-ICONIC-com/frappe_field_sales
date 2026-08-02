import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, getdate


class SalesVisit(Document):
	def on_update(self):
		self._sync_linked_event()

	def _sync_linked_event(self):
		starts_on = self._event_datetime()
		event_name = getattr(self, "event", None)
		if event_name and frappe.db.exists("Event", event_name):
			ev = frappe.get_doc("Event", event_name)
			ev.set("subject", getattr(self, "title", None) or ev.get("subject"))
			ev.set("starts_on", starts_on or ev.get("starts_on"))
			if ev.get("starts_on") and not ev.get("ends_on"):
				ev.set("ends_on", ev.get("starts_on"))
			ev.set("reference_doctype", "Sales Visit")
			ev.set("reference_docname", self.name)
			ev.save(ignore_permissions=True)
			return
		title = getattr(self, "title", None)
		if not starts_on or not title:
			return
		ev = frappe.get_doc({
			"doctype": "Event",
			"subject": title,
			"starts_on": starts_on,
			"ends_on": starts_on,
			"event_type": "Private",
			"reference_doctype": "Sales Visit",
			"reference_docname": self.name,
		})
		ev.insert(ignore_permissions=True)
		self.db_set("event", ev.name)

	def _event_datetime(self):
		event_date = getattr(self, "event_date", None)
		if not event_date:
			return None
		d = getdate(event_date)
		return get_datetime(d) if d else None
