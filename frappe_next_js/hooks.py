from . import __version__ as app_version

app_name = "frappe_next_js"
app_title = "Frappe Next JS"
app_publisher = "Your Name"
app_description = "A Frappe App to setup and manage Next.js frontends on your custom Frappe App."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your@email.com"
app_license = "MIT"

# CLI Commands
# ------------

app_commands = [
    "frappe_next_js.commands"
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_next_js/css/frappe_next_js.css"
# app_include_js = "/assets/frappe_next_js/js/frappe_next_js.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_next_js/css/frappe_next_js.css"
# web_include_js = "/assets/frappe_next_js/js/frappe_next_js.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_next_js/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

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

# Website route rules will be added dynamically when add-nextjs is run
website_route_rules = []

page_renderer = ["frappe_next_js.spa_page.SPAPage"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "frappe_next_js.utils.jinja_methods",
# 	"filters": "frappe_next_js.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "frappe_next_js.install.before_install"
# after_install = "frappe_next_js.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_next_js.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_next_js.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_next_js.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_next_js.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_next_js.tasks.weekly"
# 	],
# 	"monthly": [
# 		"frappe_next_js.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "frappe_next_js.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_next_js.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "frappe_next_js.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
