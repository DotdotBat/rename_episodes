import os
import pytest
from rename_episodes import extract_season_episode, is_video_file, format_with_leading_zeros

def test_extract_season_episode():
    # Basic cases
    assert extract_season_episode("Show Name 1") == (1, 1)
    assert extract_season_episode("5th episode") == (1, 5)
    
    # Decimal episodes
    assert extract_season_episode("Episode 14.5") == (1, 14.5)
    assert extract_season_episode("3X7.5") == (3, 7.5)
    
    # Season/episode combinations
    assert extract_season_episode("2 1") == (2, 1)
    assert extract_season_episode("Season 3 Episode 13.5") == (3, 13.5)
    
    # Multiple numbers in title
    assert extract_season_episode("300 Spartans 1 5") == (1, 5)
    
    # Pilot episodes
    assert extract_season_episode("PILOT episode") == (0, 0)
    assert extract_season_episode("pilot special") == (0, 0)
    e, s = extract_season_episode("no numbers")
    assert e is None and s is None

def test_format_number():
    assert format_with_leading_zeros(5, 1) == "5"
    assert format_with_leading_zeros(14.5, 2) == "14.5"
    assert format_with_leading_zeros(3.0, 1) == "3"
    assert format_with_leading_zeros(13.4, 4)  == "0013.4"
    assert format_with_leading_zeros(2, 2)     == "02"
    assert format_with_leading_zeros(-5, 3)    == "005"
    assert format_with_leading_zeros(123.45, 2)== "123.45"

def test_is_video_file():
    assert is_video_file("test.mp4") is True
    assert is_video_file("test.MKV") is True
    assert is_video_file("test.avi") is True
    assert is_video_file("test.txt") is False

def test_basic_renaming(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Show 1.mp4").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S1E1.mp4").exists()

def test_season_episode_extraction(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Show 2 3.mkv").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S2E3.mkv").exists()

def test_half_episode(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Episode 14.5 Special.avi").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S1E14.5.avi").exists()

def test_pilot_episode(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Pilot Special.mov").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S0E0.mov").exists()

def test_collision_detection(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "File1 1.mp4").touch()
    (tmp_path / "File 1.mp4").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    # Original files should remain
    assert (tmp_path / "File1 1.mp4").exists()
    assert (tmp_path / "File 1.mp4").exists()

def test_existing_file_collision(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Test Show S1E1.avi").touch()
    (tmp_path / "Episode 1.avi").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Episode 1.avi").exists()

def test_skip_non_video_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Notes.txt").touch()
    (tmp_path / "Episode 1.mp4").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Notes.txt").exists()
    assert (tmp_path / "Test Show S1E1.mp4").exists()

def test_complex_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Show Name Season 3 Episode 13.5 Special.mp4").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S3E13.5.mp4").exists()

def test_multiple_numbers_in_title(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "300 Spartans season 1 episode 5.mp4").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S1E5.mp4").exists()

def test_skip_non_pilot_without_numbers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Opening Credits.mkv").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Opening Credits.mkv").exists()

#new tests:

def test_existing_file_collision2(tmp_path, monkeypatch):
    """Test collision with existing file not being renamed"""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Existing S1E1.mp4").touch()
    (tmp_path / "Episode 1.mp4").touch()

    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Episode 1.mp4").exists()
    assert (tmp_path / "Existing S1E1.mp4").exists()

def test_complex_number_extraction(tmp_path, monkeypatch):
    """Test files with numbers in unexpected positions"""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Show 2023X15.7 Special.mkv").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S2023E15.7.mkv").exists()

def test_multiple_season_numbers(tmp_path, monkeypatch):
    """Test files with multiple season indicators"""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Season 2 Episode 3x15.avi").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S3E15.avi").exists()

def test_special_characters(tmp_path, monkeypatch):
    """Test filenames with special characters"""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Show Name! - 03x04.5 [HD].mkv").touch()
    
    inputs = iter(["Test Show", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    import rename_episodes
    rename_episodes.main()
    
    assert (tmp_path / "Test Show S3E4.5.mkv").exists()

