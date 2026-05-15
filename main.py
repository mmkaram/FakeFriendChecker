import json


def extract_username(entry):
    """Extract username from either title or string_list_data.value."""
    if entry.get("title"):
        return entry["title"]

    string_list_data = entry.get("string_list_data", [])
    if string_list_data and string_list_data[0].get("value"):
        return string_list_data[0]["value"]

    return None


def load_usernames(file_path):
    """Load usernames from Instagram JSON export file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Some Instagram files are wrapped in relationships_following
        if isinstance(data, dict) and "relationships_following" in data:
            data = data["relationships_following"]

        usernames = set()

        for entry in data:
            username = extract_username(entry)
            if username:
                usernames.add(username.lower())

        return usernames

    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return set()


def main():
    followers = load_usernames("followers.json")
    following = load_usernames("following.json")

    print(f"Loaded {len(followers)} followers")
    print(f"Loaded {len(following)} following")

    non_followers = following - followers

    if non_followers:
        print("\nAccounts you follow who don't follow you back:")
        for user in sorted(non_followers):
            print(f"- {user}")
    else:
        print("Everyone you follow follows you back. You're in good company!")


if __name__ == "__main__":
    main()
