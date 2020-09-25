import frappe
import sentry_sdk
from sentry_sdk.integrations.rq import RqIntegration

def init_sentry():
	sentry_dsn = get_sentry_dsn()
	if not sentry_dsn:
		return

	if sentry_enabled():
		sentry_sdk.init(sentry_dsn, integrations=[RqIntegration()])

def capture_exception():
	init_sentry()
	with sentry_sdk.configure_scope() as scope:
		scope.user = {"email": frappe.session.user}
		scope.set_tag("site", frappe.local.site)
	sentry_sdk.capture_exception()

@frappe.whitelist(allow_guest=True)
def get_sentry_dsn():
	if sentry_enabled():
		return frappe.conf.get("sentry_dsn")

def sentry_enabled():
	enabled = True
	if frappe.conf.get("developer_mode"):
		# You can set this in site_config.json to enable sentry in developer mode
		# ... enable_sentry_developer_mode: 1 ...
		enabled = frappe.conf.get("enable_sentry_developer_mode", False)
	
	return enabled
