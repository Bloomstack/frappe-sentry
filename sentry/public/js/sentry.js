if (frappe.boot.sentry_dsn && !frappe.boot.developer_mode)
{
    Raven.config(frappe.boot.sentry_dsn).install();

    Raven.setUserContext({
        email: frappe.boot.user.email,
    })
}