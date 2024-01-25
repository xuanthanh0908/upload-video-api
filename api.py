from flask import Flask, request, jsonify
from utils.upload_video import get_authenticated_service, upload_video_handler
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'https://bs.ikamegroup.com'])
### PUBLIC PROPERTIES ###
CLIENT_SECRET_FILE = 'secrets/client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

@app.route('/upload-video', methods=['POST'])
def upload_video_api():
    try:
       # Get JSON data from the request body
        request_data = request.json
        product_id = request_data.get('product_id')
        channel_id_in_ytb = request_data.get('channel_id_in_ytb')
        channel_id = request_data.get('channel_id')
        folder_path = request_data.get('folder_path')
        created_by = request_data.get('created_by')
        id = request_data.get('id')

        if channel_id is None:
            return jsonify({
                'error' : 'missing channel_id'
            }), 404
        if channel_id_in_ytb is None:
            return jsonify({
                'error' : 'missing channel_id_in_ytb'
            }), 404
        if folder_path is None:
            return jsonify({
                'error' : 'missing folder_path'
            }), 404
        if created_by is None:
            return jsonify({
                'error' : 'missing created_by'
            }), 404
        if id is None:
            return jsonify({
                'error' : 'missing id'
            }), 404
        

        youtube = get_authenticated_service(CLIENT_SECRET_FILE, SCOPES, channel_id_in_ytb)
        upload_video_handler(youtube,folder_path, channel_id, created_by, id, product_id, channel_id_in_ytb)
        return jsonify({
                'message' : 'OK'
            }), 200
    
    except Exception as e: 
        return jsonify({
            'message' : 'Failed to upload video',
            'details' : e
        }), 501
    
if __name__ == "__main__":
    app.run(debug=True,port=8000)