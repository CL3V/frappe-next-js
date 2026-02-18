import json
import re
from pathlib import Path


def create_file(path: Path, content: str):
    """Create a file with the given content, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write(content)


def add_commands_to_root_package_json(app: str, spa_name: str):
    """Add dev commands to the root package.json of the bench."""
    root_package_json_path = Path("../package.json")
    
    if not root_package_json_path.exists():
        # Create a basic package.json if it doesn't exist
        root_package = {
            "name": "frappe-bench",
            "private": True,
            "scripts": {}
        }
    else:
        with root_package_json_path.open("r") as f:
            root_package = json.load(f)
    
    if "scripts" not in root_package:
        root_package["scripts"] = {}
    
    # Add dev and build commands for the Next.js app
    root_package["scripts"][f"dev:{spa_name}"] = f"cd apps/{app}/{spa_name} && npm run dev"
    root_package["scripts"][f"build:{spa_name}"] = f"cd apps/{app}/{spa_name} && npm run build"
    root_package["scripts"][f"build:{spa_name}:frappe"] = f"cd apps/{app}/{spa_name} && npm run build:frappe"
    
    with root_package_json_path.open("w") as f:
        json.dump(root_package, f, indent=2)


def add_routing_rule_to_hooks(app: str, spa_name: str):
    """Add website routing rule to the app's hooks.py."""
    hooks_path = Path("../apps") / app / app.replace("-", "_") / "hooks.py"
    
    if not hooks_path.exists():
        return
    
    hooks_content = hooks_path.read_text()
    
    # The routing rule to add
    new_rule = f'{{"from_route": "/{spa_name}/<path:app_path>", "to_route": "{spa_name}"}}'
    
    # Check if website_route_rules exists
    if "website_route_rules" in hooks_content:
        # Check if the rule already exists
        if spa_name in hooks_content:
            return
        
        # Find the website_route_rules list and add to it
        pattern = r'(website_route_rules\s*=\s*\[)'
        if re.search(pattern, hooks_content):
            hooks_content = re.sub(
                pattern,
                f'\\1\n\t{new_rule},',
                hooks_content
            )
    else:
        # Add website_route_rules at the end of the file
        hooks_content += f'\n\nwebsite_route_rules = [\n\t{new_rule},\n]\n'
    
    # Add override for get_logged_user (allow guest)
    app_package = get_app_package_name(app)
    if "override_whitelisted_methods" not in hooks_content and f"{app_package}.api.get_logged_user" not in hooks_content:
        hooks_content += f'\noverride_whitelisted_methods = {{\n\t"frappe.auth.get_logged_user": "{app_package}.api.get_logged_user",\n}}\n'

    hooks_path.write_text(hooks_content)


def add_api_module(app: str):
    """Create api.py with guest-accessible methods for SPA."""
    from .boilerplates import NEXTJS_API_PY
    app_package = get_app_package_name(app)
    api_path = Path("../apps") / app / app_package / "api.py"
    if not api_path.exists():
        create_file(api_path, NEXTJS_API_PY)


def get_app_package_name(app: str) -> str:
    """Convert app name to Python package name (replace - with _)."""
    return app.replace("-", "_")
