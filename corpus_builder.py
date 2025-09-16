import requests
from bs4 import BeautifulSoup
import re
import time

# A comprehensive list of URLs for the Airlines domain.
URLS = [
    "https://en.wikipedia.org/wiki/IndiGo_fleet",
    "https://en.wikipedia.org/wiki/IndiGo",
    "https://en.wikipedia.org/wiki/Airline",
    "https://en.wikipedia.org/wiki/Cargo",
    "https://en.wikipedia.org/wiki/List_of_airlines_of_India",
    "https://en.wikipedia.org/wiki/List_of_airports_in_India",
    "https://en.wikipedia.org/wiki/Largest_airlines_in_the_world",
    "https://en.wikipedia.org/wiki/List_of_pilot_training_institutes_in_India",
    "https://en.wikipedia.org/wiki/Narrow-body_aircraft",
    "https://en.wikipedia.org/wiki/Airbus",
    "https://en.wikipedia.org/wiki/Airbus_A320_family",
    "https://en.wikipedia.org/wiki/Codeshare_agreement",
    "https://en.wikipedia.org/wiki/List_of_IndiGo_destinations",
    "https://en.wikipedia.org/wiki/Aviation_call_sign",
    "https://en.wikipedia.org/wiki/Airline_codes",
    "https://en.wikipedia.org/wiki/List_of_airline_codes",
    "https://en.wikipedia.org/wiki/International_Air_Transport_Association",
    "https://en.wikipedia.org/wiki/International_Civil_Aviation_Organization",
    "https://en.wikipedia.org/wiki/Flight_number",
    "https://en.wikipedia.org/wiki/Interlining",
    "https://en.wikipedia.org/wiki/Airliner",
    "https://en.wikipedia.org/wiki/Aircraft",
    "https://en.wikipedia.org/wiki/Aircrew",
    "https://en.wikipedia.org/wiki/Commercial_aviation",
    "https://en.wikipedia.org/wiki/Airport_security",
    "https://en.wikipedia.org/wiki/List_of_low-cost_airlines",
    "https://en.wikipedia.org/wiki/Cargo_aircraft",
    "https://en.wikipedia.org/wiki/ATR_(aircraft_manufacturer)",
    "https://en.wikipedia.org/wiki/ATR_72",
    "https://en.wikipedia.org/wiki/Airbus_A320neo_family",
    "https://en.wikipedia.org/wiki/Airbus_A321",
    "https://en.wikipedia.org/wiki/Airline_seat",
    "https://en.wikipedia.org/wiki/Jet_fuel",
    "https://en.wikipedia.org/wiki/Aircraft_part",
    "https://en.wikipedia.org/wiki/Traffic_collision_avoidance_system",
    "https://en.wikipedia.org/wiki/Flag_carrier",
    "https://en.wikipedia.org/wiki/Change_of_gauge_(aviation)",
    "https://en.wikipedia.org/wiki/Directorate_General_of_Civil_Aviation_(India)",
    "https://en.wikipedia.org/wiki/Civil_aviation",
    "https://en.wikipedia.org/wiki/Aviation_in_India",
    "https://en.wikipedia.org/wiki/Aircraft_Accident_Investigation_Bureau_(India)",
    "https://en.wikipedia.org/wiki/Bureau_of_Civil_Aviation_Security",
    "https://en.wikipedia.org/wiki/Airports_Authority_of_India",
    "https://en.wikipedia.org/wiki/Ministry_of_Civil_Aviation_(India)",
    "https://en.wikipedia.org/wiki/International_airport",
    "https://en.wikipedia.org/wiki/List_of_busiest_airports_in_India",
    "https://en.wikipedia.org/wiki/Freight_transport",
    "https://en.wikipedia.org/wiki/Cargo_airline",
    "https://en.wikipedia.org/wiki/Boeing",
    "https://en.wikipedia.org/wiki/Air_cargo",
    "https://en.wikipedia.org/wiki/Travel_class",
    "https://en.wikipedia.org/wiki/Fare_basis_code",
    "https://en.wikipedia.org/wiki/General_aviation",
    "https://en.wikipedia.org/wiki/Boeing_777",
    "https://epicflightacademy.com/aviation-terminology/",
    "https://centreforaviation.com/about/glossary",
    "https://vivekanandatravelspltd.com/blog/must-know-airport-terminologies-airport-dictionary/",
    "https://www.globeair.com/glossary"
]

OUTPUT_FILE = "airlines_corpus.txt"

def scrape_and_clean():
    """
    Scrapes URLs, extracts relevant text by targeting specific HTML tags,
    cleans it to be Hangman-ready, and saves the unique words/phrases to a file.
    """
    print("Starting corpus generation with scraping...")
    
    corpus = set()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in URLS:
        try:
            print(f"Scraping: {url}")
            time.sleep(1) 
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Scraping Logic
            
            for tag in soup.find_all(['p', 'li', 'th', 'td', 'h1', 'h2', 'h3']):
                text_content = tag.get_text().lower()
                
                # Remove text in brackets (like [1], [edit], etc.)
                text_content = re.sub(r'\[.*?\]', '', text_content)

                # Find all valid Hangman words/phrases in the tag's text
                words = re.findall(r'\b[a-z\s]{2,}\b', text_content)
                
                for word in words:
                    # Normalize whitespace and strip leading/trailing spaces
                    cleaned_word = re.sub(r'\s+', ' ', word).strip()
                    if cleaned_word:
                        corpus.add(cleaned_word)

        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {url}: {e}")

    print(f"\nFound {len(corpus)} unique words/phrases.")
    
    sorted_corpus = sorted(list(corpus))
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for word in sorted_corpus:
                f.write(f"{word}\n")
        print(f"Corpus successfully saved to {OUTPUT_FILE}")
    except IOError as e:
        print(f"Error writing to file {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    scrape_and_clean()

