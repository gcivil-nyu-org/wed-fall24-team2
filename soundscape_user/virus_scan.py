import requests
import os

def scan_file_with_virustotal(file_data, api_key):
    #return True
    url = "https://www.virustotal.com/api/v3/files"
    headers = {
        "x-apikey": os.getenv("VIRUS_SCAN_API")
    }
    files = {
        "file": file_data
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        analysis_id = response.json()["data"]["id"]
        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        analysis_response = requests.get(analysis_url, headers=headers)
        if analysis_response.status_code == 200:
            analysis_result = analysis_response.json()
            if analysis_result["data"]["attributes"]["status"] == "completed":
                if analysis_result["data"]["attributes"]["stats"]["malicious"] > 0:
                    return True
                else:
                    return False
            else:
                print("Analysis not completed yet.")
                return False
        else:
            print("Failed to retrieve file analysis. Status code:", analysis_response.status_code)
            return False
    else:
        print("VirusTotal scan failed. Status code:", response.status_code)
        return False