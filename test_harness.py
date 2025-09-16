import requests
import json
import time
import os

# The address of our running API server.
API_URL = "http://127.0.0.1:5000/guess"
TEST_WORDS_FILE = "words_to_test.txt"

def load_test_words(file_path):
    """
    Loads a list of words from an external text file.
    Skips empty lines and lines starting with '#'.
    """
    if not os.path.exists(file_path):
        print(f"Error: Test words file not found at '{file_path}'.")
        print("Please create this file and add words to it, one per line.")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [
                line.strip() for line in f 
                if line.strip() and not line.strip().startswith('#')
            ]
            return words
    except Exception as e:
        print(f"Error reading from {file_path}: {e}")
        return []

def play_game(secret_word):
    """
    Plays a single game of Hangman using the algo for a given secret word.
    """
    print(f"\n--- Starting new game. Word to guess: {secret_word} ---")
    
    secret_word_lower = secret_word.lower()
    guessed_letters = []
    incorrect_guesses = []
    guesses_remaining = 6
    
    word_state_list = []
    for char in secret_word_lower:
        if char == ' ':
            word_state_list.append('  ')
        else:
            word_state_list.append('_ ')
    current_word_state = "".join(word_state_list).strip()

    while guesses_remaining > 0:
        payload = {
            "currentWordState": current_word_state,
            "guessedLetters": guessed_letters,
            "guessesRemaining": guesses_remaining
        }
        
        try:
            response = requests.post(API_URL, json=payload, timeout=30)
            response.raise_for_status()
            ai_guess = response.json()['nextGuess']

            print(f"Current state: {current_word_state} | Guessed so far: {', '.join(sorted(guessed_letters)) or 'None'}")
            print(f"AI guesses: '{ai_guess}'")
            
            if ai_guess in guessed_letters:
                print(f"AI re-guessed '{ai_guess}'. Skipping.")
                continue
            
            guessed_letters.append(ai_guess)

            if ai_guess in secret_word_lower:
                print("Correct guess!")
                new_state_list = []
                for char in secret_word_lower:
                    if char in guessed_letters:
                        new_state_list.append(f"{char} ")
                    elif char == ' ':
                        new_state_list.append('  ')
                    else:
                        new_state_list.append('_ ')
                current_word_state = "".join(new_state_list).strip()
            else:
                print("Incorrect guess!")
                guesses_remaining -= 1
                incorrect_guesses.append(ai_guess)
                print(f"Incorrect guesses: {', '.join(incorrect_guesses)} | Lives remaining: {guesses_remaining}")

            if '_' not in current_word_state.replace(' ', ''):
                print(f"SUCCESS! AI guessed '{secret_word}' with {len(incorrect_guesses)} incorrect guesses.")
                return (True, incorrect_guesses)

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the API: {e}")
            return (False, incorrect_guesses)
        
        time.sleep(0.5)

    print(f"FAILURE! AI could not guess '{secret_word}'. Incorrect guesses: {', '.join(incorrect_guesses)}")
    return (False, incorrect_guesses)


def main():
    """
    Main function to run the test harness.
    """
    test_words = load_test_words(TEST_WORDS_FILE)
    if not test_words:
        print("No words to test. Exiting.")
        return

    start_time = time.time()
    results = {"success": 0, "failure": 0}
    total_incorrect_guesses_on_wins = 0
    failed_words_details = []

    unique_test_words = sorted(list(set(test_words)))
    total_words_to_test = len(unique_test_words)

    for word in unique_test_words:
        was_successful, incorrect_guesses_list = play_game(word)
        if was_successful:
            results["success"] += 1
            total_incorrect_guesses_on_wins += len(incorrect_guesses_list)
        else:
            results["failure"] += 1
            failed_words_details.append({
                "word": word,
                "guesses": incorrect_guesses_list
            })

    end_time = time.time()
    total_duration = end_time - start_time
    
    success_rate = (results["success"] / total_words_to_test) * 100 if total_words_to_test > 0 else 0
    avg_incorrect_guesses = total_incorrect_guesses_on_wins / results["success"] if results["success"] > 0 else 0

    print("\n\n" + "="*40)
    print("        Test Harness Summary")
    print("="*40)
    print(f"Total words tested: {total_words_to_test}")
    print(f"Words guessed correctly: {results['success']}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Average incorrect guesses per win: {avg_incorrect_guesses:.2f}")

    if failed_words_details:
        print("\n--- Details of Failed Words ---")
        for item in failed_words_details:
            guesses_str = ', '.join(item['guesses']) or 'None'
            print(f"Word: '{item['word']}' | Failed with incorrect guesses: {guesses_str}")
    
    print(f"\nTotal test duration: {total_duration:.2f} seconds")
    print("="*40)


if __name__ == "__main__":
    main()

