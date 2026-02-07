"""
Standalone verification of data uniqueness.
"""
import csv
from pathlib import Path

def verify():
    csv_path = Path("output/users.csv")
    
    if not csv_path.exists():
        print("❌ users.csv not found. Run user_factory.py first.")
        return False
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        emails = [row['email'] for row in reader]
    
    unique_count = len(set(emails))
    total_count = len(emails)
    
    if unique_count == total_count:
        print(f"✅ All {total_count} emails are unique!")
        return True
    else:
        print(f"❌ Found {total_count - unique_count} duplicate emails")
        return False

if __name__ == "__main__":
    verify()
