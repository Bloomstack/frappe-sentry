import frappe
from raven import Client


def handle():
    sentry_dsn = frappe.db.get_single_value("Sentry Settings", "sentry_dsn")

    if not sentry_dsn:
        return

    client = Client(sentry_dsn)
    if not frappe.conf.get("developer_mode"):
        client.user_context({
            'email': frappe.session.user,
            'site' : frappe.local.site
        })
        client.captureException()
