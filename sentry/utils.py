import gzip
import io
import json
from datetime import datetime, timedelta

import requests
import sentry_sdk
from sentry_sdk import Transport, capture_exception, configure_scope
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration
from sentry_sdk.utils import capture_internal_exceptions, logger

import frappe


class HttpTransport(Transport):
	"""Custom HTTP transport for Frappe-Sentry integration."""

	def __init__(self, options):
		from sentry_sdk.consts import VERSION

		Transport.__init__(self, options)
		assert self.parsed_dsn is not None
		self._auth = self.parsed_dsn.to_auth("sentry.python/%s" % VERSION)
		self._disabled_until = None
		self.options = options

		from sentry_sdk import Hub

		self.hub_cls = Hub

	def _send_event(self, event):
		if self._disabled_until is not None:
			if datetime.utcnow() < self._disabled_until:
				return
			self._disabled_until = None

		body = io.BytesIO()
		with gzip.GzipFile(fileobj=body, mode="w") as f:
			f.write(json.dumps(event, allow_nan=False).encode("utf-8"))

		assert self.parsed_dsn is not None
		logger.debug(
			"Sending event, type:%s level:%s event_id:%s project:%s host:%s"
			% (
				event.get("type") or "null",
				event.get("level") or "null",
				event.get("event_id") or "null",
				self.parsed_dsn.project_id,
				self.parsed_dsn.host,
			)
		)
		response = requests.post(
			str(self._auth.store_api_url),
			data=body.getvalue(),
			headers={
				"User-Agent": str(self._auth.client),
				"X-Sentry-Auth": str(self._auth.to_header()),
				"Content-Type": "application/json",
				"Content-Encoding": "gzip",
			},
		)

		try:
			if response.status_code == 429:
				self._disabled_until = datetime.utcnow() + timedelta(seconds=60)
				return
			elif response.status_code >= 300 or response.status_code < 200:
				logger.error(
					"Unexpected status code: %s (body: %s)",
					response.status_code,
					response.text,
				)
		finally:
			response.close()

		self._disabled_until = None

	def capture_event(self, event):
		hub = self.hub_cls.current

		with hub:
			with capture_internal_exceptions():
				self._send_event(event)


def handle():
	sentry_dsn = frappe.db.get_single_value("Sentry Settings", "sentry_dsn")

	if not sentry_dsn:
		sentry_dsn = frappe.conf.get("sentry_dsn")

	if not sentry_dsn:
		return

	sentry_sdk.init(
		dsn=sentry_dsn,
		transport=HttpTransport,
		integrations=[RedisIntegration(), RqIntegration()]
	)

	enabled = True
	if frappe.conf.get("developer_mode"):
		# You can set this in site_config.json
		# ... enable_sentry_developer_mode: 1 ...
		enabled = frappe.conf.get("enable_sentry_developer_mode", False)

	if enabled:
		with configure_scope() as scope:
			scope.user = {"email": frappe.session.user}
			scope.set_context("site", {
				'site': frappe.local.site
			})

			capture_exception()


@frappe.whitelist(allow_guest=True)
def get_sentry_dsn():
	return frappe.db.get_single_value("Sentry Settings", "sentry_dsn")
