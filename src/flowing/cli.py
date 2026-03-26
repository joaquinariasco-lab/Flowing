import click
import subprocess
import time
import sys
import webbrowser
import signal
import socket
import os
from importlib.resources import files

# Global process registry
processes = []

# ----------------------------
# Utils
# ----------------------------

def start_process(cmd, silent=False, env=None):
    """Start a subprocess and track it."""
    if silent:
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
    else:
        p = subprocess.Popen(cmd, env=env)
    processes.append(p)
    return p


def shutdown(signum=None, frame=None):
    """Terminate all subprocesses cleanly."""
    click.echo("\n🛑 Shutting down Flowing...")
    for p in processes:
        try:
            p.terminate()
        except Exception:
            pass
    for p in processes:
        try:
            p.wait(timeout=5)
        except Exception:
            pass
    sys.exit(0)


def get_free_port():
    """Get an available port."""
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def wait_for_port(port, timeout=10):
    """Wait until a port is open."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)
    return False


def get_dashboard_path():
    """Resolve dashboard.py path inside installed package."""
    return files("flowing.observability").joinpath("dashboard.py")


def safe_open_browser(url: str):
    """
    Safely attempt to open a browser.
    Avoids gio / headless environment errors.
    """
    try:
        if os.environ.get("DISPLAY") or sys.platform in ("win32", "darwin"):
            webbrowser.open(url)
        else:
            click.echo(f"🌐 Dashboard available at: {url}")
    except Exception:
        click.echo(f"🌐 Dashboard available at: {url}")


# ----------------------------
# CLI
# ----------------------------

@click.group()
def main():
    """Flowing: The Control Plane for AI Agents."""
    pass


@main.command()
def dashboard():
    """Launch only the dashboard."""
    click.echo("🚀 Launching Flowing Dashboard...")

    dashboard_path = str(get_dashboard_path())
    port = get_free_port()

    # Env to disable Streamlit auto browser
    env = os.environ.copy()
    env["BROWSER"] = "none"

    start_process([
        sys.executable, "-m", "streamlit", "run",
        dashboard_path,
        "--server.port", str(port),
        "--server.headless", "true",
    ], env=env)

    if wait_for_port(port):
        url = f"http://localhost:{port}"
        safe_open_browser(url)
        click.echo(f"Dashboard running at {url}")
    else:
        click.echo("❌ Failed to start dashboard.")


@main.command()
def demo():
    """WOW EFFECT: Start a full AI system with observability."""
    
    # Register shutdown handlers
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    click.secho("🌊 Booting Flowing-OS...", fg='cyan', bold=True)

    # ----------------------------
    # 1. Start Dashboard
    # ----------------------------
    dashboard_path = str(get_dashboard_path())
    dashboard_port = get_free_port()

    click.echo("📊 Starting Observability UI...")

    env = os.environ.copy()
    env["BROWSER"] = "none"  # ✅ prevents gio errors

    start_process([
        sys.executable, "-m", "streamlit", "run",
        dashboard_path,
        "--server.port", str(dashboard_port),
        "--server.headless", "true",
    ], silent=True, env=env)

    if not wait_for_port(dashboard_port):
        click.echo("❌ Dashboard failed to start.")
        shutdown()

    dashboard_url = f"http://localhost:{dashboard_port}"
    safe_open_browser(dashboard_url)

    # ----------------------------
    # 2. Start Agents
    # ----------------------------
    click.echo("🤖 Spawning agent network...")

    agent_ports = []

    for i in range(2):
        port = get_free_port()
        agent_ports.append(port)

        name = f"Agent_{chr(65+i)}"

        click.echo(f"   • {name} running on port {port}")

        start_process([
            sys.executable, "-m", "flowing.agents.server",
            "--name", name,
            "--port", str(port)
        ], silent=True)

    # ----------------------------
    # 3. Generate Demo Activity
    # ----------------------------
    click.secho("📝 Generating live trace...", fg='yellow')

    try:
        subprocess.run(
            [sys.executable, "-m", "flowing.examples.simple_workflow"],
            check=False
        )
    except Exception:
        click.echo("⚠️ Could not run example workflow.")

    # ----------------------------
    # 4. Final UX
    # ----------------------------
    click.secho("\n✅ SYSTEM LIVE", fg='green', bold=True)
    click.echo(f"Dashboard: {dashboard_url}")
    click.echo("Agents: running")
    click.echo("\nPress Ctrl+C to stop")

    # Keep alive
    while True:
        time.sleep(1)
