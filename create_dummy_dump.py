import tarfile
import os
import io

def create_dummy_dump():
    # Create a dummy structure
    print("Creating dummy dump...")
    
    # 1. Kubelet log with error
    kubelet_log = "I0101 10:00:00.123456    1234 kubelet.go:123] ...\nE0101 10:05:00.123456    1234 kubelet.go:456] DiskPressure: node is low on disk space\n"
    
    # 2. Daemon log with error
    daemon_log = "level=error msg='Handler for GET /v1.40/containers/json returned error: context deadline exceeded'\n"
    
    # 3. Node directory
    # structure: nodes/worker-1/
    
    with tarfile.open("test_dump.tar.gz", "w:gz") as tar:
        # Add kubelet log
        t = tarfile.TarInfo(name="support-bundle/kubernetes/kubelet.log")
        t.size = len(kubelet_log)
        tar.addfile(t, io.BytesIO(kubelet_log.encode('utf-8')))
        
        # Add daemon log
        t = tarfile.TarInfo(name="support-bundle/daemon/docker/daemon.log")
        t.size = len(daemon_log)
        tar.addfile(t, io.BytesIO(daemon_log.encode('utf-8')))
        
        # Add node dir (just emulating existence)
        t = tarfile.TarInfo(name="nodes/worker-1/")
        t.type = tarfile.DIRTYPE
        tar.addfile(t)
        
    print("Created test_dump.tar.gz")

if __name__ == "__main__":
    create_dummy_dump()
