## Sentry

Sends errors and performance data to Sentry. Compatible with Frappe / ERPNext v12 and v13 (Use `master-v13` branch for v13)

## Features

- Sends front-end and backend errors to Sentry
- Performance monitoring (only front-end)
- Sends account email and site when error occurs
- If `frappe.log_error` is called without exception, it takes the message and title and passes that to Sentry

## Setup 

For Sentry to work with the python backend and background jobs some changes are required in Frappe.

You will need to add the below block of code in the `log_error` function in the `__init__.py` file (https://github.com/frappe/frappe/blob/version-13/frappe/__init__.py#L2012)

``` 
    try:
        from sentry.utils import capture_exception
        capture_exception(message, title)
    except:
        pass
```

Additionally you will have to add the below block of code in the `start_worker` function in the `background_jobs.py` file (https://github.com/frappe/frappe/blob/version-13/frappe/utils/background_jobs.py#L172)

```
    try:
        from sentry.utils import init_sentry
        init_sentry()
    except:
        pass
```

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
#### License

MIT