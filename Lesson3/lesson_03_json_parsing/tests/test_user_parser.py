"""
Test suite for JSON parsing functionality.
Demonstrates production-grade test patterns.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.parser import parse_users_from_file, filter_adults, filter_active_adults
from utils.user_model import User
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_parse_users():
    """Test user parsing with realistic data and edge cases."""
    logger.info("=" * 60)
    logger.info("TEST: Parsing Users from JSON")
    logger.info("=" * 60)
    
    data_file = Path(__file__).parent.parent / "data" / "users.json"
    users = parse_users_from_file(data_file)
    
    logger.info(f"\nParsed {len(users)} users:")
    for user in users:
        logger.info(f"  {user}")
    
    # Assertions
    assert len(users) > 0, "Should parse at least some users"
    assert all(isinstance(u, User) for u in users), "All items should be User objects"
    assert all(u.id > 0 for u in users), "All users should have valid IDs"
    
    logger.info("[OK] Parsing test passed")
    return users


def test_filter_adults(users):
    """Test filtering for adult users."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST: Filtering Adult Users (age > 18)")
    logger.info("=" * 60)
    
    adults = filter_adults(users)
    
    logger.info(f"\nFound {len(adults)} adults:")
    for user in adults:
        logger.info(f"  {user}")
    
    # Assertions
    assert all(u.is_adult() for u in adults), "All filtered users should be adults"
    assert len(adults) < len(users), "Should filter out some users"
    
    # Verify age validation
    for user in adults:
        assert user.age is not None, "Adults should have known age"
        assert user.age > 18, f"User {user.name} age {user.age} is not > 18"
    
    logger.info("[OK] Adult filtering test passed")
    return adults


def test_filter_active_adults(users):
    """Test filtering for active adult users."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST: Filtering Active Adults")
    logger.info("=" * 60)
    
    active_adults = filter_active_adults(users)
    
    logger.info(f"\nFound {len(active_adults)} active adults:")
    for user in active_adults:
        logger.info(f"  {user}")
    
    # Assertions
    assert all(u.is_adult() and u.is_active for u in active_adults)
    
    logger.info("[OK] Active adult filtering test passed")
    return active_adults


def generate_html_report(users, adults, active_adults, output_path):
    """Generate an HTML visualization of the results."""
    # Build HTML template - use regular string to avoid f-string parsing issues with CSS
    html_template = """<!DOCTYPE html>
        <html>
        <head>
            <title>JSON Parsing Results</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 40px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin: 20px 0;
                }}
                .stat-box {{
                    padding: 20px;
                    border-radius: 4px;
                    text-align: center;
                }}
                .stat-box.blue {{ background: #3498db20; border-left: 4px solid #3498db; }}
                .stat-box.green {{ background: #2ecc7120; border-left: 4px solid #2ecc71; }}
                .stat-box.orange {{ background: #e67e2220; border-left: 4px solid #e67e22; }}
                .stat-number {{ font-size: 36px; font-weight: bold; }}
                .stat-label {{ color: #7f8c8d; margin-top: 5px; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ecf0f1;
                }}
                th {{
                    background: #34495e;
                    color: white;
                }}
                tr:hover {{ background: #f8f9fa; }}
                .badge {{
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .badge.adult {{ background: #2ecc71; color: white; }}
                .badge.minor {{ background: #e74c3c; color: white; }}
                .badge.unknown {{ background: #95a5a6; color: white; }}
                .badge.active {{ background: #3498db; color: white; }}
                .badge.inactive {{ background: #7f8c8d; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 JSON Parsing Analysis Report</h1>
                <p>Generated: {timestamp}</p>
                
                <div class="stats">
                    <div class="stat-box blue">
                        <div class="stat-number">{total_users}</div>
                        <div class="stat-label">Total Users Parsed</div>
                    </div>
                    <div class="stat-box green">
                        <div class="stat-number">{adults_count}</div>
                        <div class="stat-label">Adults (age > 18)</div>
                    </div>
                    <div class="stat-box orange">
                        <div class="stat-number">{active_adults_count}</div>
                        <div class="stat-label">Active Adults</div>
                    </div>
                </div>
                
                <h2>All Parsed Users</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Email</th>
                            <th>Status</th>
                            <th>Category</th>
                        </tr>
                    </thead>
                    <tbody>
        {user_rows}
                    </tbody>
                </table>
            </div>
        </body>
        </html>"""
    
    # Build user rows
    user_rows = ""
    for user in users:
        age_display = str(user.age) if user.age else "Unknown"
        age_badge = "adult" if user.is_adult() else ("minor" if user.age else "unknown")
        status_badge = "active" if user.is_active else "inactive"
        
        user_rows += f"""                        <tr>
                            <td>{user.id}</td>
                            <td>{user.name}</td>
                            <td>{age_display}</td>
                            <td>{user.email or 'N/A'}</td>
                            <td><span class="badge {status_badge}">{status_badge.upper()}</span></td>
                            <td><span class="badge {age_badge}">{age_badge.upper()}</span></td>
                        </tr>
        """
    
    # Format the template with actual values
    html = html_template.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total_users=len(users),
        adults_count=len(adults),
        active_adults_count=len(active_adults),
        user_rows=user_rows
    )
    
    report_path = output_path / "report.html"
    report_path.write_text(html)
    logger.info(f"\n📊 Generated HTML report: {report_path}")


def run_all_tests():
    """Execute all tests and generate reports."""
    print("\n" + "🚀 " * 30)
    print("LESSON 3: JSON PARSING - PRODUCTION PATTERNS")
    print("🚀 " * 30 + "\n")
    
    try:
        # Run tests
        users = test_parse_users()
        adults = test_filter_adults(users)
        active_adults = test_filter_active_adults(users)
        
        # Generate report
        output_path = Path(__file__).parent.parent / "output"
        generate_html_report(users, adults, active_adults, output_path)
        
        # Final summary
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print(f"Total Users: {len(users)}")
        print(f"Adults: {len(adults)}")
        print(f"Active Adults: {len(active_adults)}")
        print(f"\nView HTML report: {output_path / 'report.html'}")
        print("=" * 60)
        
        return True
        
    except AssertionError as e:
        logger.error(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        logger.error(f"\n💥 UNEXPECTED ERROR: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
