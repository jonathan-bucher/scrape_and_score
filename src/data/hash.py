# generating keys for quarterbacks and defenses by year

import hashlib

# Function to generate a hash key
def generate_key(position, name = False, team = False, year = False):

    if position == 'defense':
        # Concatenate team and year into a string
        key_string = f"{team}_{year}"

        # Create a MD5 hash of the string
        return hashlib.md5(key_string.encode()).hexdigest()[:8]
    
    elif position == 'quarterback':
        key_string = name
        return hashlib.md5(key_string.encode()).hexdigest()[:8]