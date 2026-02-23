
"""
Visual Regression Comparator
Provides pixel-perfect screenshot comparison with tolerance and diff generation.
"""

import shutil
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont


@dataclass
class ComparisonResult:
    """Result of a visual regression comparison."""
    passed: bool
    diff_percentage: float
    diff_image_path: Path | None
    message: str
    baseline_path: Path | None = None
    current_path: Path | None = None


class VisualRegression:
    """
    Manages visual regression testing with baseline management and pixel comparison.

    Attributes:
        baseline_dir: Directory to store baseline screenshots
        threshold: Maximum allowed difference percentage (0.1 = 0.1%)
    """

    def __init__(self, baseline_dir: Path, threshold: float = 0.1):
        self.baseline_dir = Path(baseline_dir)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.threshold = threshold

    def compare(
        self,
        test_name: str,
        current_screenshot: Path,
        diff_dir: Path | None = None
    ) -> ComparisonResult:
        """
        Compare current screenshot against baseline.

        Args:
            test_name: Unique identifier for this test (used in baseline filename)
            current_screenshot: Path to the current screenshot
            diff_dir: Directory to save diff images (optional)

        Returns:
            ComparisonResult with pass/fail status and diff details
        """
        baseline_path = self.baseline_dir / f"{test_name}.png"

        # First run: Create baseline
        if not baseline_path.exists():
            shutil.copy(current_screenshot, baseline_path)
            return ComparisonResult(
                passed=True,
                diff_percentage=0.0,
                diff_image_path=None,
                message=f"✓ Baseline created: {baseline_path}",
                baseline_path=baseline_path,
                current_path=current_screenshot
            )

        # Subsequent runs: Perform pixel comparison
        diff_pct = self._calculate_pixel_difference(baseline_path, current_screenshot)

        if diff_pct <= self.threshold:
            return ComparisonResult(
                passed=True,
                diff_percentage=diff_pct,
                diff_image_path=None,
                message=f"✓ Visual regression check passed ({diff_pct:.4f}% diff)",
                baseline_path=baseline_path,
                current_path=current_screenshot
            )
        else:
            # Generate visual diff
            diff_path = None
            if diff_dir:
                diff_dir = Path(diff_dir)
                diff_dir.mkdir(parents=True, exist_ok=True)
                diff_path = diff_dir / f"{test_name}_diff.png"
                self._generate_diff_image(baseline_path, current_screenshot, diff_path)

            return ComparisonResult(
                passed=False,
                diff_percentage=diff_pct,
                diff_image_path=diff_path,
                message=f"✗ Visual regression check failed ({diff_pct:.4f}% diff exceeds {self.threshold}% threshold)",
                baseline_path=baseline_path,
                current_path=current_screenshot
            )

    def _calculate_pixel_difference(self, baseline_path: Path, current_path: Path) -> float:
        """
        Calculate percentage of pixels that differ between two images.

        Uses PIL ImageChops.difference to compute per-pixel RGB differences,
        then calculates the percentage of total pixel values that changed.
        """
        baseline = Image.open(baseline_path).convert("RGB")
        current = Image.open(current_path).convert("RGB")

        # Ensure same dimensions
        if baseline.size != current.size:
            raise ValueError(
                f"Image dimensions don't match: baseline={baseline.size}, current={current.size}"
            )

        # Compute pixel-by-pixel difference
        diff = ImageChops.difference(baseline, current)

        # Calculate difference magnitude
        # Each pixel has 3 channels (RGB), each ranging 0-255
        # Use get_flattened_data (getdata is deprecated in Pillow 14+)
        flat = list(diff.get_flattened_data())
        total_diff = sum(sum(p) for p in flat) if flat and isinstance(flat[0], (tuple, list)) else sum(flat)

        # Total possible difference: width * height * 3 channels * 255 max value
        width, height = baseline.size
        max_diff = width * height * 3 * 255

        # Percentage difference
        diff_percentage = (total_diff / max_diff) * 100

        return diff_percentage

    def _generate_diff_image(self, baseline_path: Path, current_path: Path, output_path: Path):
        """
        Generate a visual diff image highlighting changed pixels.

        Changed pixels are amplified and colorized for easy visual identification.
        """
        baseline = Image.open(baseline_path).convert("RGB")
        current = Image.open(current_path).convert("RGB")

        # Compute difference
        diff = ImageChops.difference(baseline, current)

        # Amplify differences for visibility (multiply by 10, cap at 255)
        diff_enhanced = diff.point(lambda p: min(p * 10, 255))

        # Create side-by-side comparison
        width, height = baseline.size
        comparison = Image.new("RGB", (width * 3, height + 40), color=(255, 255, 255))

        # Paste images
        comparison.paste(baseline, (0, 40))
        comparison.paste(current, (width, 40))
        comparison.paste(diff_enhanced, (width * 2, 40))

        # Add labels
        draw = ImageDraw.Draw(comparison)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            font = ImageFont.load_default()

        draw.text((10, 10), "BASELINE", fill=(0, 0, 0), font=font)
        draw.text((width + 10, 10), "CURRENT", fill=(0, 0, 0), font=font)
        draw.text((width * 2 + 10, 10), "DIFF (10x)", fill=(255, 0, 0), font=font)

        comparison.save(output_path)
