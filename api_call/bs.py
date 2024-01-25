from flask import jsonify
import os
import requests
external_api_url = "https://bs.ikamegroup.com/api/v1"


def update_status_and_progress_youtube(id, data):
    try:
        url = f'{external_api_url}/youtube/{id}'
        response = requests.patch(url, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        data = response.json()
        return jsonify(data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

def create_link_for_history(body, file_path):
    try:
        url = f'{external_api_url}/history'
        response = requests.post(url, json=body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        data = response.json()
        if response.status_code == 201:
            # If the request was successful (status code 201), delete the file
            os.remove(file_path)
            print("File deleted successfully")
        return jsonify(data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500