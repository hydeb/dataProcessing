import csv
import subprocess
import os

# Function to get permutations from Ollama Llama 3.2
def get_permutations(keyword):
    try:
        # Construct the command to run Ollama with the keyword
        #command = f'ollama run llama3.2 "Generate variations or permutations of the keyword: {keyword}"'
        prompt = f"List variations or synonyms for the keyword '{keyword}', separated by commas, without any additional text."
        command = ['ollama', 'run', 'llama3.2', prompt]
        
        # Execute the command and capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            # Split the output into a list, clean it, and return
            permutations = result.stdout.strip().split('\n')
            # Filter out empty lines and clean up the results
            permutations = [p.strip() for p in permutations if p.strip()]
            return ', '.join(permutations) if permutations else 'No permutations found'
        else:
            return f'Error: {result.stderr}'
            
    except Exception as e:
        return f'Error: {str(e)}'

# Function to process the CSV file
def process_csv(input_file, output_file):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    # Read the CSV and process it
    rows = []
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Verify required columns exist
        required_columns = {'RF filter keywords', 'Keyword colors', 'Risk Score', 
                          'Customer', 'Permutations', 'Notes'}
        if not all(col in reader.fieldnames for col in required_columns):
            print("Error: CSV is missing one or more required columns")
            return
        
        # Process each row
        for row in reader:
            rf_keywords = row['RF filter keywords'].strip()
            if rf_keywords:
                # Get permutations from Ollama
                permutations = get_permutations(rf_keywords)
                row['Permutations'] = permutations
            rows.append(row)
    
    # Write the updated data to a new CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['RF filter keywords', 'Keyword colors', 'Risk Score', 
                     'Customer', 'Permutations', 'Notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Processing complete. Results written to '{output_file}'")

# Main execution
if __name__ == "__main__":
    input_file = 'input.csv'  # Replace with your input CSV file name
    output_file = 'output.csv'  # Replace with your desired output CSV file name
    
    print("Starting CSV processing...")
    process_csv(input_file, output_file)
