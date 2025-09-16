from flask import Flask, request, jsonify
from hangman_ai import HangmanAI

# Initializing Flask App
app = Flask(__name__)

# Create a Single, Global Instance of the App. App loads corpus files at the start only once.
print("Starting the Flask server. Please wait while the Algo model loads.")
ai_model = HangmanAI()
print("Algo model loaded. Server is ready.")


# Definining API Endpoint
@app.route('/guess', methods=['POST'])
def handle_guess():
    """
    To Handle a request to make a hangman guess.
    It expects a JSON payload with 'currentWordState' and 'guessedLetters'.
    """
    # 1. Get data from incoming request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid request: No JSON payload received."}), 400

    current_word_state = data.get('currentWordState')
    guessed_letters = data.get('guessedLetters')
    
    # 2. Validate input
    if current_word_state is None or guessed_letters is None:
        return jsonify({"error": "Invalid request: Missing 'currentWordState' or 'guessedLetters'."}), 400

    # 3. Use the App to make a guess
    next_guess = ai_model.make_guess(current_word_state, guessed_letters)
    
    # 4. Format and return the response
    response = {
        "nextGuess": next_guess
    }
    
    return jsonify(response)


# Run the Flask App 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
