frappe.ready(function () {
    if (!window.sentry_dsn) {
        frappe.call({
            method: "sentry.utils.get_sentry_dsn",
            callback: function (r) {
                window.localStorage.sentry_dsn = r.message
            }
        })
    }

    if (window.localStorage.sentry_dsn) {
        Raven.config(window.localStorage.sentry_dsn).install();


        if (frappe.sid != "Guest") {
            Raven.setUserContext({
                email: frappe.user_id,
            })
        }
    }
});