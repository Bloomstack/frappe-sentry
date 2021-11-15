## Sentry

Logs errors to Sentry

## Installation Instructions

bench get-app https://github.com/Bloomstack/frappe-sentry
bench --site sitename install-app sentry
bench migrate
bench restart
bench clear-cache

To configure DSN search for sentry settings inside of the Frappe ui and insert your DSN Link and press save

#### License

MIT
