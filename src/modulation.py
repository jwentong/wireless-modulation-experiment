"""Digital modulation functions for BPSK, QPSK, and 16-QAM."""

import numpy as np
from utils import plot_constellation


def _as_binary_array(bits):
    """Return bits as a flat integer NumPy array and validate 0/1 values."""
    bits = np.asarray(bits, dtype=int).ravel()
    if np.any((bits != 0) & (bits != 1)):
        raise ValueError("bits must contain only 0 and 1")
    return bits


def bpsk_modulate(bits):
    """
    BPSK modulation.

    Mapping:
        0 -> +1
        1 -> -1
    """
    bits = _as_binary_array(bits)
    return (1 - 2 * bits).astype(complex)


def qpsk_modulate(bits):
    """
    QPSK modulation with Gray-code mapping.

    Mapping:
        00 -> ( 1 + 1j) / sqrt(2)
        01 -> (-1 + 1j) / sqrt(2)
        11 -> (-1 - 1j) / sqrt(2)
        10 -> ( 1 - 1j) / sqrt(2)
    """
    bits = _as_binary_array(bits)
    if len(bits) % 2 != 0:
        raise ValueError("QPSK requires an even number of bits")

    bit_pairs = bits.reshape(-1, 2)
    i_values = np.where(bit_pairs[:, 1] == 0, 1, -1)
    q_values = np.where(bit_pairs[:, 0] == 0, 1, -1)
    return (i_values + 1j * q_values).astype(complex) / np.sqrt(2)


def qam16_modulate(bits):
    """
    16-QAM modulation with Gray-code mapping and unit average power.

    For both I and Q components:
        00 -> +3
        01 -> +1
        11 -> -1
        10 -> -3
    """
    bits = _as_binary_array(bits)
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM requires the number of bits to be a multiple of 4")

    bit_groups = bits.reshape(-1, 4)

    def component_levels(two_bit_groups):
        first = two_bit_groups[:, 0]
        second = two_bit_groups[:, 1]
        return np.where(first == 0, 3 - 2 * second, -3 + 2 * second)

    i_values = component_levels(bit_groups[:, :2])
    q_values = component_levels(bit_groups[:, 2:])
    return (i_values + 1j * q_values).astype(complex) / np.sqrt(10)


def test_modulation():
    """Run a small smoke test and generate constellation figures."""
    print("=" * 50)
    print("Digital modulation test")
    print("=" * 50)

    bits_bpsk = np.random.randint(0, 2, 1000)
    symbols_bpsk = bpsk_modulate(bits_bpsk)
    print(f"BPSK: {len(bits_bpsk)} bits -> {len(symbols_bpsk)} symbols")
    plot_constellation(symbols_bpsk[:100], "BPSK Constellation", "bpsk_constellation.png")

    bits_qpsk = np.random.randint(0, 2, 1000)
    symbols_qpsk = qpsk_modulate(bits_qpsk)
    print(f"QPSK: {len(bits_qpsk)} bits -> {len(symbols_qpsk)} symbols")
    plot_constellation(symbols_qpsk[:200], "QPSK Constellation", "qpsk_constellation.png")

    bits_qam = np.random.randint(0, 2, 1000)
    symbols_qam = qam16_modulate(bits_qam)
    print(f"16-QAM: {len(bits_qam)} bits -> {len(symbols_qam)} symbols")
    plot_constellation(symbols_qam[:250], "16-QAM Constellation", "16qam_constellation.png")

    print("=" * 50)
    print("Done. Figures are saved in the results directory.")


if __name__ == "__main__":
    test_modulation()
