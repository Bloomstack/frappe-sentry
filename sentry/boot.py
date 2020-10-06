import frappe
from .utils import get_sentry_dsn


def boot_session(bootinfo):
	bootinfo.sentry_dsn = get_sentry_dsn()
