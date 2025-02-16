import os
import re

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'} 

def format_with_leading_zeros(number:int|float, leading_digits_count:int)->str:
    if isinstance(number, float) and number.is_integer():
        number = int(number)
    num_str = str(number)
    parts = num_str.split('.')
    whole_part = parts[0]
    padded_whole = whole_part.zfill(leading_digits_count)
    if len(parts) == 2: 
        return f"{padded_whole}.{parts[1]}"
    else:
        return padded_whole

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

    biggest_season = 0
    biggest_episode = 0
    for f in files:
        name, ext = os.path.splitext(f)
        season , episode = extract_season_episode(name)
        if episode is None:
            continue
        if biggest_season<season:
            biggest_season = season
        if biggest_episode<episode:
            biggest_episode = episode        
    
    season_leading_digit_count = len(str(int(biggest_season)))
    episode_leading_digit_count = len(str(int(biggest_episode)))

    for f in files:
        name, ext = os.path.splitext(f)
        s , e = extract_season_episode(name)
        if e is None:
            continue
        s = format_with_leading_zeros(s, season_leading_digit_count)
        e = format_with_leading_zeros(e, episode_leading_digit_count)
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
    
    print(f"Successfully renamed {len(name_mapping)} files")

if __name__ == "__main__":
    main()