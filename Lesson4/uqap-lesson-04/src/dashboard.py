"""
Web dashboard for visualizing parsed user data
"""
from flask import Flask, render_template, jsonify
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_parser import load_users, benchmark_parsing
from src.models import UserModel

# Set template folder to parent directory's templates folder
template_dir = Path(__file__).parent.parent / "templates"
app = Flask(__name__, template_folder=str(template_dir))


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/users')
def get_users():
    """API endpoint to get all users"""
    try:
        data_dir = Path(__file__).parent.parent / "data"
        csv_file = data_dir / "test_users.csv"
        
        if not csv_file.exists():
            return jsonify({"error": "Data file not found"}), 404
        
        users = load_users(csv_file)
        users_data = [user.to_dict() for user in users]
        
        return jsonify({
            "users": users_data,
            "count": len(users_data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """API endpoint to get statistics"""
    try:
        data_dir = Path(__file__).parent.parent / "data"
        csv_file = data_dir / "test_users.csv"
        
        if not csv_file.exists():
            return jsonify({"error": "Data file not found"}), 404
        
        users = load_users(csv_file)
        metrics = benchmark_parsing(csv_file)
        
        # Calculate statistics
        role_counts = {}
        active_count = 0
        privileged_count = 0
        
        for user in users:
            role = user.role
            role_counts[role] = role_counts.get(role, 0) + 1
            if user.active:
                active_count += 1
            if user.is_privileged():
                privileged_count += 1
        
        return jsonify({
            "total_users": len(users),
            "active_users": active_count,
            "inactive_users": len(users) - active_count,
            "privileged_users": privileged_count,
            "role_distribution": role_counts,
            "performance": {
                "avg_time_ms": round(metrics['avg_time_ms'], 2),
                "time_per_record_ms": round(metrics['time_per_record_ms'], 4)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("UQAP Lesson 4 - Data Parsing Dashboard")
    print("="*60)
    print("\nDashboard starting on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
