# combine_tibetan_words.py
import os
from utils import read_json_file, write_json_file

def combine_unique_word_list(root_directory):
    """
    Combines unique Tibetan words from all JSON files in the specified root directory and its subdirectories.

    Parameters:
        root_directory (str): The root directory to start searching for JSON files.

    Returns:
        tuple: A tuple containing:
            - combined_words (list): The list of combined unique Tibetan words.
            - duplicates (dict): A dictionary of duplicates and the files they were found in.
    """
    # Initialize a set to store unique Tibetan words
    unique_words = set()

    # List to store the combined unique Tibetan words
    combined_words = []

    # Dictionary to keep track of duplicates and their corresponding file names
    duplicates = {}

    # Walk through the directory tree and collect all JSON files
    json_files = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith('.json'):
                json_files.append(os.path.join(dirpath, filename))

    # Process each JSON file
    for json_file in json_files:
        # Get the base name of the file for reporting duplicates
        file_name = os.path.basename(json_file)
        
        # Load the list of Tibetan words from the JSON file using the utility function
        try:
            words = read_json_file(json_file)
            if not isinstance(words, list):
                print(f"Warning: The file '{json_file}' does not contain a list. Skipping.")
                continue
        except Exception:
            # Error messages are already handled in the utility function
            continue

        # Process each word in the list
        for word in words:
            if word:
                if word not in unique_words:
                    unique_words.add(word)
                    combined_words.append(word)
                else:
                    # Record the duplicate word and the file it was found in
                    if word not in duplicates:
                        duplicates[word] = [file_name]
                    else:
                        duplicates[word].append(file_name)
                    print(f"Duplicate found: '{word}' in file '{json_file}'")
            else:
                print(f"Warning: Empty word encountered in file '{json_file}'. Skipping.")
    
    return combined_words, duplicates

if __name__ == "__main__":
    # Define the root directory and output file path
    root_dir = 'data/output'  # Replace with your actual root directory path
    output_file = 'data/output/combine_unique_tibetan_words/combined_unique_tibetan_words.json'
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}'")
    
    # Combine the word lists
    combined_words, duplicates = combine_unique_word_list(root_dir)
    
    # Save the combined unique Tibetan words to a JSON file using the utility function
    try:
        write_json_file(output_file, combined_words)
    except Exception:
        print(f"Failed to write combined words to '{output_file}'.")
    
    # Print summary information
    print(f"\nCombined unique Tibetan words saved to '{output_file}'")
    print(f"Total unique words: {len(combined_words)}")
    
    # If there were duplicates, print them
    if duplicates:
        print("\nDuplicates found across files:")
        for word, files in duplicates.items():
            file_list = ', '.join(files)
            print(f"'{word}' found in files: {file_list}")

