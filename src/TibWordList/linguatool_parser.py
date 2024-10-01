# combine_tibetan_words.py
import os
from utils import read_json_file, write_json_file

def linguatool_parser(input_output_files):
    """
    Processes a list of input JSON files to extract Tibetan words and writes them to corresponding output JSON files.

    Parameters:
        input_output_files (list of tuples): A list where each tuple contains:
            - input_file (str): Path to the input JSON file.
            - output_file (str): Path to the output JSON file where extracted words will be saved.

    Returns:
        None
    """
    for input_file, output_file in input_output_files:
        tibetan_words = []  # Initialize an empty list for each file

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"Created output directory: '{output_dir}'")
            except Exception as e:
                print(f"Failed to create directory '{output_dir}': {e}")
                continue

        # Check if the input file exists
        if not os.path.exists(input_file):
            print(f"Warning: File '{input_file}' does not exist and will be skipped.")
            continue

        # Load the JSON data from the file using the utility function
        try:
            data = read_json_file(input_file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from '{input_file}': {e}")
            continue
        except FileNotFoundError as e:
            print(f"Error reading '{input_file}': {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while reading '{input_file}': {e}")
            continue

        # Navigate to the 'data' section of the JSON
        records = data.get('data', {})

        # Iterate over each record
        for record in records.values():
            tibetan_entry = record.get('Tibetan', {})
            word = tibetan_entry.get('Word', '').strip()
            if word:
                tibetan_words.append(word)
            else:
                print(f"Warning: Empty word encountered in file '{input_file}'. Skipping.")

        # Save the list of Tibetan words to a JSON file using the utility function
        try:
            write_json_file(output_file, tibetan_words)
        except Exception as e:
            print(f"An error occurred while writing to '{output_file}': {e}")
            continue

        print(f"Extracted {len(tibetan_words)} Tibetan words from '{input_file}' into '{output_file}'.")
        
if __name__ == "__main__":
    """
    Main function to execute the linguatool_parser and combine_word_list functions.
    """
    # Define the list of input and output file pairs
    input_output_files = [
        ('data/linguatools/linguatools_page1.json', 'data/output/linguatools/linguatools_page1.json'),
        ('data/linguatools/linguatools_page2.json', 'data/output/linguatools/linguatools_page2.json')
    ]

    # Call the linguatool_parser to process the input files
    linguatool_parser(input_output_files)



