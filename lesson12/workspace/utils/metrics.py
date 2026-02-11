"""
metrics.py - Performance measurement utilities
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional
from functools import wraps


@dataclass
class LocatorMetric:
    """Performance metrics for a locator strategy"""
    strategy_name: str
    locator_type: str
    locator_value: str
    execution_time: float
    success: bool
    error_message: Optional[str] = None
    risk_level: str = "LOW"


@dataclass
class MetricsCollector:
    """Collects and analyzes locator performance metrics"""
    metrics: List[LocatorMetric] = field(default_factory=list)
    
    def add_metric(self, metric: LocatorMetric):
        """Add a metric to the collection"""
        self.metrics.append(metric)
    
    def get_fastest(self) -> Optional[LocatorMetric]:
        """Get the fastest successful locator"""
        successful = [m for m in self.metrics if m.success]
        return min(successful, key=lambda m: m.execution_time) if successful else None
    
    def get_slowest(self) -> Optional[LocatorMetric]:
        """Get the slowest successful locator"""
        successful = [m for m in self.metrics if m.success]
        return max(successful, key=lambda m: m.execution_time) if successful else None
    
    def generate_report(self) -> str:
        """Generate a text report of all metrics"""
        lines = ["\n" + "="*70]
        lines.append("LOCATOR STRATEGY PERFORMANCE REPORT")
        lines.append("="*70 + "\n")
        
        for i, metric in enumerate(self.metrics, 1):
            status = "✓ PASS" if metric.success else "✗ FAIL"
            risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(metric.risk_level, "⚪")
            
            lines.append(f"{i}. {metric.strategy_name}")
            lines.append(f"   Type: {metric.locator_type}")
            lines.append(f"   Value: {metric.locator_value}")
            lines.append(f"   Time: {metric.execution_time:.4f}s")
            lines.append(f"   Status: {status}")
            lines.append(f"   Risk: {risk_emoji} {metric.risk_level}")
            
            if not metric.success and metric.error_message:
                lines.append(f"   Error: {metric.error_message}")
            
            lines.append("")
        
        # Summary
        fastest = self.get_fastest()
        slowest = self.get_slowest()
        
        if fastest and slowest:
            lines.append("-" * 70)
            lines.append("SUMMARY")
            lines.append("-" * 70)
            lines.append(f"Fastest: {fastest.strategy_name} ({fastest.execution_time:.4f}s)")
            lines.append(f"Slowest: {slowest.strategy_name} ({slowest.execution_time:.4f}s)")
            lines.append(f"Speed Difference: {slowest.execution_time / fastest.execution_time:.2f}x")
        
        return "\n".join(lines)


def measure_time(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            return result, elapsed, None
        except Exception as e:
            elapsed = time.time() - start_time
            return None, elapsed, str(e)
    return wrapper
