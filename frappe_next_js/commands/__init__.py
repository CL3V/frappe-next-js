import click

from .nextjs_generator import NextJSGenerator


@click.command("add-nextjs")
@click.option("--name", default="frontend", prompt="Frontend Name", help="Name of the Next.js frontend directory")
@click.option("--app", prompt="App Name", help="Name of the Frappe app to add the frontend to")
@click.option("--typescript/--no-typescript", default=None, help="Configure the project with TypeScript")
@click.option("--tailwindcss/--no-tailwindcss", default=None, help="Configure the project with TailwindCSS")
@click.option(
    "--site",
    default="localhost",
    help="Site name for API proxying (default: localhost)",
)
def add_nextjs(name, app, typescript, tailwindcss, site):
    """Add a Next.js frontend to a Frappe app.
    
    This command scaffolds a new Next.js project with:
    - App Router (Next.js 14+)
    - frappe-js-sdk integration
    - TypeScript support (optional)
    - TailwindCSS support (optional)
    - API proxy configuration for Frappe backend
    
    Example:
        bench add-nextjs --app my_app --name frontend --typescript --tailwindcss
    """
    if not app:
        click.echo("Please provide an app with --app", err=True)
        return

    if typescript is None:
        typescript = click.confirm("Use TypeScript?", default=True)
    if tailwindcss is None:
        tailwindcss = click.confirm("Use TailwindCSS?", default=True)
    
    generator = NextJSGenerator(
        spa_name=name,
        app=app,
        typescript=typescript,
        tailwindcss=tailwindcss,
        site_name=site,
    )
    generator.generate_nextjs()


commands = [add_nextjs]
