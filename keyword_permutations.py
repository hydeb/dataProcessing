import csv
import subprocess
import os

# Function to get permutations from Ollama Llama 3.2
def get_permutations(keyword):
    try:
        command = f'ollama run llama3.2 "Generate variations or permutations of the keyword: {keyword}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            permutations = result.stdout.strip().split('\n')
            permutations = [p.strip() for p in permutations if p.strip()]
            return ', '.join(permutations) if permutations else 'No permutations found'
        else:
            return f'Error: {result.stderr}'
    except Exception as e:
        return f'Error: {str(e)}'

# Function to try opening file with different encodings
def try_open_csv(file_path):
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', newline='', encoding=encoding) as csvfile:
                # Read a small portion to test
                csvfile.read(1024)
                # If successful, return the encoding
                return encoding
        except UnicodeDecodeError as e:
            print(f"Tried encoding '{encoding}' - failed: {e}")
    raise Exception("Could not decode file with any supported encoding.")

# Function to process the CSV file
def process_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    # Detect workable encoding
    try:
        encoding = try_open_csv(input_file)
        print(f"Using encoding: {encoding}")
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Read the CSV with the detected encoding
    rows = []
    try:
        with open(input_file, 'r', newline='', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Check for required columns
            required_columns = {'RF filter keywords', 'Keyword colors', 'Risk Score', 
                              'Customer', 'Permutations', 'Notes'}
            if not all(col in reader.fieldnames for col in required_columns):
                print(f"Error: CSV is missing one or more required columns. Found: {reader.fieldnames}")
                return
            
            # Process each row
            for row in reader:
                rf_keywords = row['RF filter keywords'].strip()
                if rf_keywords:
                    permutations = get_permutations(rf_keywords)
                    row['Permutations'] = permutations
                rows.append(row)
    
        # Write to output file in UTF-8
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['RF filter keywords', 'Keyword colors', 'Risk Score', 
                         'Customer', 'Permutations', 'Notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"Processing complete. Results written to '{output_file}'")
    
    except Exception as e:
        print(f"Error during processing: {e}")

# Main execution
if __name__ == "__main__":
    input_file = 'input.csv'  # Your input file
    output_file = 'output.csv'  # Your output file
    print("Starting CSV processing...")
    process_csv(input_file, output_file)
