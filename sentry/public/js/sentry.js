import { init, configureScope } from '@sentry/browser';

if (frappe.boot.sentry_dsn) {
	init({ dsn: frappe.boot.sentry_dsn });
	configureScope(function (scope) {
		scope.setUser({ email: frappe.boot.user.email });
	});
}