import os
import re

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'} #lower case

def format_number(num):
    if isinstance(num, float) and num.is_integer():
        num = int(num)
    return str(num)
    
def extract_season_episode(show_name:str):
    numbers = re.findall(r'(\d+\.\d+|\d+)', show_name)
    numbers = [float(n) if '.' in n else int(n) for n in numbers]
    if len(numbers) == 0:
        if "pilot" in show_name.lower():
            return (0, 0)
        return (None, None)
    episode = numbers[-1]
    season = 1
    if len(numbers)>1:
        season = numbers[-2]
    return (season, episode)


def is_video_file(filename:str):
    _, extension = os.path.splitext(filename)
    return extension.lower() in VIDEO_EXTENSIONS

def main():
    show_name = input("""This script will attempt to rename all files in the current directory. 
                      It is recommended to save a copy of the directory before proceeding.
                      Please provide the name of the show for naming consistency.
                      Show name: """).strip()
    
    files = [f for f in os.listdir('.') if os.path.isfile(f) and is_video_file(f)]

    name_mapping = {}
    colliding_new_names = set()
        
    for f in files:
        name, ext = os.path.splitext(f)
        s , e = extract_season_episode(name)
        if e is None:
            continue
        new_filename = f"{show_name} S{s}E{e}{ext}"
        if new_filename in name_mapping.values():
            colliding_new_names.add(new_filename)
        name_mapping[f] = new_filename

    if len(colliding_new_names)>0:
        print("Renaming collisions detected:")
        for new in colliding_new_names:
            olds = [o for o in name_mapping.keys() if name_mapping[o] == new]
        print(f"{olds} -> {new}")
        input("Press any key to abort")
        return

    correctly_formatted_names = []
    for old, new in name_mapping.items():
        if old==new:
            correctly_formatted_names.append(old)
    
    for name in correctly_formatted_names:
        del name_mapping[name]

    if len(name_mapping) == 0:
        print("Nothing to rename detected")
        return

    print("Renaming Preview:")
    for old, new in name_mapping.items():
        print(f"{old} -> {new}")

    confirm = input("Proceed with renaming?(Y/N): ")
    if "y" != confirm.lower():
        print("Aborted")
        return   

    for old, new in name_mapping.items():
        try:
            os.rename(old, new)
            print(f"Renamed: {old} -> {new}")
        except Exception as e:
            print(f"Error renaming {old}: {str(e)}")
            return
    
    print(f"Successfully renamed {len(name_mapping)} files.")

if __name__ == "__main__":
    main()