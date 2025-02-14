# Consistent TV Show Episode names

A Python script to consistently rename TV show episode files for better media player organization.

## Use Case

When you have a collection of TV show episodes with inconsistent naming that causes your media player to play them out of order, this script will:

1. Rename files to a consistent format
2. Extract season and episode numbers from original filenames
3. Handle special cases like .5 episodes and pilot episodes
4. Prevent naming collisions

## Features

- Consistent naming format: `Show Name SXXEYY.ext`
- Supports multiple video formats: `.mp4`, `.mkv`, `.avi`, `.mov`
- Handles:
  - Regular episodes
  - Half episodes (e.g., 14.5)
  - Pilot episodes (renamed to S00E00)
  - Complex filenames with special characters
- Collision detection
- Dry-run preview before renaming

## Usage

1. Place the script in your episodes folder
2. Run the script:
   ```bash
   python rename_episodes.py
   ```
3. Enter the show name when prompted
4. Review the preview of changes
5. Confirm to proceed with renaming

## Example

Before:
```
Show Name 1.mp4
5th episode of Show Name.mkv
Show Name Episode 14.5 Special.mp4
```

After:
```
Show Name S1E1.mp4
Show Name S1E5.mkv
Show Name S1E14.5.mp4
```

## Requirements

- Python 3.x
- No additional dependencies

## Safety Features

- Previews changes before renaming
- Detects and prevents naming collisions
- Preserves original file extensions
- Skips non-video files
- Aborts on errors

## Limitations

- Assumes season number precedes episode number
- Requires at least one number in filename (except for pilot episodes)
- Doesn't handle multi-episode files (e.g., S01E01-E02)
