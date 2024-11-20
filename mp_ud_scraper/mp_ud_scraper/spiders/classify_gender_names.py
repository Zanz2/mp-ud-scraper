import json
import nomquamgender as nqg
import pandas as pd
from tqdm import tqdm
import argparse

def process_jsonl_with_gender(input_file):
    # Initialize the gender classifier
    model = nqg.NBGC()
    
    # Read input file and store modified records
    modified_records = []
    total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))

    # Read the input JSONL file
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in tqdm(f, total=total_lines, desc="Processing names"):
            record = json.loads(line.strip())
            
            # Get gender prediction for the full name
            if 'case_full_name' in record and record['case_full_name']:
                result = model.annotate([record['case_full_name']], as_df=True)
                p_gf = result['p(gf)'].iloc[0]
                
                # Handle NaN values
                if pd.isna(p_gf):
                    record['gender'] = '?'
                    record['gender_confidence'] = 0.0
                else:
                    record['gender'] = 'F' if p_gf > 0.5 else 'M'
                    record['gender_confidence'] = abs(p_gf - 0.5) * 2
            else:
                record['gender'] = '?'
                record['gender_confidence'] = 0.0
            
            modified_records.append(record)
    
    # Write the modified records to output file
    extension = input_file.split(".")[-1]
    base_name = input_file.split(".")[0]
    output_file = f"{base_name}_gendered.{extension}"
    with open(output_file, 'w', encoding='utf-8') as f:
        for record in modified_records:
            f.write(json.dumps(record) + '\n')
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Add gender predictions to a JSONL file')
    parser.add_argument('input_file', help='Path to input JSONL file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the processing
    process_jsonl_with_gender(args.input_file)