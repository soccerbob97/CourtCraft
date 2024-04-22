import zipfile
import os

def main():
    for i in range(4, 24):
        if i < 10:
            year = "0" + str(i)
        else:
            year = str(i)
        file_name = f'NBA_20{year}_Shots.csv.zip'
        if not os.path.isfile(file_name):
            print("MISSING THIS FILE: ", file_name)
            return None 
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            print("extracting ", file_name)
            zip_ref.extractall()

main()