if (frappe.boot.sentry_dsn && !frappe.boot.developer_mode) {
	Sentry.init({ "dsn": frappe.boot.sentry_dsn });
	Sentry.configureScope(function (scope) {
		scope.setUser({ "email": frappe.boot.user.email });
	});
}