import zipfile
import os
import io

def create_nested_zip_dump():
    # Create a dummy structure
    print("Creating nested zip dump...")
    
    # Structure:
    # mke-dump-123/nodes/worker-1/
    # mke-dump-123/kubernetes/kubelet.log
    
    root_folder = "mke-dump-123"
    
    kubelet_log = "E0101 10:05:00.123456    1234 kubelet.go:456] DiskPressure: node is low on disk space\n"
    
    with zipfile.ZipFile("test_nested_dump.zip", "w") as zf:
        # Add kubelet log inside root folder
        zf.writestr(f"{root_folder}/kubernetes/kubelet.log", kubelet_log)
        
        # Add node dir marker
        zf.writestr(f"{root_folder}/nodes/worker-1/.placeholder", "")
        
    print("Created test_nested_dump.zip")

if __name__ == "__main__":
    create_nested_zip_dump()
