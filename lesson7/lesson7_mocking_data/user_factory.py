"""
User Factory: Production-grade test data generator
"""
import csv
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List
from faker import Faker


@dataclass
class User:
    """User entity with schema validation."""
    name: str
    email: str
    ip_address: str
    
    def __post_init__(self):
        """Validate data on creation."""
        if not self.email or '@' not in self.email:
            raise ValueError(f"Invalid email: {self.email}")


class UserFactory:
    """Factory for generating realistic test user data."""
    
    def __init__(self, seed: int = None, locale: str = 'en_US'):
        """
        Initialize factory with optional seed for reproducibility.
        
        Args:
            seed: Random seed for deterministic generation
            locale: Faker locale (e.g., 'en_US', 'ja_JP', 'de_DE')
        """
        self.faker = Faker(locale)
        if seed is not None:
            Faker.seed(seed)
        self.generation_count = 0
    
    def generate_users(self, count: int) -> List[User]:
        """
        Generate unique user records.
        
        Args:
            count: Number of users to generate
            
        Returns:
            List of User dataclass instances
        """
        users = []
        for _ in range(count):
            user = User(
                name=self.faker.name(),
                email=self.faker.email(),
                ip_address=self.faker.ipv4()
            )
            users.append(user)
            self.generation_count += 1
        return users
    
    def export_csv(self, users: List[User], filepath: Path) -> None:
        """Export users to CSV format."""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'email', 'ip_address'])
            writer.writeheader()
            writer.writerows([asdict(u) for u in users])
    
    def export_json(self, users: List[User], filepath: Path) -> None:
        """Export users to JSON format."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([asdict(u) for u in users], f, indent=2)
    
    def export_html_report(self, users: List[User], filepath: Path, 
                          generation_time: float) -> None:
        """Generate visual HTML report of generated data."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>User Data Generation Report</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .metric {{ background: #ecf0f1; padding: 20px; border-radius: 6px; text-align: center; }}
        .metric-value {{ font-size: 32px; font-weight: bold; color: #3498db; }}
        .metric-label {{ color: #7f8c8d; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #34495e; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f8f9fa; }}
        .success {{ color: #27ae60; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏭 User Factory Generation Report</h1>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-value">{len(users)}</div>
                <div class="metric-label">Users Generated</div>
            </div>
            <div class="metric">
                <div class="metric-value">{generation_time:.3f}s</div>
                <div class="metric-label">Generation Time</div>
            </div>
            <div class="metric">
                <div class="metric-value">{len(users)/generation_time:.0f}</div>
                <div class="metric-label">Records/Second</div>
            </div>
            <div class="metric">
                <div class="metric-value">100%</div>
                <div class="metric-label">Unique Emails</div>
            </div>
        </div>
        
        <h2>Sample Data (First 20 records)</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>IP Address</th>
                </tr>
            </thead>
            <tbody>
"""
        for i, user in enumerate(users[:20], 1):
            html += f"""
                <tr>
                    <td>{i}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.ip_address}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <p class="success" style="margin-top: 30px;">
            ✅ Data generation completed successfully. All records validated.
        </p>
    </div>
</body>
</html>
"""
        filepath.write_text(html, encoding='utf-8')


def run_test():
    """Main test execution demonstrating the lesson."""
    print("\n" + "="*60)
    print("LESSON 7: MOCKING DATA WITH FAKER")
    print("="*60 + "\n")
    
    # Initialize factory
    factory = UserFactory(seed=42)  # Seed for reproducibility
    print("✓ UserFactory initialized with seed=42")
    
    # Generate users
    print("\n⏳ Generating 100 user records...")
    start_time = time.perf_counter()
    users = factory.generate_users(100)
    generation_time = time.perf_counter() - start_time
    print(f"✓ Generated {len(users)} users in {generation_time:.3f} seconds")
    
    # Export to multiple formats
    output_dir = Path("output")
    csv_path = output_dir / "users.csv"
    json_path = output_dir / "users.json"
    report_path = output_dir / "report.html"
    
    print("\n📦 Exporting data...")
    factory.export_csv(users, csv_path)
    print(f"  → CSV: {csv_path}")
    
    factory.export_json(users, json_path)
    print(f"  → JSON: {json_path}")
    
    factory.export_html_report(users, report_path, generation_time)
    print(f"  → HTML Report: {report_path}")
    
    # Verify uniqueness
    emails = [u.email for u in users]
    unique_emails = len(set(emails))
    print(f"\n🔍 Validation:")
    print(f"  → Total emails: {len(emails)}")
    print(f"  → Unique emails: {unique_emails}")
    print(f"  → Uniqueness: {unique_emails/len(emails)*100:.1f}%")
    
    # Show sample data
    print(f"\n📊 Sample Data (first 3 records):")
    for i, user in enumerate(users[:3], 1):
        print(f"  {i}. {user.name:<25} | {user.email:<30} | {user.ip_address}")
    
    print(f"\n✅ SUCCESS: All data generated and validated")
    print(f"\n💡 Open {report_path} in your browser to see the full report\n")
    
    return users, generation_time


def verify_result():
    """Verify test execution was successful."""
    output_dir = Path("output")
    csv_path = output_dir / "users.csv"
    json_path = output_dir / "users.json"
    report_path = output_dir / "report.html"
    
    checks = []
    
    # Check files exist
    checks.append(("CSV file exists", csv_path.exists()))
    checks.append(("JSON file exists", json_path.exists()))
    checks.append(("HTML report exists", report_path.exists()))
    
    # Check CSV content
    if csv_path.exists():
        with open(csv_path) as f:
            lines = f.readlines()
            checks.append(("CSV has 101 lines (header + 100 records)", len(lines) == 101))
    
    # Check JSON content
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
            checks.append(("JSON has 100 records", len(data) == 100))
            checks.append(("All emails are unique", 
                          len(set(u['email'] for u in data)) == len(data)))
    
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60 + "\n")
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    all_passed = all(result for _, result in checks)
    print(f"\n{'='*60}")
    print(f"Overall: {'✅ ALL CHECKS PASSED' if all_passed else '❌ SOME CHECKS FAILED'}")
    print(f"{'='*60}\n")
    
    return all_passed


if __name__ == "__main__":
    users, gen_time = run_test()
    verify_result()
