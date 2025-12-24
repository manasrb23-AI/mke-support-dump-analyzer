import os
import glob
import json
import re

async def parse_dump(base_path: str):
    """
    Traverses the extracted dump and collects data.
    """
    data = {
        "metadata": {
            "version": "Unknown",
            "node_count": 0,
            "manager_count": 0,
            "worker_count": 0,
            "os_info": "Unknown"
        },
        "nodes": [],
        "logs": {
            "kubelet": [],
            "docker": [],
            "syslog": []
        }
    }
    
    # Attempt to find UCP/MKE version
    # Usually in a file like 'ucp-version' or 'info.json' at root or under subdirs
    # This is a best-effort approach based on common structures
    
    # 1. Info / Metadata
    # Try looking for a cluster-info or similar
    # For now, we'll scan for specific patterns if standard files aren't found
    
    # 2. Node Discovery
    # Often found in 'nodes/' directory or 'dsinfo/nodes'
    # We will search for directories that look like nodes
    
    # Heuristic: verify if 'nodes' dir exists
    nodes_dir = os.path.join(base_path, "nodes")
    if os.path.exists(nodes_dir):
        for node_name in os.listdir(nodes_dir):
            node_path = os.path.join(nodes_dir, node_name)
            if os.path.isdir(node_path):
                node_role = "Worker" # Default
                # Check for role indicators in inspect files if available
                # e.g., docker inspect Output
                
                data["nodes"].append({
                    "name": node_name,
                    "role": node_role,
                    "status": "Unknown" # To be filled by parsing logs/inspects
                })
        data["metadata"]["node_count"] = len(data["nodes"])

    # 3. Log Aggregation
    # We won't read ALL logs into memory. We'll grep for errors.
    # But for the parser, let's just enable path discovery for the heuristics to use.
    
    return data

def find_files(base_path: str, pattern: str):
    return glob.glob(os.path.join(base_path, "**", pattern), recursive=True)
