import click
import subprocess
import time
import os
import sys

@click.group()
def main():
    """Flowing OS: The Interoperability Layer for AI Agents."""
    pass

@main.command()
def dashboard():
    """Launch the Real-Time Observability Dashboard."""
    click.echo("🚀 Launching Flowing Dashboard...")
    # This assumes your streamlit file is moved to the package
    subprocess.Popen(["streamlit", "run", "src/flowing/observability/dashboard.py"])

@main.command()
@click.option('--agents', default=3, help='Number of worker agents to start.')
def demo(agents):
    """WOW EFFECT: Start a full agentic ecosystem in seconds."""
    click.secho("🌊 Initializing Flowing Ecosystem...", fg='cyan', bold=True)
    
    # 1. Start the Dashboard first
    subprocess.Popen(["streamlit", "run", "src/flowing/observability/dashboard.py"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    # 2. Start the Worker Agents (using your GenericWorker logic)
    for i in range(agents):
        port = 5000 + i
        name = f"Worker_{i+1}"
        click.echo(f"🤖 Starting {name} on port {port}...")
        # Use sys.executable to ensure we use the same environment
        subprocess.Popen([sys.executable, "-m", "flowing.agents.server", 
                         "--name", name, "--port", str(port)],
                         stdout=subprocess.DEVNULL)
    
    time.sleep(1)
    
    # 3. Start the Autonomous Controller (The Economy)
    click.secho("💰 Activating Autonomous Economy Controller...", fg='green')
    # This runs your '04_autonomous_economy.py' logic
    subprocess.Popen([sys.executable, "examples/04_autonomous_economy.py"])

    click.secho("\n✅ System Running!", fg='cyan', bold=True)
    click.echo("View live traces and agent balances at: http://localhost:8501")
    click.echo("Press Ctrl+C to stop the ecosystem.")
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\n🛑 Shutting down ecosystem...")

if __name__ == "__main__":
    main()
