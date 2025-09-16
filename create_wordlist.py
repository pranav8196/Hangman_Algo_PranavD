import re
import os
from PyPDF2 import PdfReader

def create_word_list_from_pdf(pdf_path):
    """
    Reads a PDF, extracts aviation terms (text before " — ") from pages 3-353,
    cleans them, and saves them to a file.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            total_pages = len(reader.pages)
            print(f"PDF has {total_pages} pages. Extracting from pages 3 to 353...")
            
            # Adjust for 0-based indexing
            start_page, end_page = 2, 352  
            if end_page >= total_pages:
                end_page = total_pages - 1

            found_words = set()

            for i in range(start_page, end_page + 1):
                page_text = reader.pages[i].extract_text() or ""
                lines = page_text.splitlines()

                for line in lines:
                    line = line.strip()
                    # Only consider lines with space-dash-space (definition separator)
                    if not line or " — " not in line:
                        continue
                    
                    # Split at " — " and take the left part (the term)
                    term = line.split(" — ", 1)[0].strip()

                    # Clean: keep letters, numbers, and spaces
                    cleaned_term = re.sub(r'[^A-Za-z0-9 ]+', '', term).strip()

                    # Uppercase for consistency
                    cleaned_term = cleaned_term.upper()

                    # Add only meaningful terms
                    if len(cleaned_term) >= 3 and not cleaned_term.isdigit():
                        found_words.add(cleaned_term)

        # Sort and save
        sorted_words = sorted(found_words)
        os.makedirs('data', exist_ok=True)
        output_path = os.path.join('data', 'airlines.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in sorted_words:
                f.write(word + '\n')

        print(f"\nSuccessfully created word list with {len(sorted_words)} unique terms.")
        print(f"File saved to: {output_path}")

        return sorted_words

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    pdf_filename = "aviationdictionary (1).pdf"
    extracted_words = create_word_list_from_pdf(pdf_filename)

    if extracted_words:
        print("\nSample of the first 20 extracted words:")
        for word in extracted_words[:20]:
            print(word)
