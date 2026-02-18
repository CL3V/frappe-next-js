"""Page renderer for Next.js SPA - serves static files without Jinja processing."""

import mimetypes
import os

from werkzeug.wrappers import Response

import frappe


class SPAPage:
	"""Serves Next.js SPA from www/{spa_name}/ - index.html and static assets."""

	def __init__(self, path, http_status_code=None):
		self.path = path
		self.http_status_code = http_status_code

	def _get_spa_root(self):
		"""Extract the SPA root directory name from the path."""
		return self.path.split("/")[0] if self.path else ""

	def can_render(self):
		if not self.path:
			return False

		spa_root = self._get_spa_root()
		request_path = (frappe.local.request.path or "").strip("/")
		if not request_path.startswith(spa_root):
			return False

		for app in frappe.get_installed_apps():
			index_path = frappe.get_app_path(app, "www", spa_root, "index.html")
			if os.path.isfile(index_path):
				return True
		return False

	def _find_file(self, request_path):
		"""Find the file to serve for the given request path."""
		for app in frappe.get_installed_apps():
			www_base = frappe.get_app_path(app, "www")
			file_path = os.path.normpath(os.path.join(www_base, *request_path.split("/")))
			if not file_path.startswith(www_base) or file_path.endswith(".py"):
				continue
			# Exact file match (CSS, JS, fonts, images)
			if os.path.isfile(file_path):
				return file_path
			# Directory with index.html (e.g. /frontend/login → /frontend/login/index.html)
			index_in_dir = os.path.join(file_path, "index.html")
			if os.path.isfile(index_in_dir):
				return index_in_dir
		return None

	def render(self):
		request_path = (frappe.local.request.path or "").strip("/")
		spa_root = self._get_spa_root()

		if not request_path or request_path == spa_root or request_path.rstrip("/") == spa_root:
			request_path = f"{spa_root}/index.html"

		# Try to serve the exact file or directory index
		file_path = self._find_file(request_path)
		if file_path:
			with open(file_path, "rb") as f:
				data = f.read()
			mimetype = mimetypes.guess_type(file_path)[0] or "text/html"
			return Response(data, mimetype=mimetype)

		# Fallback to root index.html for unmatched SPA routes
		for app in frappe.get_installed_apps():
			index_path = frappe.get_app_path(app, "www", spa_root, "index.html")
			if os.path.isfile(index_path):
				with open(index_path, "rb") as f:
					return Response(f.read(), mimetype="text/html")
		return Response("Not Found", status=404)
