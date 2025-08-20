import json

def load_usernames(file_path, is_following=False):
    """Load usernames from Instagram JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Followers are a list of objects
        if not is_following:
            return set(
                entry['string_list_data'][0]['value']
                for entry in data
                if entry.get('string_list_data')
            )
        # Following is under a key
        else:
            return set(
                entry['string_list_data'][0]['value']
                for entry in data['relationships_following']
                if entry.get('string_list_data')
            )
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return set()

def main():
    followers = load_usernames('followers.json')
    following = load_usernames('following.json', is_following=True)

    non_followers = following - followers

    if non_followers:
        print("Accounts you follow who don't follow you back:")
        for user in sorted(non_followers):
            print(f"- {user}")
    else:
        print("Everyone you follow follows you back. You're in good company!")

if __name__ == '__main__':
    main()
