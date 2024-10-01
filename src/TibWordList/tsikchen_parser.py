# combine_tibetan_words.py
import csv
import os
from utils import write_json_file

def tsikchen_parser(input_file, output_file):
    """
    Extracts entries from the first column of a TSV file and writes them to a JSON file.

    Parameters:
        input_file (str): Path to the input TSV file.
        output_file (str): Path to the output JSON file where extracted entries will be saved.

    Returns:
        None
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: '{output_dir}'")
        except Exception as e:
            print(f"Failed to create directory '{output_dir}': {e}")
            return

    # List to store the first column values
    first_column_values = []

    # Open the TSV file and read its contents
    try:
        with open(input_file, 'r', encoding='utf-8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            
            # Attempt to read the header row
            try:
                header = next(reader)
                if '#' in header:
                    first_col_index = header.index('#')
                else:
                    first_col_index = 0
            except StopIteration:
                print(f"Warning: The TSV file '{input_file}' is empty.")
                return

            # Iterate over the rows and extract the first column
            for row_number, row in enumerate(reader, start=2):  # Start at 2 considering header
                if len(row) > first_col_index:
                    value = row[first_col_index].strip()
                    if value:  # Ensure the value is not empty
                        first_column_values.append(value)
                    else:
                        print(f"Warning: Empty value encountered at row {row_number} in file '{input_file}'. Skipping.")
                else:
                    print(f"Warning: Row {row_number} has insufficient columns in file '{input_file}'. Skipping.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading '{input_file}': {e}")
        return

    # Save the list to a JSON file using write_json_file
    try:
        write_json_file(output_file, first_column_values)
    except Exception as e:
        print(f"An error occurred while writing to '{output_file}': {e}")
        return

    print(f"Extracted {len(first_column_values)} entries from the first column of '{input_file}' into '{output_file}'.")

if __name__ == "__main__":
    # Define the input and output file paths
    input_file = 'data/input/tsikchen_data.tsv'
    output_file = 'data/output/tsikchen_entries.json'
    
    # Call the tsikchen_parser function
    tsikchen_parser(input_file, output_file)
    