"""
Digital modulation helpers for the lab exercises.
"""

import numpy as np

from utils import plot_constellation


def bpsk_modulate(bits):
    """
    Map binary bits to BPSK symbols.

    0 -> +1
    1 -> -1
    """
    bits = np.asarray(bits, dtype=int)
    symbols = (1 - 2 * bits).astype(np.complex128)
    return symbols


def qpsk_modulate(bits):
    """
    Map bits to Gray-coded QPSK symbols with unit average power.
    """
    bits = np.asarray(bits, dtype=int)
    if len(bits) % 2 != 0:
        raise ValueError("QPSK requires an even number of bits.")

    bit_pairs = bits.reshape(-1, 2)
    gray_map = {
        (0, 0): 1 + 1j,
        (0, 1): -1 + 1j,
        (1, 1): -1 - 1j,
        (1, 0): 1 - 1j,
    }
    symbols = np.array([gray_map[tuple(pair)] for pair in bit_pairs], dtype=np.complex128)
    return symbols / np.sqrt(2)


def qam16_modulate(bits):
    """
    Map bits to Gray-coded 16-QAM symbols with unit average power.
    """
    bits = np.asarray(bits, dtype=int)
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM requires the number of bits to be a multiple of 4.")

    bit_groups = bits.reshape(-1, 4)
    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3,
    }

    i_values = np.array([gray_map[tuple(group[:2])] for group in bit_groups], dtype=float)
    q_values = np.array([gray_map[tuple(group[2:])] for group in bit_groups], dtype=float)
    symbols = i_values + 1j * q_values
    return symbols / np.sqrt(10)


def test_modulation():
    """
    Generate example constellation plots for all modulation schemes.
    """
    print("=" * 50)
    print("Digital modulation test")
    print("=" * 50)

    print("\n1. Testing BPSK...")
    bits_bpsk = np.random.randint(0, 2, 1000)
    symbols_bpsk = bpsk_modulate(bits_bpsk)
    print(f"   Input bits: {len(bits_bpsk)}")
    print(f"   Output symbols: {len(symbols_bpsk)}")
    print(f"   Unique symbols: {np.unique(symbols_bpsk)}")
    plot_constellation(symbols_bpsk[:100], "BPSK Constellation", "bpsk_constellation.png")
    print("   BPSK test passed")

    print("\n2. Testing QPSK...")
    bits_qpsk = np.random.randint(0, 2, 1000)
    symbols_qpsk = qpsk_modulate(bits_qpsk)
    print(f"   Input bits: {len(bits_qpsk)}")
    print(f"   Output symbols: {len(symbols_qpsk)}")
    print(f"   Symbol magnitudes: {np.abs(symbols_qpsk[:4])}")
    plot_constellation(symbols_qpsk[:200], "QPSK Constellation", "qpsk_constellation.png")
    print("   QPSK test passed")

    print("\n3. Testing 16-QAM...")
    bits_qam = np.random.randint(0, 2, 1000)
    symbols_qam = qam16_modulate(bits_qam)
    print(f"   Input bits: {len(bits_qam)}")
    print(f"   Output symbols: {len(symbols_qam)}")
    print(f"   Unique symbols: {len(np.unique(symbols_qam))}")
    plot_constellation(symbols_qam[:250], "16-QAM Constellation", "16qam_constellation.png")
    print("   16-QAM test passed")

    print("\n" + "=" * 50)
    print("Finished. Check the plots in the results directory.")
    print("=" * 50)


if __name__ == "__main__":
    test_modulation()
