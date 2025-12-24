import os
import re

STATUS_READY = "Ready"
STATUS_NOT_READY = "NotReady"

COMMON_ERRORS = [
    {"pattern": r"DiskPressure", "title": "Node Disk Pressure", "desc": "One or more nodes are experiencing disk pressure.", "severity": "error"},
    {"pattern": r"MemoryPressure", "title": "Node Memory Pressure", "desc": "One or more nodes are low on memory.", "severity": "error"},
    {"pattern": r"NetworkPluginNotReady", "title": "CNI Plugin Issue", "desc": "The CNI plugin is not ready.", "severity": "error"},
    {"pattern": r"context deadline exceeded", "title": "Context Deadline Exceeded", "desc": "Timeouts occurring in cluster operations.", "severity": "warning"},
    {"pattern": r"OOMKilled", "title": "OOM Killed", "desc": "Processes are being killed due to Out Of Memory.", "severity": "error"},
    {"pattern": r"Calico is not ready", "title": "Calico Not Ready", "desc": "Calico networking component is failing.", "severity": "error"},
]

def analyze_bundle(base_path: str, parsed_data: dict):
    results = {
        "score": 100,
        "issues": [],
        "metadata": parsed_data["metadata"],
        "nodes": parsed_data["nodes"],
        "summary": "Analysis complete."
    }
    
    issues_found = []
    
    # 1. Log Scanning (Heuristic)
    # Scan known log files for error patterns
    # Limit scan to save time/memory - top 1MB of key files or similar?
    # For now, we iterate over a few key log types found by glob
    
    log_files_to_scan = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".log") or file == "daemon.log" or file == "syslog":
                 log_files_to_scan.append(os.path.join(root, file))
    
    # Limit number of files to scan for performance in this demo
    log_files_to_scan = log_files_to_scan[:50] 
    
    for log_file in log_files_to_scan:
        try:
             with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read() # Reading full file for basic demo (be careful with large files in prod)
                
                for error in COMMON_ERRORS:
                    if re.search(error["pattern"], content):
                        # Avoid duplicates
                        if not any(i['title'] == error['title'] for i in issues_found):
                            issues_found.append({
                                "title": error["title"],
                                "description": error["desc"],
                                "severity": error["severity"]
                            })
                            results["score"] -= 10
        except Exception:
            pass
            
    # 2. Node Status checks from parsed data
    # (Mock logic if parsed_data doesn't have deep status yet)
    for node in results["nodes"]:
        node["status"] = STATUS_READY # Defaulting to Ready for UI demo if check not failed
    
    if results["score"] < 0: results["score"] = 0
    
    if len(issues_found) == 0:
        results["summary"] = "Cluster appears healthy based on available logs."
    else:
        results["summary"] = f"Found {len(issues_found)} critical or warning issues."
        
    results["issues"] = issues_found
    return results
