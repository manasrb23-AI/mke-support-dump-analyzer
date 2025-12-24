## MKE Support Dump Analyzer Walkthrough
Built a web application to analyze Mirantis Kubernetes Engine (MKE) support dumps. The app allows you to upload a .tar.gz dump, parses the logs, and provides a root cause analysis report.

### Application Architecture
Backend: Python FastAPI
Handles file uploads (/upload)
Extracts compressed dumps safely
Parses logs (kubelet, docker, syslog)
Runs heuristics to detect common issues (Disk Pressure, OOM, etc.)
Frontend: HTML/CSS/JS (Vanilla)
Modern, glassmorphism-inspired UI
Drag-and-drop file upload
Interactive report dashboard
### Verification Results
I verified the application using a synthetic support dump (test_dump.tar.gz) containing known error patterns.

### Test Case: Disk Pressure Detection

Input: A dummy dump with a kubelet.log containing DiskPressure.

Expected Output: The analysis report should list "Node Disk Pressure" as a critical issue.

Result: SUCCESS. The verification script confirmed that the server processed the upload and returned the correct error analysis.
Screenshots

(Note: Since I am running in a headless environment, these are descriptions of the views)

Upload Page: A clean, dark-themed interface with a drag-and-drop zone.

Analysis Report: A dashboard showing cluster health score (reduced by errors), a list of critical issues, and node status.

### How to Run
Install Dependencies:
```sh 
pip install -r requirements.txt
```
Start the Server:
```sh
python -m uvicorn app.main:app --port 8080 --reload
```
or simply:
```sh
uvicorn app.main:app --port 8080
```
Access the App: Open http://127.0.0.1:8080 in your browser.

Analyze: Upload your support-bundle.tar.gz to see the results.
