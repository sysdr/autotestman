"""
CSV/Excel data parser with type safety
"""
import csv
from pathlib import Path
from typing import Iterator
import time

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not installed. Excel support disabled.")

from src.models import UserModel


def load_users_csv(file_path: Path) -> list[UserModel]:
    """
    Load users from CSV using standard library (no dependencies)
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        List of validated UserModel objects
        
    Raises:
        FileNotFoundError: If CSV doesn't exist
        ValueError: If data validation fails
    """
    if not file_path.exists():
        raise FileNotFoundError(f"CSV not found: {file_path}")
    
    users = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
            try:
                # Normalize boolean values
                active_val = row['active'].strip().upper()
                active = active_val in {'TRUE', '1', 'YES', 'Y'}
                
                user = UserModel(
                    email=row['email'].strip(),
                    password=row['password'].strip(),
                    role=row['role'].strip().lower(),
                    active=active,
                    created_at=row.get('created_at', None)
                )
                users.append(user)
                
            except (KeyError, ValueError) as e:
                raise ValueError(f"Error parsing row {row_num}: {e}") from e
    
    return users


def load_users_excel(file_path: Path, sheet_name: str = 'TestUsers') -> list[UserModel]:
    """
    Load users from Excel file using pandas
    
    Args:
        file_path: Path to Excel file (.xlsx or .xls)
        sheet_name: Name of sheet to read (default: 'TestUsers')
        
    Returns:
        List of validated UserModel objects
        
    Raises:
        ImportError: If pandas not installed
        FileNotFoundError: If Excel file doesn't exist
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("pandas required for Excel. Install: pip install pandas openpyxl")
    
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    # Read Excel with explicit dtypes to prevent type coercion
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        dtype={
            'email': str,
            'password': str,
            'role': str,
        },
        engine='openpyxl'
    )
    
    # Normalize boolean column
    if 'active' in df.columns:
        df['active'] = df['active'].map({
            'TRUE': True, 'FALSE': False,
            True: True, False: False,
            'true': True, 'false': False,
            1: True, 0: False
        })
    
    # Handle missing values
    df = df.fillna({'created_at': None})
    
    users = []
    for idx, row in df.iterrows():
        try:
            user = UserModel(
                email=row['email'].strip(),
                password=row['password'].strip(),
                role=row['role'].strip().lower(),
                active=row['active'],
                created_at=row.get('created_at', None)
            )
            users.append(user)
        except (KeyError, ValueError) as e:
            raise ValueError(f"Error parsing Excel row {idx + 2}: {e}") from e
    
    return users


def load_users_lazy(file_path: Path) -> Iterator[UserModel]:
    """
    Memory-efficient iterator that yields users one at a time
    
    Use this for large files (>10,000 rows) to avoid loading all into RAM
    
    Args:
        file_path: Path to CSV file
        
    Yields:
        UserModel objects one at a time
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            active = row['active'].strip().upper() in {'TRUE', '1', 'YES'}
            
            yield UserModel(
                email=row['email'].strip(),
                password=row['password'].strip(),
                role=row['role'].strip().lower(),
                active=active,
                created_at=row.get('created_at', None)
            )


def load_users(file_path: Path | str, **kwargs) -> list[UserModel]:
    """
    Universal loader - auto-detects format and loads accordingly
    
    Args:
        file_path: Path to data file (CSV or Excel)
        **kwargs: Additional arguments passed to specific loader
        
    Returns:
        List of validated UserModel objects
    """
    path = Path(file_path)
    
    if path.suffix == '.csv':
        return load_users_csv(path)
    elif path.suffix in {'.xlsx', '.xls'}:
        return load_users_excel(path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}. Use .csv, .xlsx, or .xls")


def benchmark_parsing(file_path: Path, runs: int = 5) -> dict:
    """
    Measure parsing performance
    
    Returns:
        Dictionary with performance metrics
    """
    times = []
    
    for _ in range(runs):
        start = time.perf_counter()
        users = load_users(file_path)
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    
    return {
        "file": file_path.name,
        "records": len(users),
        "avg_time_ms": avg_time * 1000,
        "time_per_record_ms": (avg_time * 1000) / len(users) if users else 0
    }


if __name__ == "__main__":
    # Demo usage
    print("\n[UQAP] Data Parser Demo\n")
    
    data_dir = Path(__file__).parent.parent / "data"
    csv_file = data_dir / "test_users.csv"
    
    if csv_file.exists():
        print(f"Loading users from {csv_file.name}...")
        users = load_users_csv(csv_file)
        
        print(f"✓ Loaded {len(users)} users\n")
        
        for user in users:
            print(f"  {user}")
        
        # Benchmark
        print(f"\n[Performance Metrics]")
        metrics = benchmark_parsing(csv_file)
        print(f"  Parse time: {metrics['avg_time_ms']:.2f}ms")
        print(f"  Per record: {metrics['time_per_record_ms']:.4f}ms")
    else:
        print(f"Error: {csv_file} not found. Run setup_lesson.py first.")
