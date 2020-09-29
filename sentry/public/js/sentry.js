import { init, configureScope } from '@sentry/browser';

if (frappe.boot.sentry_dsn && !frappe.boot.developer_mode) {
	init({ dsn: frappe.boot.sentry_dsn });
	configureScope(function (scope) {
		scope.setUser({ email: frappe.boot.user.email });
	});
}