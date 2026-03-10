import json
import os
from datetime import datetime

LOG_FILE = "audit_log.json"

def log_event(original_text, sanitized_text, entities_found):
    """
    Logs security events to a local file.
    This file is the 'product' you show to CISOs.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "risk_types": entities_found,
        "action_taken": "SANITIZED",
        "original_snippet": original_text[:50] + "...", # Truncate for readability
        "sanitized_snippet": sanitized_text[:50] + "..."
    }
    
    try:
        # Load existing logs
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = []
        
        # Append new log
        data.append(entry)
        
        # Save
        with open(LOG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        print(f"Logging failed: {e}")