import zipfile
import os
import io

def create_dummy_zip_dump():
    # Create a dummy structure
    print("Creating dummy zip dump...")
    
    # 1. Kubelet log with error
    kubelet_log = "I0101 10:00:00.123456    1234 kubelet.go:123] ...\nE0101 10:05:00.123456    1234 kubelet.go:456] DiskPressure: node is low on disk space\n"
    
    # 2. Daemon log with error
    daemon_log = "level=error msg='Handler for GET /v1.40/containers/json returned error: context deadline exceeded'\n"
    
    with zipfile.ZipFile("test_dump.zip", "w") as zf:
        # Add kubelet log
        zf.writestr("support-bundle/kubernetes/kubelet.log", kubelet_log)
        
        # Add daemon log
        zf.writestr("support-bundle/daemon/docker/daemon.log", daemon_log)
        
        # Add node dir (just emulating existence)
        # Zip doesn't explicit dirs usually, but adding a file inside works'
        # zf.writestr("nodes/worker-1/.placeholder", "")
        
    print("Created test_dump.zip")

if __name__ == "__main__":
    create_dummy_zip_dump()
