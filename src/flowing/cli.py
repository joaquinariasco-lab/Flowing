import click
import subprocess
import time
import os
import sys
import webbrowser

@click.group()
def main():
    """Flowing: The Zero-Friction Debugger for AI Agents."""
    pass

@main.command()
def dashboard():
    """Launch the Real-Time Observability Dashboard."""
    click.echo("🚀 Launching Flowing Dashboard...")
    # Adjust path to where your streamlit app lives
    subprocess.Popen(["streamlit", "run", "src/flowing/observability/dashboard.py"])

@main.command()
def demo():
    """WOW EFFECT: Start a full debugging ecosystem instantly."""
    click.secho("🌊 Initializing Flowing Debugger Ecosystem...", fg='cyan', bold=True)
    
    # 1. Start the Dashboard (The Niche)
    click.echo("📊 Starting Observability UI...")
    subprocess.Popen(["streamlit", "run", "src/flowing/observability/dashboard.py"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Give Streamlit a moment to start
    time.sleep(3)
    webbrowser.open("http://localhost:8501")
    
    # 2. Start two Worker Agents on different ports
    for i in range(2):
        port = 5000 + i
        name = f"Agent_{chr(65+i)}" # Agent_A, Agent_B
        click.echo(f"🤖 Spinning up {name} on port {port}...")
        subprocess.Popen([sys.executable, "-m", "flowing.agents.server", 
                         "--name", name, "--port", str(port)],
                         stdout=subprocess.DEVNULL)
    
    time.sleep(2)
    
    # 3. Run a sample Trace to show data immediately
    click.secho("📝 Generating initial trace data...", fg='yellow')
    # This runs one of your example scripts to populate the dashboard
    subprocess.run([sys.executable, "examples/simple_workflow.py"])
    
    click.secho("\n✅ SYSTEM LIVE!", fg='green', bold=True)
    click.echo("Check your browser at http://localhost:8501 to see the live traces.")
    click.echo("Press Ctrl+C to stop the demo.")
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\n🛑 Shutting down...")
