import random
import string
import pandas as pd

# Function to generate random password
def generate_password(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

# Generate synthetic dataset
def create_synthetic_password_data(n=1000):
    data = []

    for _ in range(n):

        category = random.choice(["weak", "medium", "strong"])

        if category == "weak":
            length = random.randint(4, 6)
            chars = string.ascii_lowercase
        elif category == "medium":
            length = random.randint(6, 10)
            chars = string.ascii_letters + string.digits
        else:  # strong
            length = random.randint(10, 16)
            chars = string.ascii_letters + string.digits + string.punctuation

        password = generate_password(length, chars)

        data.append([password, category])

    # Name of the dataset
    random_password = pd.DataFrame(data, columns=["password", "strength"])

    return random_password


# Create dataset
random_password = create_synthetic_password_data(10000)

# Save to CSV
random_password.to_csv("random_password.csv", index=False)

random_password.head()
