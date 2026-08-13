import typer

from email_agent.config import settings

app = typer.Typer()

@app.command()
def info():
    """Show current configurations"""
    typer.echo(f"Model: {settings.cerebras_model}")
    typer.echo(f"Base URL: {settings.cerebras_base_url}")
    typer.echo(f"API Key set: {bool(settings.cerebras_api_key)}")
    typer.echo(f"checkpointer: {settings.checkpointer}")

if __name__ == "__main__":
    app()