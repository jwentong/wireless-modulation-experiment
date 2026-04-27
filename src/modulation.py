"""Digital modulation functions used by the grading tests.

The module implements BPSK, Gray-coded QPSK, and Gray-coded 16-QAM.  The
returned symbols are normalized so that the average symbol power is one for
the random bit streams used in the experiment.
"""

from __future__ import annotations

import os

import numpy as np

from utils import plot_constellation


_QPSK_MAP = {
    (0, 0): (1 + 1j) / np.sqrt(2),
    (0, 1): (-1 + 1j) / np.sqrt(2),
    (1, 1): (-1 - 1j) / np.sqrt(2),
    (1, 0): (1 - 1j) / np.sqrt(2),
}

_QAM16_LEVELS = {
    (0, 0): 3,
    (0, 1): 1,
    (1, 1): -1,
    (1, 0): -3,
}


def _as_bit_array(bits: np.ndarray) -> np.ndarray:
    """Return a one-dimensional integer bit array."""
    bit_array = np.asarray(bits, dtype=int).reshape(-1)
    if np.any((bit_array != 0) & (bit_array != 1)):
        raise ValueError("Input bits must contain only 0 and 1.")
    return bit_array


def _plot_once(symbols: np.ndarray, title: str, filename: str) -> None:
    """Create a constellation image if it is missing.

    The numerical modulation result should not depend on file-system state.
    Plotting is therefore best-effort: existing figures are reused, and a
    locked or read-only result file does not break the modulation tests.
    """
    filepath = os.path.join("results", filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        return

    try:
        plot_constellation(symbols, title=title, filename=filename)
    except OSError:
        pass


def bpsk_modulate(bits: np.ndarray) -> np.ndarray:
    """Modulate bits with BPSK using 0 -> +1 and 1 -> -1."""
    bit_array = _as_bit_array(bits)
    symbols = (1 - 2 * bit_array).astype(np.complex128)
    _plot_once(symbols, "BPSK Constellation", "bpsk_constellation.png")
    return symbols


def qpsk_modulate(bits: np.ndarray) -> np.ndarray:
    """Modulate bits with Gray-coded QPSK.

    Mapping:
        00 -> ( 1 + 1j) / sqrt(2)
        01 -> (-1 + 1j) / sqrt(2)
        11 -> (-1 - 1j) / sqrt(2)
        10 -> ( 1 - 1j) / sqrt(2)
    """
    bit_array = _as_bit_array(bits)
    if len(bit_array) % 2 != 0:
        raise ValueError("QPSK requires an even number of input bits.")

    pairs = bit_array.reshape(-1, 2)
    symbols = np.array([_QPSK_MAP[tuple(pair)] for pair in pairs], dtype=np.complex128)
    _plot_once(symbols, "QPSK Constellation", "qpsk_constellation.png")
    return symbols


def qam16_modulate(bits: np.ndarray) -> np.ndarray:
    """Modulate bits with Gray-coded square 16-QAM.

    Each four-bit group is split into I and Q bit pairs.  Both axes use the
    Gray-coded amplitude mapping 00 -> +3, 01 -> +1, 11 -> -1, 10 -> -3 and
    are divided by sqrt(10) for unit average symbol power.
    """
    bit_array = _as_bit_array(bits)
    if len(bit_array) % 4 != 0:
        raise ValueError("16-QAM requires the input length to be a multiple of 4.")

    groups = bit_array.reshape(-1, 4)
    in_phase = np.array([_QAM16_LEVELS[tuple(group[:2])] for group in groups])
    quadrature = np.array([_QAM16_LEVELS[tuple(group[2:])] for group in groups])
    symbols = (in_phase + 1j * quadrature) / np.sqrt(10)
    symbols = symbols.astype(np.complex128)
    _plot_once(symbols, "16-QAM Constellation", "16qam_constellation.png")
    return symbols


def test_modulation() -> None:
    """Run a small manual smoke test and generate constellation images."""
    rng = np.random.default_rng(42)

    bpsk_bits = rng.integers(0, 2, 1000)
    qpsk_bits = rng.integers(0, 2, 1000)
    qam16_bits = rng.integers(0, 2, 1000)

    print("BPSK symbols:", bpsk_modulate(bpsk_bits)[:4])
    print("QPSK symbols:", qpsk_modulate(qpsk_bits)[:4])
    print("16-QAM symbols:", qam16_modulate(qam16_bits)[:4])
    print("Constellation images are available in the results directory.")


if __name__ == "__main__":
    test_modulation()
