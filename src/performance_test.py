"""BER performance tests for BPSK, QPSK, and 16-QAM."""

import os

import matplotlib.pyplot as plt
import numpy as np

from demodulation import bpsk_demodulate, qpsk_demodulate, qam16_demodulate
from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
from utils import add_awgn, calculate_ber, generate_random_bits, plot_ber_curve


SCHEMES = {
    "BPSK": (bpsk_modulate, bpsk_demodulate, 1),
    "QPSK": (qpsk_modulate, qpsk_demodulate, 2),
    "16QAM": (qam16_modulate, qam16_demodulate, 4),
}


def test_ber_performance(modulation_scheme="BPSK", num_bits=10000, snr_range=None):
    """
    Measure BER for one modulation scheme over a range of SNR values.

    Returns:
        (snr_range, ber_values)
    """
    if snr_range is None:
        snr_range = np.arange(0, 16, 2)
    snr_range = np.asarray(snr_range, dtype=float)

    scheme = modulation_scheme.upper()
    if scheme not in SCHEMES:
        raise ValueError(f"Unsupported modulation scheme: {modulation_scheme}")

    modulate, demodulate, bits_per_symbol = SCHEMES[scheme]
    valid_num_bits = (int(num_bits) // bits_per_symbol) * bits_per_symbol
    if valid_num_bits <= 0:
        raise ValueError("num_bits is too small for the selected modulation scheme")

    if valid_num_bits != num_bits:
        print(
            f"{scheme}: adjusted num_bits from {num_bits} to {valid_num_bits} "
            "to satisfy symbol grouping"
        )

    print(f"\nTesting {scheme}: {valid_num_bits} bits")
    print("-" * 40)

    ber_values = []
    for snr_db in snr_range:
        bits_tx = generate_random_bits(valid_num_bits)
        symbols_tx = modulate(bits_tx)
        symbols_rx = add_awgn(symbols_tx, snr_db)
        bits_rx = demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        ber_values.append(ber)
        print(f"SNR = {snr_db:5.1f} dB, BER = {ber:.6f}")

    return snr_range, np.asarray(ber_values)


def compare_modulations(num_bits=10000, snr_range=None):
    """Compare BER curves for BPSK, QPSK, and 16-QAM."""
    if snr_range is None:
        snr_range = np.arange(0, 16, 2)

    print("=" * 50)
    print("Digital modulation BER comparison")
    print("=" * 50)

    snr_bpsk, ber_bpsk = test_ber_performance("BPSK", num_bits, snr_range)
    snr_qpsk, ber_qpsk = test_ber_performance("QPSK", num_bits, snr_range)
    snr_qam, ber_qam = test_ber_performance("16QAM", num_bits, snr_range)

    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", "ber_comparison.png")

    plt.figure(figsize=(10, 6))
    plt.semilogy(snr_bpsk, ber_bpsk, "b-o", label="BPSK", linewidth=2)
    plt.semilogy(snr_qpsk, ber_qpsk, "r-s", label="QPSK", linewidth=2)
    plt.semilogy(snr_qam, ber_qam, "g-^", label="16-QAM", linewidth=2)
    plt.xlabel("SNR (dB)", fontsize=12)
    plt.ylabel("Bit Error Rate (BER)", fontsize=12)
    plt.title("BER Performance Comparison", fontsize=14, fontweight="bold")
    plt.legend(fontsize=11)
    plt.grid(True, which="both", alpha=0.3)
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"\nSaved BER comparison figure to {filepath}")

    plot_ber_curve(snr_bpsk, ber_bpsk, title="BPSK BER Performance", filename="bpsk_ber.png")
    plot_ber_curve(snr_qpsk, ber_qpsk, title="QPSK BER Performance", filename="qpsk_ber.png")
    plot_ber_curve(snr_qam, ber_qam, title="16-QAM BER Performance", filename="16qam_ber.png")

    return {
        "BPSK": (snr_bpsk, ber_bpsk),
        "QPSK": (snr_qpsk, ber_qpsk),
        "16QAM": (snr_qam, ber_qam),
    }


def main():
    """Run the recommended performance comparison."""
    compare_modulations()


if __name__ == "__main__":
    main()
