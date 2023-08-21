import os
import json

def validateData():
    current_dir = os.path.join(os.getcwd(), "data")
    list_path = os.path.join(current_dir, "_list.json")
    levels = []
    had_error = False
    with open(list_path, "r") as file:
        levels = json.load(file)
        
    for filename in levels:
        if filename.startswith("_"):
                continue
        file_path = os.path.join(current_dir, f"{filename}.json")
        lines = []
        with open(file_path, "r") as file:
            data = json.load(file)
            records = data["records"]
            names = []
            for record in records:
                name = record["user"].lower()
                if name in names:
                    had_error = True
                    print(f"Duplicate {filename}: {name}")
                    
                names.append(name)
                
    if had_error:
        sys.exit(1)

if __name__ == "__main__":
    validateData()
