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
    if not frappe.conf.get("developer_mode"):
        client.user_context({
            'email': frappe.session.user,
            'site' : frappe.local.site
        })
        client.captureException()