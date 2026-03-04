frappe.ui.form.on("Daily Sales Summary", {
	onload: function (frm) {
		if (frm.doc.__islocal && !frm.doc.uuid) {
			frm.set_value("uuid", frappe.utils.get_random_string(10));
		}
	},
	before_save: function (frm) {
		if (!frm.doc.uuid) {
			frm.set_value("uuid", frappe.utils.get_random_string(10));
		}
	},
});
