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

    def can_render(self):
        if not self.path:
            return False
        request_path = (frappe.local.request.path or "").strip("/")
        if not request_path.startswith(self.path):
            return False
        for app in frappe.get_installed_apps():
            index_path = frappe.get_app_path(app, "www", self.path, "index.html")
            if os.path.isfile(index_path):
                return True
        return False

    def render(self):
        request_path = (frappe.local.request.path or "").strip("/")
        if not request_path or request_path == self.path or request_path.rstrip("/") == self.path:
            request_path = f"{self.path}/index.html"

        for app in frappe.get_installed_apps():
            www_base = frappe.get_app_path(app, "www")
            file_path = os.path.normpath(os.path.join(www_base, *request_path.split("/")))
            if file_path.startswith(www_base) and os.path.isfile(file_path) and not file_path.endswith(".py"):
                with open(file_path, "rb") as f:
                    data = f.read()
                mimetype = mimetypes.guess_type(file_path)[0] or "text/html"
                return Response(data, mimetype=mimetype)

        # Fallback to index.html for SPA client-side routing (e.g. /frontend/login)
        for app in frappe.get_installed_apps():
            index_path = frappe.get_app_path(app, "www", self.path, "index.html")
            if os.path.isfile(index_path):
                with open(index_path, "rb") as f:
                    return Response(f.read(), mimetype="text/html")
        return Response("Not Found", status=404)
