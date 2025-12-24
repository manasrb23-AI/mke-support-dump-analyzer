import requests
import sys

def verify_zip_upload():
    # Correct port is 8080 as per previous user request
    url = "http://127.0.0.1:8080/upload"
    files = {'file': open('test_dump.zip', 'rb')}
    
    try:
        print("Sending upload request...")
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            if "Node Disk Pressure" in response.text:
                print("SUCCESS: Found expected 'Node Disk Pressure' issue in report validation.")
            else:
                print("FAILURE: Did not find expected issue in report.")
                print("Response excerpt:", response.text[:500])
        else:
            print("FAILURE: Request failed.")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_zip_upload()
