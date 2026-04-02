import csv
import random

# Configuration
num_rows = 50000
filename = "dataset.csv"
locations = ["mumbai", "kolkata", "chennai", "delhi", "bangalore"]
devices = ["android", "iphone", "web"]

def generate_data():
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Header
        writer.writerow(['amount', 'location', 'device', 'is_fraud'])
        
        for _ in range(num_rows):
            # Generate amount
            amount = random.randint(10, 100000)
            location = random.choice(locations)
            device = random.choice(devices)
            
            # Basic logic: Higher amounts have a higher probability of being fraud
            if amount > 70000:
                is_fraud = 1 if random.random() < 0.7 else 0
            elif amount > 20000:
                is_fraud = 1 if random.random() < 0.1 else 0
            else:
                is_fraud = 1 if random.random() < 0.01 else 0
                
            writer.writerow([amount, location, device, is_fraud])

if __name__ == "__main__":
    generate_data()
    print(f"Successfully created {filename} with {num_rows} rows.")