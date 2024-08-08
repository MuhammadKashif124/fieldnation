import os
import json

def list_chrome_profiles(user_data_dir):
    profiles = []
    for item in os.listdir(user_data_dir):
        item_path = os.path.join(user_data_dir, item)
        if os.path.isdir(item_path) and (item.startswith("Profile") or item == "Default"):
            preferences_path = os.path.join(item_path, "Preferences")
            if os.path.isfile(preferences_path):
                with open(preferences_path, 'r', encoding='utf-8') as f:
                    preferences = json.load(f)
                    profile_name = preferences.get('profile', {}).get('name', 'Unknown')
                    profiles.append((item, profile_name))
    return profiles

user_data_dir = os.path.expanduser(r'C:\Users\evenb\AppData\Local\Google\Chrome\User Data')
profiles = list_chrome_profiles(user_data_dir)

for folder_name, profile_name in profiles:
    print(f"Folder: {folder_name} - Profile Name: {profile_name}")
