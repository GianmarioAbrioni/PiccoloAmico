import zipfile
import os

zip_path = 'attached_assets/PiccoloAmico_COMPLETO_FINAL_STATISTICHE.zip'
extract_to = '.'

print(f"Extracting {zip_path} to {extract_to}")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    # Print files in the zip
    print("Files in zip archive:")
    for file in zip_ref.namelist():
        print(f"- {file}")
    
    # Extract all files
    zip_ref.extractall(extract_to)
    print("Extraction completed")

# List files in the current directory
print("\nFiles in current directory after extraction:")
for root, dirs, files in os.walk(".", topdown=True):
    for name in files:
        print(os.path.join(root, name))