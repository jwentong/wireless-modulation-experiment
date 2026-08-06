"""
Digital demodulation helpers for the lab exercises.
"""

import numpy as np


def bpsk_demodulate(symbols):
    """
    Recover BPSK bits using a zero-threshold decision on the real axis.
    """
    symbols = np.asarray(symbols, dtype=np.complex128)
    return (np.real(symbols) <= 0).astype(int)


def qpsk_demodulate(symbols):
    """
    Recover QPSK bits using minimum Euclidean distance detection.
    """
    symbols = np.asarray(symbols, dtype=np.complex128)
    reference_symbols = np.array(
        [
            (1 + 1j) / np.sqrt(2),
            (-1 + 1j) / np.sqrt(2),
            (-1 - 1j) / np.sqrt(2),
            (1 - 1j) / np.sqrt(2),
        ],
        dtype=np.complex128,
    )
    reference_bits = np.array(
        [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 0],
        ],
        dtype=int,
    )

    distances = np.abs(symbols[:, None] - reference_symbols[None, :]) ** 2
    nearest_indices = np.argmin(distances, axis=1)
    return reference_bits[nearest_indices].reshape(-1)


def qam16_demodulate(symbols):
    """
    Recover 16-QAM bits using Gray-coded I/Q slicing.
    """
    symbols = np.asarray(symbols, dtype=np.complex128)
    scaled_real = np.real(symbols) * np.sqrt(10)
    scaled_imag = np.imag(symbols) * np.sqrt(10)

    def slice_component(values):
        bits = np.zeros((len(values), 2), dtype=int)
        bits[values < -2] = [1, 0]
        bits[(values >= -2) & (values < 0)] = [1, 1]
        bits[(values >= 0) & (values < 2)] = [0, 1]
        bits[values >= 2] = [0, 0]
        return bits

    i_bits = slice_component(scaled_real)
    q_bits = slice_component(scaled_imag)
    return np.hstack((i_bits, q_bits)).reshape(-1)


def test_demodulation():
    """
    Run a simple smoke test for the three demodulators.
    """
    from modulation import bpsk_modulate, qam16_modulate, qpsk_modulate
    from utils import add_awgn, calculate_ber

    print("=" * 50)
    print("Demodulation test")
    print("=" * 50)

    print("\n1. Testing BPSK demodulation...")
    bits_tx = np.random.randint(0, 2, 100)
    symbols_rx = add_awgn(bpsk_modulate(bits_tx), snr_db=10)
    bits_rx = bpsk_demodulate(symbols_rx)
    print(f"   BER = {calculate_ber(bits_tx, bits_rx):.4f} (SNR=10 dB)")

    print("\n2. Testing QPSK demodulation...")
    bits_tx = np.random.randint(0, 2, 100)
    symbols_rx = add_awgn(qpsk_modulate(bits_tx), snr_db=10)
    bits_rx = qpsk_demodulate(symbols_rx)
    print(f"   BER = {calculate_ber(bits_tx, bits_rx):.4f} (SNR=10 dB)")

    print("\n3. Testing 16-QAM demodulation...")
    bits_tx = np.random.randint(0, 2, 100)
    if len(bits_tx) % 4 != 0:
        bits_tx = bits_tx[: len(bits_tx) - (len(bits_tx) % 4)]
    symbols_rx = add_awgn(qam16_modulate(bits_tx), snr_db=15)
    bits_rx = qam16_demodulate(symbols_rx)
    print(f"   BER = {calculate_ber(bits_tx, bits_rx):.4f} (SNR=15 dB)")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    test_demodulation()
