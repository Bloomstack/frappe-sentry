import frappe
from utils import get_sentry_data, get_release

def boot_session(bootinfo):
    sentry = get_sentry_data()
    bootinfo.sentry_dsn = sentry.sentry_dsn
    bootinfo.sentry_release = get_release(sentry)
    bootinfo.sentry_environment = sentry.environment