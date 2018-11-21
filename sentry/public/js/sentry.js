$(document).ready(function () {
    if (frappe.boot.sentry_dsn && !frappe.boot.developer_mode) {
        Sentry.init({
            "dsn": frappe.boot.sentry_dsn,
            "environment": frappe.boot.sentry_environment,
            "release": frappe.boot.sentry_release
        });

        Sentry.configureScope((scope) => {
            scope.setUser({ "username": frappe.session.user });
            scope.setTag("site", frappe.boot.sitename);
        });
    }
});