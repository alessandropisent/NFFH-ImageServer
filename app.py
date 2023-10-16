from flask import Flask, request, jsonify, send_file
import os
import base64

app = Flask(__name__)

# Define the directory where you'll store the uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/<role>/upload', methods=['POST'])
def upload_image(role):
    try:
        
        data = request.json  # Assuming JSON request with base64 data

        base64_image = data['base64_image']
        user = data['user']
        
        # Decode the base64 image data
        image_data = base64.b64decode(base64_image)
        
        # Create a unique filename for the image
        filename = f'image_{len(os.listdir(app.config["UPLOAD_FOLDER"])) + 1}.png'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the decoded image to the 'uploads' directory
        with open(filepath, 'wb') as image_file:
            image_file.write(image_data)
        
        # Construct the URL for the uploaded image
        image_url = f"/{UPLOAD_FOLDER}/{filename}"
        
        return jsonify({'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/images/<image_filename>', methods=['GET'])
def get_image(image_filename):
    # Construct the path to the image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    
    # Serve the image using send_file
    return send_file(image_path, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
