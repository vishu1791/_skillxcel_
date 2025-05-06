import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()  # Generate a salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
    return hashed.decode('utf-8')  # Convert bytes to string

# Example usage:
passwords = ["password123", "securepass", "mypassword", "test1234", "flaskapp"]
hashed_passwords = [hash_password(pw) for pw in passwords]

for i, hp in enumerate(hashed_passwords, 1):
    print(f"Hashed Password {i}: {hp}")
