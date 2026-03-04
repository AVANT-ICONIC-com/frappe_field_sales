frappe.ui.form.on("Item", {
	refresh: function (frm) {
		var show_sales_args = (frappe.user_roles || []).indexOf("Sales User") !== -1 ||
			(frappe.user_roles || []).indexOf("System Manager") !== -1;
		["sales_arguments_german", "sales_arguments_french"].forEach(function (fieldname) {
			if (frm.meta.get_field(fieldname)) {
				frm.set_df_property(fieldname, "hidden", !show_sales_args);
			}
		});
	},
});
