frappe.ui.form.on("Vehicle Log Entry", {
	source_type: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.source_doctype = row.source_type === "Manually" ? "" : (row.source_type || "");
		frm.refresh_field("vehicle_log_entries");
	},
});
