# combine_tibetan_words.py
import os
from utils import read_json_file, write_json_file

def combine_unique_word_list(root_directory):
    """
    Combines unique Tibetan words from all JSON files in the specified root directory and its subdirectories.

    Parameters:
        root_directory (str): The root directory to start searching for JSON files.

    Returns:
        list: A list containing all unique Tibetan words.
    """
    # Initialize a set to store unique Tibetan words
    unique_words = set()

    # Walk through the directory tree and collect all JSON files
    json_files = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith('.json'):
                json_files.append(os.path.join(dirpath, filename))

    # Process each JSON file
    for json_file in json_files:
        # Get the base name of the file for reporting purposes (optional)
        file_name = os.path.basename(json_file)
        
        # Load the list of Tibetan words from the JSON file using the utility function
        try:
            words = read_json_file(json_file)
            if not isinstance(words, list):
                print(f"Warning: The file '{json_file}' does not contain a list. Skipping.")
                continue
        except Exception as e:
            print(f"Error reading '{json_file}': {e}. Skipping.")
            continue

        # Add each word to the set of unique words
        for word in words:
            if word:
                unique_words.add(word)  
            else:
                print(f"Warning: Empty word encountered in file '{json_file}'. Skipping.")

    # Convert the set of unique words to a list
    combined_words = list(unique_words)

    return combined_words

if __name__ == "__main__":
    # Define the root directory and output file path
    root_dir = 'data/output'  # Replace with your actual root directory path
    output_file = 'data/output/combine_unique_tibetan_words/combined_unique_tibetan_word_list.json'
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}'")
    
    # Combine the word lists
    combined_words = combine_unique_word_list(root_dir)
    
    # Save the combined unique Tibetan words to a JSON file using the utility function
    try:
        write_json_file(output_file, combined_words)
    except Exception as e:
        print(f"Failed to write combined words to '{output_file}': {e}.")
    
    # Print summary information
    print(f"\nCombined unique Tibetan words saved to '{output_file}'")
    print(f"Total unique words: {len(combined_words)}")
