from flask import Flask, request, jsonify, render_template, session
import ollama
import base64
app = Flask(__name__)
app.secret_key = "dfswhiojiojcs"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Image is required.'}), 400    
    image_file = request.files['image']
    query = request.form['query']    
    try:
        image_string = base64.b64encode(image_file.read())
    
        res = ollama.chat( 
            model="llava:7b",
            messages=[
                {
                 'role':"system",
                 'content':"Be concise and only include the most important details."
                },
                {
                    'role': 'user',
                    'content': query,
                    'images': [image_string]
                }
            ],

            options={
                'num_ctx':100,
                'num_predict':100
            },
            stream=True
        )
        def gen():
         for chunk in res:
           description = chunk['message']['content']
           yield description
        return app.response_class(gen())        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/get_history', methods=['GET'])
def get_history():
    conversation_history = session.get('conversation_history', [])
    return jsonify({'conversation_history': conversation_history})
app.run(debug=True,port = 8080, host="0.0.0.0")
