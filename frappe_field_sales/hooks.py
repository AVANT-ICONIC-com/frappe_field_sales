app_name = "frappe_field_sales"
app_title = "Frappe Field Sales"
app_publisher = "AVANT ICONIC"
app_description = "Custom field sales app: Sales Visit, Rapport, Vehicle Log, get_aussendienst_items, company-based access."
app_email = "rico@avant-iconic.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Whitelist API methods (callable via frappe.call)
# ------------------
whitelist = ["frappe_field_sales.api.items.get_aussendienst_items"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "frappe_field_sales",
# 		"logo": "/assets/frappe_field_sales/logo.png",
# 		"title": "Frappe Field Sales",
# 		"route": "/frappe_field_sales",
# 		"has_permission": "frappe_field_sales.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_field_sales/css/frappe_field_sales.css"
# app_include_js = "/assets/frappe_field_sales/js/frappe_field_sales.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_field_sales/css/frappe_field_sales.css"
# web_include_js = "/assets/frappe_field_sales/js/frappe_field_sales.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_field_sales/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Vehicle Log": "public/js/vehicle_log.js",
	"Item": "public/js/item.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "frappe_field_sales/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "frappe_field_sales.utils.jinja_methods",
# 	"filters": "frappe_field_sales.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "frappe_field_sales.install.before_install"
after_install = "frappe_field_sales.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappe_field_sales.uninstall.before_uninstall"
# after_uninstall = "frappe_field_sales.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "frappe_field_sales.utils.before_app_install"
# after_app_install = "frappe_field_sales.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "frappe_field_sales.utils.before_app_uninstall"
# after_app_uninstall = "frappe_field_sales.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_field_sales.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Sales Visit": "frappe_field_sales.permissions.get_sales_visit_permission_query_conditions",
	"Mutation Log": "frappe_field_sales.permissions.get_mutation_log_permission_query_conditions",
	"Daily Sales Summary": "frappe_field_sales.permissions.get_daily_sales_summary_permission_query_conditions",
	"Vehicle Log": "frappe_field_sales.permissions.get_vehicle_log_permission_query_conditions",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Visit": {"before_insert": "frappe_field_sales.permissions.set_default_company"},
	"Mutation Log": {"before_insert": "frappe_field_sales.permissions.set_default_company"},
	"Daily Sales Summary": {"before_insert": "frappe_field_sales.permissions.set_default_company"},
	"Vehicle Log": {"before_insert": "frappe_field_sales.permissions.set_default_company"},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_field_sales.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_field_sales.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_field_sales.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_field_sales.tasks.weekly"
# 	],
# 	"monthly": [
# 		"frappe_field_sales.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "frappe_field_sales.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_field_sales.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "frappe_field_sales.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["frappe_field_sales.utils.before_request"]
# after_request = ["frappe_field_sales.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappe_field_sales.utils.before_job"]
# after_job = ["frappe_field_sales.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"frappe_field_sales.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

