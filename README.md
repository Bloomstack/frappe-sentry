## Sentry

Sends errors and performance data to Sentry. Compatible with Frappe / ERPNext v12 and v13 (Use `master-v13` branch for v13)

## Features

- Sends front-end and backend errors to Sentry
- Performance monitoring (only front-end)
- Sends account email and site when error occurs
- If `frappe.log_error` is called without exception, it takes the message and title and passes that to Sentry

## Setup 

For Sentry to work with the python backend no changes are needed in Frappe.
For frontend errors no changes are needed in Frappe. 

## Configuring Sentry

You need to get the Sentry DSN and add it to the `common_site_config.json` file.

```
{
    "sentry_dsn": "https://<key>:<secret>@sentry.io/<project_id>"
}
```

Adding it to the `site_config.json` file for a site will override the Sentry DSN in the `common_site_config.json` file.

By default Sentry will not log errors if `developer_mode` is set to True. For enabling Sentry in developer mode you must set the `enable_sentry_developer_mode` key as True in the `site_config.json` or `common_site_config.json` file.

Additional tags can be provided in `site_config.json`: `project`, `server_name` and `sentry_site`

#### License

MIT