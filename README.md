# Hangman Solving Algorithm for IndiGo
This repository contains an intelligent Hangman solver developed for the Artificial Intelligence & Machine Learning role assessment at IndiGo. The algorithm is designed to guess words from the Airlines domain with high accuracy and efficiency, operating within a six-guess limit.

The project is structured as a self-contained web service, allowing it to be evaluated programmatically as per the assessment guidelines.

Approach or Strategy
The core of this project is a Probabilistic Reduction Approach. Instead of making generic guesses, the algorithm's strategy is to guess the letter that is most likely to appear in the set of all possible valid words at any given turn. This is achieved through a multi-tiered strategy and a sophisticated data pipeline.

The Data Pipeline
The intelligence of the solver is derived from a custom, domain-specific corpus. This corpus is generated and refined through a two-step process that exemplifies a professional data science workflow:

Corpus Building (corpus_builder.py): A "smart" web scraper fetches raw text from a curated list of over 60 aviation-related URLs. This script intelligently parses HTML structure to capture not just individual words but also context-rich phrases, which provides valuable statistical information about real-world letter frequencies.

Dictionary Usage: To ensure the corpus is rich in aviation-specific terminology, an external aviation dictionary was also leveraged.

Source: [Jeppesen Aviation Dictionary]("https://clearskywords.files.wordpress.com/2014/12/aviationdictionary.pdf) 

Citation: Gomez, J. (2008). The Aviation Dictionary for Pilots and Aviation Maintenance Technicians. Jeppesen Sanderson.

Corpus Refinement (refine_corpus.py): The raw, noisy data is cleaned by a second script. This script validates scraped words against the aviation dictionary, discards structural junk (like "alphabet soup" or concatenated text), and ensures the final corpus is of the highest quality.

The Guessing Algorithm (hangman_ai.py)
The algorithm's logic is encapsulated in a "graceful degradation" system designed to always make the most informed guess possible:

Tier 1: Specialized Airlines Corpus: The primary strategy uses our custom-built, refined airlines_corpus.txt. The algorithm filters this list based on the current word state (length and known letters) and performs a frequency analysis on the remaining "candidate words" to find the statistically most likely next letter.

Tier 2: General English Corpus Fallback: If the specialized corpus yields no possible candidates (i.e., the word is out-of-domain), the solver seamlessly falls back to using a large, general English dictionary, running the exact same filtering and frequency logic.

Tier 3: Letter Frequency Safety Net: In the rare case that a word is not in either dictionary, the algorithm has a final safety net. It will guess the most common letter in the English language that has not yet been tried, ensuring the program never fails to make a guess.

# Running & Testing Instructions
This project is designed to run with minimal setup from a system terminal.

1. Setup
First, clone the repository and navigate into the project directory.

git clone <your-repo-url>
cd Hangman_Game_Model

Next, create and activate a Python virtual environment.

Create the virtual environment
python -m venv venv

Activate the environment based on your operating system and terminal:

On macOS / Linux:

source venv/bin/activate

On Windows (Command Prompt / PowerShell):

.\venv\Scripts\activate

On Windows (Git Bash):

source venv/Scripts/activate

Finally, install all the required libraries using the requirements.txt file.

pip install -r requirements.txt

2. Running the Application
The project runs as a local web service. To start the solver, run the API script in one terminal.

python api.py

You will see a confirmation that the model has loaded and the server is running on http://127.0.0.1:5000.

3. Evaluating the Model
The algorithm's performance is evaluated using the test_harness.py script. This script reads a list of words from an external file, plays a full game for each one, and reports the final results.

To run with your own list of 100 words:

Open the words_to_test.txt file.

Delete the sample words provided.

Paste in your own list of 100 words (one word or phrase per line).

Save the file.

Once the API server is running, open a second terminal (with the virtual environment activated) and run the test harness:

python test_harness.py

The script will play through each word and print a final summary of the success rate and average incorrect guesses.

Libraries Used
This project relies on a small number of well-known, standard libraries:

requests: For communicating with the API server.

beautifulsoup4: For parsing HTML in the corpus_builder.py script.

Flask: For creating the simple web API.

Standard Python libraries such as re, os, time, and collections are also used.
