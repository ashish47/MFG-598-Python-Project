from flask import Flask, render_template, request, jsonify
import os, json, glob

app = Flask(__name__)
CWD = os.getcwd()
UPLOAD_FOLDER = os.path.join(CWD, 'uploadStore')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/listNames', methods=['GET'])
def list_files():
    try:
        # List all files in the directory
        files = [f.replace('.json','') for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        return jsonify(files)
    except Exception as e:
        # Handle exceptions, like if the directory does not exist
        return jsonify({"error": str(e)}), 500

@app.route('/getJson/<name>', methods=['GET'])
def get_json(name):
    file_path = os.path.join(UPLOAD_FOLDER, f"{name}.json")
    with open(file_path, 'r') as file:
        data = json.load(file)
        return jsonify(data)

@app.route('/', methods=['GET'])
def get_json_files():
    
    # list all files in UPLOAD_FOLDER
    if not os.path.exists(UPLOAD_FOLDER):
    # Create the directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER)
    files = [f.replace('.json','') for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    # Render a template and pass the variables to it
    return render_template('template.html', file_names=files)
    

@app.route('/resume/<fileName>', methods=['GET'])
def get_resume(fileName):

    file_path = os.path.join(UPLOAD_FOLDER, f"{fileName}.json")
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Render a template and pass the variables to it
    return render_template('resume.html', profile_data=data)

@app.route('/upload-json', methods=['POST'])
def upload_json():
    # Check if there is a file in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        # Define the full file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Save the file
        file.save(file_path)

        return jsonify({"message": "JSON file saved successfully"}), 200

@app.route('/deleteFile/<filename>', methods=['POST'])
def delete_file(filename):
    # Build the full file path
    file_path = os.path.join(UPLOAD_FOLDER, filename + '.json')

    # Check if file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        return jsonify({'message': f'{filename} deleted successfully'}), 200
    else:
        # File not found
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
