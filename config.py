import schedule
import time
import subprocess
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('covid_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_PATH = "python"  # or "python3" depending on your system

# Pipeline files
ORCHESTRATOR_SCRIPT = os.path.join(WORKSPACE_DIR, "orchestrator.py")
DASHBOARD_SCRIPT = os.path.join(WORKSPACE_DIR, "dashboard.py")

def run_orchestrator():
    """Run the data pipeline orchestrator"""
    try:
        logger.info("Starting orchestrator...")
        result = subprocess.run(
            [PYTHON_PATH, ORCHESTRATOR_SCRIPT],
            capture_output=True,
            text=True,
            cwd=WORKSPACE_DIR
        )
        if result.returncode == 0:
            logger.info("Orchestrator completed successfully")
        else:
            logger.error(f"Orchestrator failed with error: {result.stderr}")
    except Exception as e:
        logger.error(f"Error running orchestrator: {e}")

def run_dashboard():
    """Run the dashboard"""
    try:
        logger.info("Starting dashboard...")
        # Run dashboard in a separate process
        process = subprocess.Popen(
            [PYTHON_PATH, DASHBOARD_SCRIPT],
            cwd=WORKSPACE_DIR
        )
        logger.info(f"Dashboard started with PID: {process.pid}")
        return process
    except Exception as e:
        logger.error(f"Error starting dashboard: {e}")
        return None

def stop_dashboard(dashboard_process):
    """Stop the dashboard process"""
    if dashboard_process and dashboard_process.poll() is None:
        try:
            dashboard_process.terminate()
            dashboard_process.wait(timeout=5)
            logger.info("Dashboard stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping dashboard: {e}")
            dashboard_process.kill()

def weekly_update():
    """Perform weekly update of data and dashboard"""
    logger.info("Starting weekly update...")
    
    # Stop existing dashboard if running
    global dashboard_process
    if 'dashboard_process' in globals() and dashboard_process:
        stop_dashboard(dashboard_process)
    
    # Run orchestrator to update data
    run_orchestrator()
    
    # Start dashboard with new data
    dashboard_process = run_dashboard()
    
    logger.info("Weekly update completed")

# Schedule the weekly update for every Monday at 00:00
schedule.every().monday.at("00:00").do(weekly_update)

if __name__ == "__main__":
    logger.info("Starting COVID-19 pipeline scheduler...")
    
    # Run initial update
    weekly_update()
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check schedule every minute
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        if 'dashboard_process' in globals() and dashboard_process:
            stop_dashboard(dashboard_process)
        logger.info("Shutdown complete")