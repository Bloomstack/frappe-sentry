import frappe


def boot_session(bootinfo):
	bootinfo.sentry_dsn = frappe.db.get_single_value("Sentry Settings", "sentry_dsn")
