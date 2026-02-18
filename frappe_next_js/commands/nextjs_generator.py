import click
import subprocess
import json

from pathlib import Path
from .boilerplates import *  # noqa: F403
from .utils import (
    create_file,
    add_commands_to_root_package_json,
    add_routing_rule_to_hooks,
    add_api_module,
    get_app_package_name,
)


class NextJSGenerator:
    def __init__(self, spa_name: str, app: str, typescript: bool, tailwindcss: bool, site_name: str = "localhost"):
        """Initialize a new NextJSGenerator instance."""
        self.spa_name = spa_name
        self.app = app
        self.app_path = Path("../apps") / app
        self.spa_path: Path = self.app_path / self.spa_name
        self.use_typescript = typescript
        self.add_tailwindcss = tailwindcss
        self.site_name = site_name
        self.webserver_port = self._get_webserver_port()
        
        self.validate_spa_name()

    def _get_webserver_port(self) -> str:
        """Read webserver_port from common_site_config.json, default to 8000."""
        config_path = Path("../sites/common_site_config.json")
        try:
            with config_path.open("r") as f:
                config = json.load(f)
            return str(config.get("webserver_port", 8000))
        except (FileNotFoundError, json.JSONDecodeError):
            return "8000"

    def validate_spa_name(self):
        """Validate that the SPA name is not the same as the app name."""
        if self.spa_name == self.app:
            click.echo("Frontend name must not be same as app name", err=True)
            exit(1)
        
        if self.spa_path.exists():
            click.echo(f"Directory {self.spa_name} already exists in {self.app}", err=True)
            exit(1)

    def generate_nextjs(self):
        """Generate the Next.js project."""
        click.echo(f"Generating Next.js frontend '{self.spa_name}' for app '{self.app}'...")
        
        # Create the project directory
        self.spa_path.mkdir(parents=True, exist_ok=True)
        
        # Create project structure
        self.create_package_json()
        self.create_next_config()
        self.create_src_structure()
        self.create_env_file()
        self.create_config_files()
        
        if self.add_tailwindcss:
            self.setup_tailwindcss()
        
        # Create app root package.json (like CRM pattern)
        self.create_app_package_json()
        
        # Update app .gitignore
        self.update_app_gitignore()
        
        # Install dependencies
        self.install_dependencies()
        
        # Add commands to root package.json
        add_commands_to_root_package_json(self.app, self.spa_name)
        
        # Add routing rule to hooks.py
        add_routing_rule_to_hooks(self.app, self.spa_name)
        # Create api.py with guest-accessible methods
        add_api_module(self.app)
        
        # Create www directory for production builds
        self.create_www_directory()
        
        click.echo("\n" + "="*60)
        click.echo("✅ Next.js frontend created successfully!")
        click.echo("="*60)
        click.echo(f"\nTo start the development server:")
        click.echo(f"  cd apps/{self.app}/{self.spa_name} && npm run dev")
        click.echo(f"\nOr from bench directory:")
        click.echo(f"  npm run dev:{self.spa_name}")
        click.echo(f"\nVisit: http://localhost:3000")
        click.echo("="*60 + "\n")

    def create_app_package_json(self):
        """Create root package.json for the app (CRM-style delegation to spa directory)."""
        app_package_json = self.app_path / "package.json"
        if not app_package_json.exists():
            content = self._render_template(NEXTJS_APP_PACKAGE_JSON)
            create_file(app_package_json, content)

    def update_app_gitignore(self):
        """Add node_modules and frontend output to the app's .gitignore."""
        gitignore_path = self.app_path / ".gitignore"
        if not gitignore_path.exists():
            return

        content = gitignore_path.read_text()
        entries_to_add = []

        app_package = get_app_package_name(self.app)
        www_path = f"{app_package}/www/{self.spa_name}"
        if "node_modules" not in content:
            entries_to_add.append("node_modules")
        if www_path not in content:
            entries_to_add.append(www_path)

        if entries_to_add:
            if not content.endswith("\n"):
                content += "\n"
            content += "\n".join(entries_to_add) + "\n"
            gitignore_path.write_text(content)

    def create_package_json(self):
        """Create package.json for the Next.js project."""
        template = NEXTJS_PACKAGE_JSON if self.use_typescript else NEXTJS_PACKAGE_JSON_JS
        content = self._render_template(template)
        create_file(self.spa_path / "package.json", content)

    def create_next_config(self):
        """Create next.config.js."""
        content = self._render_template(NEXTJS_CONFIG)
        create_file(self.spa_path / "next.config.js", content)

    def create_src_structure(self):
        """Create the src directory structure with app router."""
        src_app_path = self.spa_path / "src" / "app"
        src_lib_path = self.spa_path / "src" / "lib"
        src_components_ui_path = self.spa_path / "src" / "components" / "ui"
        src_hooks_path = self.spa_path / "src" / "hooks"
        
        # Create directories
        src_app_path.mkdir(parents=True, exist_ok=True)
        src_lib_path.mkdir(parents=True, exist_ok=True)
        src_components_ui_path.mkdir(parents=True, exist_ok=True)
        src_hooks_path.mkdir(parents=True, exist_ok=True)
        
        # Create layout file
        if self.use_typescript:
            layout_content = self._render_template(NEXTJS_LAYOUT_TSX)
            create_file(src_app_path / "layout.tsx", layout_content)
        else:
            layout_content = self._render_template(NEXTJS_LAYOUT_JS)
            create_file(src_app_path / "layout.js", layout_content)
        
        # Create page file
        if self.use_typescript:
            page_content = self._render_template(NEXTJS_PAGE_TSX)
            create_file(src_app_path / "page.tsx", page_content)
        else:
            page_content = self._render_template(NEXTJS_PAGE_JS)
            create_file(src_app_path / "page.js", page_content)
        
        # Create login page
        login_path = src_app_path / "login"
        login_path.mkdir(parents=True, exist_ok=True)
        if self.use_typescript:
            login_content = self._render_template(NEXTJS_LOGIN_PAGE_TSX)
            create_file(login_path / "page.tsx", login_content)
        else:
            login_content = self._render_template(NEXTJS_LOGIN_PAGE_JS)
            create_file(login_path / "page.js", login_content)
        
        # Create globals.css
        create_file(src_app_path / "globals.css", NEXTJS_GLOBALS_CSS)
        
        # Create Frappe lib with createResource pattern
        if self.use_typescript:
            frappe_content = self._render_template(NEXTJS_FRAPPE_LIB_TSX)
            create_file(src_lib_path / "frappe.tsx", frappe_content)
        else:
            frappe_content = self._render_template(NEXTJS_FRAPPE_LIB_JS)
            create_file(src_lib_path / "frappe.js", frappe_content)
        
        # Create shadcn utils (cn function)
        create_file(src_lib_path / "utils.ts", SHADCN_UTILS)
        
        # Create shadcn UI components
        self.create_shadcn_components(src_components_ui_path, src_hooks_path)

    def create_env_file(self):
        """Create .env.local file."""
        content = self._render_template(NEXTJS_ENV_LOCAL)
        create_file(self.spa_path / ".env.local", content)

    def create_config_files(self):
        """Create configuration files."""
        # Create .gitignore
        create_file(self.spa_path / ".gitignore", NEXTJS_GITIGNORE)
        
        # Create .eslintrc.json
        create_file(self.spa_path / ".eslintrc.json", NEXTJS_ESLINTRC)
        
        if self.use_typescript:
            # Create tsconfig.json
            create_file(self.spa_path / "tsconfig.json", NEXTJS_TSCONFIG)
            # Create next-env.d.ts
            create_file(self.spa_path / "next-env.d.ts", NEXTJS_ENV_DTS)
        else:
            # Create jsconfig.json
            create_file(self.spa_path / "jsconfig.json", NEXTJS_JSCONFIG)

    def setup_tailwindcss(self):
        """Set up TailwindCSS."""
        click.echo("Setting up TailwindCSS...")
        
        # Add tailwind dependencies to package.json
        package_json_path = self.spa_path / "package.json"
        with package_json_path.open("r") as f:
            package = json.load(f)
        
        package["devDependencies"]["tailwindcss"] = "^3.4.0"
        package["devDependencies"]["postcss"] = "^8.4.0"
        package["devDependencies"]["autoprefixer"] = "^10.4.0"
        
        with package_json_path.open("w") as f:
            json.dump(package, f, indent=2)
        
        # Create tailwind.config.js
        create_file(self.spa_path / "tailwind.config.js", NEXTJS_TAILWIND_CONFIG)
        
        # Create postcss.config.js
        create_file(self.spa_path / "postcss.config.js", NEXTJS_POSTCSS_CONFIG)

    def install_dependencies(self):
        """Install npm dependencies."""
        click.echo("Installing dependencies...")
        try:
            subprocess.run(
                ["npm", "install"],
                cwd=self.spa_path,
                check=True
            )
            click.echo("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            click.echo(f"Warning: Failed to install dependencies: {e}", err=True)
            click.echo("You can install them manually by running: npm install")

    def create_www_directory(self):
        """Create www directory for the SPA route handler."""
        www_path = self.app_path / get_app_package_name(self.app) / "www" / self.spa_name
        www_path.mkdir(parents=True, exist_ok=True)
        
        # Create index.html that will be served
        index_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{self.spa_name}</title>
</head>
<body>
    <div id="root">Loading...</div>
    <script>
        // This page is served when accessing /{self.spa_name}
        // In development, run 'npm run dev' in the {self.spa_name} directory
        // In production, run 'npm run build' to generate static files
    </script>
</body>
</html>
"""
        create_file(www_path / "index.html", index_html)

    def create_shadcn_components(self, components_ui_path: Path, hooks_path: Path):
        """Create shadcn/ui components."""
        # Button component
        create_file(components_ui_path / "button.tsx", SHADCN_BUTTON)
        
        # Card component
        create_file(components_ui_path / "card.tsx", SHADCN_CARD)
        
        # Input component
        create_file(components_ui_path / "input.tsx", SHADCN_INPUT)
        
        # Toast component
        create_file(components_ui_path / "toast.tsx", SHADCN_TOAST)
        
        # Toaster component
        create_file(components_ui_path / "toaster.tsx", SHADCN_TOASTER)
        
        # use-toast hook
        create_file(hooks_path / "use-toast.ts", SHADCN_USE_TOAST)
        
        # components.json for shadcn CLI
        create_file(self.spa_path / "components.json", SHADCN_COMPONENTS_JSON)

    def _render_template(self, template: str) -> str:
        """Render a template with context variables."""
        context = {
            "spa_name": self.spa_name,
            "app_name": self.app,
            "app_package": get_app_package_name(self.app),
            "app_title": self.app.replace("_", " ").replace("-", " ").title(),
            "site_name": self.site_name,
            "webserver_port": self.webserver_port,
        }
        
        result = template
        for key, value in context.items():
            result = result.replace("{{ " + key + " }}", value)
        
        return result
