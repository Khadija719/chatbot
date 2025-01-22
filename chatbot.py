from flask import Flask, render_template, request, jsonify
import aiml
import os

app = Flask(__name__)

# Initialize the AIML kernel
kernel = aiml.Kernel()


# Load the AIML file
kernel.learn("know.aiml")

# Construct the path to the AIML files directory
aiml_directory = os.path.join(os.path.dirname(__file__), 'aiml_files')

# Check if the directory exists and load AIML files
if os.path.exists(aiml_directory):
    # Iterate over each file in the directory
    for file in os.listdir(aiml_directory):
        if file.endswith(".aiml"):
            try:
                kernel.learn(os.path.join(aiml_directory, file))
            except Exception as e:
                print(f"Error loading AIML file {file}: {e}")
else:
    print(f"Directory not found: {aiml_directory}")

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chatbot requests
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        bot_response = kernel.respond(user_message)
        return jsonify(response=bot_response)
    else:
        return jsonify(response="I didn't understand that. Could you please rephrase?")

if __name__ == '__main__':
    app.run(debug=True)
