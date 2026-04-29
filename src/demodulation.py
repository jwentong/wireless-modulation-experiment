"""Digital demodulation functions for BPSK, QPSK, and 16-QAM."""

import numpy as np


def bpsk_demodulate(symbols):
    """
    BPSK hard-decision demodulation.

    Decision rule:
        real(symbol) > 0 -> 0
        real(symbol) <= 0 -> 1
    """
    symbols = np.asarray(symbols, dtype=complex).ravel()
    return np.where(np.real(symbols) > 0, 0, 1).astype(int)


def qpsk_demodulate(symbols):
    """
    QPSK hard-decision demodulation for the Gray-code mapping in modulation.py.
    """
    symbols = np.asarray(symbols, dtype=complex).ravel()
    constellation = np.array(
        [
            (1 + 1j) / np.sqrt(2),
            (-1 + 1j) / np.sqrt(2),
            (-1 - 1j) / np.sqrt(2),
            (1 - 1j) / np.sqrt(2),
        ],
        dtype=complex,
    )
    bit_pairs = np.array(
        [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 0],
        ],
        dtype=int,
    )

    distances = np.abs(symbols[:, np.newaxis] - constellation[np.newaxis, :])
    nearest = np.argmin(distances, axis=1)
    return bit_pairs[nearest].reshape(-1)


def qam16_demodulate(symbols):
    """
    16-QAM hard-decision demodulation for the Gray-code mapping in modulation.py.
    """
    symbols = np.asarray(symbols, dtype=complex).ravel()
    levels = np.array([-3, -1, 1, 3], dtype=float) / np.sqrt(10)
    level_bits = np.array(
        [
            [1, 0],
            [1, 1],
            [0, 1],
            [0, 0],
        ],
        dtype=int,
    )

    def demod_component(values):
        distances = np.abs(values[:, np.newaxis] - levels[np.newaxis, :])
        nearest = np.argmin(distances, axis=1)
        return level_bits[nearest]

    i_bits = demod_component(np.real(symbols))
    q_bits = demod_component(np.imag(symbols))
    return np.hstack((i_bits, q_bits)).reshape(-1)


def test_demodulation():
    """Run a small modulation/demodulation smoke test."""
    from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
    from utils import add_awgn, calculate_ber

    print("=" * 50)
    print("Digital demodulation test")
    print("=" * 50)

    test_cases = [
        ("BPSK", bpsk_modulate, bpsk_demodulate, 1000, 10),
        ("QPSK", qpsk_modulate, qpsk_demodulate, 1000, 10),
        ("16-QAM", qam16_modulate, qam16_demodulate, 1000, 15),
    ]

    for name, modulate, demodulate, num_bits, snr_db in test_cases:
        bits_tx = np.random.randint(0, 2, num_bits)
        symbols_tx = modulate(bits_tx)
        symbols_rx = add_awgn(symbols_tx, snr_db=snr_db)
        bits_rx = demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"{name}: SNR={snr_db} dB, BER={ber:.6f}")


if __name__ == "__main__":
    test_demodulation()
