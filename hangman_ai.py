import re
from collections import Counter
import os

class HangmanAI:
    """
    An Algo to play the game of Hangman, optimized for the Airlines domain.
    It uses a probabilistic reduction approach with a multi-tiered fallback system.
    """
    
    def __init__(self, data_dir="data"):
        """
        Initializes the Algo by loading knowledge sources (corpora) into memory
        from the specified data directory.
        """
        print("Initializing Hangman Algo...")
        airlines_corpus_path = os.path.join(data_dir, "airlines_corpus.txt")
        general_corpus_path = os.path.join(data_dir, "general_corpus.txt")

        self.airlines_corpus = self._load_corpus(airlines_corpus_path)
        self.general_corpus = self._load_corpus(general_corpus_path)
        
        # A fallback list of English letters ordered by frequency.
        self.fallback_letters = list("eariotnslcudpmhgbfywkvxzjq")
        print("Algo Initialized successfully.")

    def _load_corpus(self, file_path):
        """Helper function to load a word list from a file."""
        if not os.path.exists(file_path):
            print(f"Warning: Corpus file not found at '{file_path}'")
            return []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Read words and strip any leading/trailing whitespace.
                words = [line.strip() for line in f if line.strip()]
                print(f"Successfully loaded {len(words)} words from {file_path}.")
                return words
        except Exception as e:
            print(f"Error loading corpus from {file_path}: {e}")
            return []

    def make_guess(self, current_word_state, guessed_letters):
        """
        Makes an intelligent guess based on the current state of the game.

        Args:
            current_word_state (str): The current word state.
            guessed_letters (list): A list of letters that have already been guessed.

        Returns:
            str: The single best letter to guess next.
        """
        # Tier 1: Try to find a guess using the specialized Airlines corpus.
        best_guess = self._get_best_guess_from_corpus(self.airlines_corpus, current_word_state, guessed_letters)
        if best_guess:
            return best_guess

        # Tier 2: If Tier 1 fails, fall back to the general English corpus.
        best_guess = self._get_best_guess_from_corpus(self.general_corpus, current_word_state, guessed_letters)
        if best_guess:
            return best_guess

        # Tier 3: If both corpora fail, use the simple letter frequency fallback.
        return self._get_fallback_guess(guessed_letters)

    def _get_best_guess_from_corpus(self, corpus, current_word_state, guessed_letters):
        """
        Filters a corpus to find candidate words and returns the best letter to guess.
        This is the core probabilistic reduction algorithm.
        """
        
        
        word_components = re.split(r'\s{2,}', current_word_state)
        
        regex_parts = []
        for component in word_components:
            part_pattern = component.replace(' ', '').replace('_', '.')
            regex_parts.append(part_pattern)
            
        final_pattern = r'\s+'.join(regex_parts)
        
        try:
            # Compile the regex for an exact match from start to end.
            regex = re.compile(f"^{final_pattern}$")
        except re.error as e:
            print(f"Error compiling regex: {final_pattern} -> {e}")
            return None # Cannot proceed if the pattern is invalid

        # Filter the corpus using the generated regex to find all possible candidates.
        candidate_words = [word for word in corpus if regex.match(word)]

        if not candidate_words:
            return None # No candidates found

        # Frequency Analysis on Candidate Words
        all_letters_in_candidates = "".join(candidate_words)
        letter_counts = Counter(all_letters_in_candidates)

        # Remove letters that have already been guessed.
        for letter in guessed_letters:
            if letter in letter_counts:
                del letter_counts[letter]
        
        # Also remove spaces from the potential guesses.
        if ' ' in letter_counts:
            del letter_counts[' ']

        # If there are any valid letters left, return the most common one.
        if letter_counts:
            return letter_counts.most_common(1)[0][0]

        return None

    def _get_fallback_guess(self, guessed_letters):
        """
        Provides a simple fallback guess based on general English letter frequency
        if no candidates are found in any corpus.
        """
        for letter in self.fallback_letters:
            if letter not in guessed_letters:
                return letter
        # As an absolute last resort if all common letters are guessed
        return 'z'

