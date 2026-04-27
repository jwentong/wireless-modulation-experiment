"""Environment smoke tests for the digital modulation experiment."""

from __future__ import annotations

import os
import sys
import tempfile


def test_python_version() -> bool:
    """Check that the Python version is new enough."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[FAIL] Python 3.8 or newer is required.")
        return False

    print("[OK] Python version is supported.")
    return True


def test_packages() -> bool:
    """Check that required packages can be imported."""
    packages = ("numpy", "scipy", "matplotlib", "pytest")
    all_ok = True

    for package in packages:
        try:
            module = __import__(package)
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {package} {version} is available.")
        except ImportError:
            print(f"[FAIL] {package} is not installed.")
            all_ok = False

    return all_ok


def test_numpy_operations() -> bool:
    """Check basic NumPy array and complex-number operations."""
    try:
        import numpy as np

        samples = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j])
        magnitudes = np.abs(samples)
        if not np.allclose(magnitudes, np.sqrt(2)):
            print("[FAIL] NumPy complex magnitude calculation is unexpected.")
            return False

        print("[OK] NumPy operations work.")
        return True
    except Exception as exc:  # pragma: no cover - diagnostic path
        print(f"[FAIL] NumPy operation test failed: {exc}")
        return False


def test_matplotlib() -> bool:
    """Check that Matplotlib can save a simple figure."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        x_values = np.array([1, -1, -1, 1, 1])
        y_values = np.array([1, 1, -1, -1, 1])

        plt.figure(figsize=(4, 4))
        plt.plot(x_values, y_values, "b-")
        plt.grid(True)
        output_path = os.path.join(tempfile.gettempdir(), "wireless_modulation_test_plot.png")
        plt.savefig(output_path)
        plt.close()

        print("[OK] Matplotlib can save figures.")
        return True
    except Exception as exc:  # pragma: no cover - diagnostic path
        print(f"[FAIL] Matplotlib test failed: {exc}")
        return False


def main() -> int:
    """Run all environment checks."""
    print("=" * 50)
    print("Digital modulation experiment - environment test")
    print("=" * 50)

    results = [
        test_python_version(),
        test_packages(),
        test_numpy_operations(),
        test_matplotlib(),
    ]

    print("=" * 50)
    if all(results):
        print("All environment checks passed.")
        return 0

    print("Some environment checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
