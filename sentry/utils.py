import frappe
from raven import Client
from raven.transport.http import HTTPTransport
from raven.transport.threaded import ThreadedHTTPTransport

def handle(async=True):
    sentry_dsn = frappe.db.get_single_value("Sentry Settings", "sentry_dsn")

    if not sentry_dsn:
        return

    if async:
        transport = ThreadedHTTPTransport
    else:
        transport = HTTPTransport


    client = Client(sentry_dsn, transport=transport)
    enabled = True
    if frappe.conf.get("developer_mode"):
        # You can set this in site_config.json
        # ... enable_sentry_developer_mode: 1 ...
        enabled = frappe.conf.get("enable_sentry_developer_mode", False)

    if enabled:
        client.user_context({
            'email': frappe.session.user,
            'site' : frappe.local.site
        })
        client.captureException()

@frappe.whitelist(allow_guest=True)
def get_sentry_dsn():
    return frappe.db.get_single_value("Sentry Settings", "sentry_dsn")