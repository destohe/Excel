# Created originally to instantly compare assyst and Jira exports

import pandas as pd
import os
import PySimpleGUI as sg

def read_file(file_path):
    # Check if file is CSV/XLS/XLSX
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported File Format. Please Provide CSV, XLS or XLSX Files...")

def compare_columns(file1, file2):
    # Load files
    df1 = read_file(file1)
    df2 = read_file(file2)
    
    print("Columns in File 1:", df1.columns.tolist())
    print("Columns in File 2:", df2.columns.tolist())
    
    # Check columns
    col1 = input("Enter the column name from File 1 to Compare:")
    col2 = input("Enter the column name from File 2 to Compare:")
    
    if col1 not in df1.columns or col2 not in df2.columns:
        print("One or both of these columns does not exist. Please check and try again.")
        return
    
    # Load column data as a clean string
    df1[col1] = df1[col1].astype(str).str.strip()
    df2[col2] = df2[col2].astype(str).str.strip()
    
    ###DEBUGGING
    # print(f"Values in {col1} from File 1")
    # print(df1[col1].tolist())
    # print(f"Values in {col2} from File 2")
    # print(df2[col2].tolist())

    matching_values = df1[col1][df1[col1].isin(df2[col2])].unique()

    # Check if user wants match or non match and check depending on decision
    comparison_choice = input("Do you want to find (m)atches or (n)on-matches? (m/n): ").strip().lower()
    
    if comparison_choice not in ['m', 'n']:
        print("Invalid Choice, please pick either M for matches or N for non-matches")
        return

    values = []
    if comparison_choice == 'm':
        values = df1[col1][df1[col1].isin(df2[col2])].unique()
    elif comparison_choice == 'n':
        values = df1[col1][~df1[col1].isin(df2[col2])].unique()
    
    # Add total matches/non matches
    total_matches = len(values)
    print(f"Total Matches Found: {total_matches}")
    
    print("Matching Values:")
    for value in values:
        print(value)
    
    # Check if user wants to save results
    save_to_file = input("Do you want to save the matching values to a text file? (yes/no): ").strip().lower()
    # If yes then right results into a file and print the filepath so the user can find the file easily
    if save_to_file == "yes" or save_to_file == "y":
        output_file = 'values.txt'
        output_path = os.path.join(os.getcwd(), output_file)
        with open(output_path, 'w') as f:
            f.write(f"Total values found: {total_matches} \n")
            f.write(f"Values: \n")
            for value in values:
                f.write(f"{value}\n")
        print(f"Values saved to {output_file}")

# Input Filepaths Here
file1 = input("File 1 path: ")
file2 = input("File 2 path: ")

# Example hardcoded file paths for testing:
# file1 = r"C:\Users\a214802\Downloads\AssystExport_18June2024_NOTDONESEARCH.xls"
# file2 = r"C:\Users\a214802\Downloads\jira 2024-06-18T11_58_25+0100.csv"

compare_columns(file1, file2)
