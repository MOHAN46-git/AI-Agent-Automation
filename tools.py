"""Deterministic tool interfaces for the autonomous agent."""

import math
import os
from typing import Dict

def calculate_expression(expression: str) -> str:
    """Safely evaluates basic mathematical expressions using Python.
    
    Args:
        expression: The mathematical string expression (e.g. '42 * 61', 'sqrt(144)').
    """
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names.update({"abs": abs, "round": round})
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Calculation Error: {str(e)}"

def read_system_metric(metric_name: str) -> str:
    """Reads simulated system telemetry or host metadata.
    
    Args:
        metric_name: The metric identifier, e.g. 'cpu_load', 'memory_usage', 'disk_free'.
    """
    mock_metrics: Dict[str, str] = {
        "cpu_load": "42%",
        "memory_usage": "61%",
        "disk_free": "184 GB",
        "active_threads": "148"
    }
    return mock_metrics.get(metric_name.lower().strip(), f"Error: Metric '{metric_name}' not found.")

def write_local_log(filename: str, content: str) -> str:
    """Writes an incident or analysis report to the local agent workspace.
    
    Args:
        filename: Name of the log file (e.g. 'telemetry_audit.log').
        content: The text payload to append to the file.
    """
    os.makedirs("agent_workspace", exist_ok=True)
    safe_path = os.path.join("agent_workspace", os.path.basename(filename))
    try:
        with open(safe_path, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Successfully wrote {len(content)} characters to {safe_path}"
    except Exception as e:
        return f"Filesystem Error: {str(e)}"

AGENT_TOOLS = [calculate_expression, read_system_metric, write_local_log]
