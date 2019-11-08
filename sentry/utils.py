import sys

import sentry_sdk
from sentry_sdk import HttpTransport, capture_exception, configure_scope
from sentry_sdk.integrations.redis import RedisIntegration

import frappe


def handle(async=True):
	sentry_dsn = frappe.db.get_single_value("Sentry Settings", "sentry_dsn")

	if not sentry_dsn:
		return

	sentry_sdk.init(
		dsn=sentry_dsn,
		transport=HttpTransport,
		integrations=[RedisIntegration()]
	)

	enabled = True
	if frappe.conf.get("developer_mode"):
		# You can set this in site_config.json
		# ... enable_sentry_developer_mode: 1 ...
		enabled = frappe.conf.get("enable_sentry_developer_mode", False)

	if enabled:
		with configure_scope() as scope:
			scope.user = {"email": frappe.session.user}
			scope.set_context("site", {
				'site': frappe.local.site
			})

			if async:
				capture_exception()
			else:
				# TODO: capture exceptions from background jobs
				capture_exception(error=sys.exc_info())


@frappe.whitelist(allow_guest=True)
def get_sentry_dsn():
	return frappe.db.get_single_value("Sentry Settings", "sentry_dsn")
