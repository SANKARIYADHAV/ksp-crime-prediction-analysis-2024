from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CrimeBot Chat</title>
    </head>
    <body>
        <h1>CrimeBot Chat</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv">
            <button type="submit">Upload</button>
        </form>
        <hr>
        <h2>Chat with CrimeBot</h2>
        <form action="/chat" method="post">
            <input type="text" name="user_input" placeholder="Enter your message">
            <button type="submit">Send</button>
        </form>
        <div id="chatbox">
            {% if response %}
            <p><strong>CrimeBot:</strong> {{ response }}</p>
            {% endif %}
        </div>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', message='No selected file')
    
    if file:
        # Read the uploaded dataset
        df = pd.read_csv(file)

        # Convert the CSV data to a list of conversations
        conversation_data = []
        for index, row in df.iterrows():
            conversation_data.append(row['Question'])
            conversation_data.append(row['Answer'])

        # Initialize chatbot
        chatbot = ChatBot('CrimeBot')
        trainer = ListTrainer(chatbot)
        
        # Train the chatbot on the uploaded dataset
        trainer.train(conversation_data)

        return render_template('index.html', message='Chatbot trained successfully!')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    # Initialize chatbot
    chatbot = ChatBot('CrimeBot')

    # Get response from the chatbot
    response = chatbot.get_response(user_input)

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
