import frappe
import sentry_sdk
from sentry_sdk import capture_exception
from sentry_sdk import configure_scope
from sentry_sdk import HttpTransport


def handle(async=True):
    sentry = get_sentry_data()
    if not sentry.sentry_dsn:
        return

    sentry_sdk.init(dsn=sentry.sentry_dsn,
                    environment=sentry.environment,
                    release=get_release(sentry),
                    debug=True)

    if not frappe.conf.get("developer_mode"):
        with configure_scope() as scope:
            scope.user = {
                "username": frappe.session.user
            }
            scope.set_tag("site", frappe.local.site)
        capture_exception()


@frappe.whitelist(allow_guest=True)
def get_sentry_dsn():
    return frappe.db.get_single_value("Sentry Settings", "sentry_dsn")


def get_sentry_data():
    return frappe.get_single("Sentry Settings")


def get_release(sentry_settings):
    app = frappe.local.module_app.get(sentry_settings.module.lower())
    return "{0}@{1}".format(app, frappe.get_attr(app + ".__version__"))
