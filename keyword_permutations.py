import csv
import subprocess
import os
import chardet

# Detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

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

# Function to process the CSV file
def process_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    # Detect encoding
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")
    
    # Read the CSV and process it
    rows = []
    try:
        with open(input_file, 'r', newline='', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            
            required_columns = {'RF filter keywords', 'Keyword colors', 'Risk Score', 
                              'Customer', 'Permutations', 'Notes'}
            if not all(col in reader.fieldnames for col in required_columns):
                print("Error: CSV is missing one or more required columns")
                return
            
            for row in reader:
                rf_keywords = row['RF filter keywords'].strip()
                if rf_keywords:
                    permutations = get_permutations(rf_keywords)
                    row['Permutations'] = permutations
                rows.append(row)
    
        # Write the updated data to a new CSV (always use UTF-8 for output)
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['RF filter keywords', 'Keyword colors', 'Risk Score', 
                         'Customer', 'Permutations', 'Notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"Processing complete. Results written to '{output_file}'")
    
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}. Try a different encoding or fix the file.")

# Main execution
if __name__ == "__main__":
    input_file = 'input.csv'
    output_file = 'output.csv'
    print("Starting CSV processing...")
    process_csv(input_file, output_file)
