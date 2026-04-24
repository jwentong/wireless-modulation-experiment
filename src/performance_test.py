"""
BER performance analysis for the modulation and demodulation chain.
"""

import os

import numpy as np

from demodulation import bpsk_demodulate, qam16_demodulate, qpsk_demodulate
from modulation import bpsk_modulate, qam16_modulate, qpsk_modulate
from utils import add_awgn, calculate_ber, plot_ber_curve, generate_random_bits


def _normalize_num_bits(modulation_scheme, num_bits):
    if modulation_scheme == "QPSK":
        return num_bits - (num_bits % 2)
    if modulation_scheme == "16QAM":
        return num_bits - (num_bits % 4)
    return num_bits


def test_ber_performance(modulation_scheme="BPSK", num_bits=10000, snr_range=None):
    """
    Measure BER for a modulation scheme over a range of SNR values.
    """
    if snr_range is None:
        snr_range = np.arange(0, 16, 2)

    if modulation_scheme == "BPSK":
        modulate_func = bpsk_modulate
        demodulate_func = bpsk_demodulate
    elif modulation_scheme == "QPSK":
        modulate_func = qpsk_modulate
        demodulate_func = qpsk_demodulate
    elif modulation_scheme == "16QAM":
        modulate_func = qam16_modulate
        demodulate_func = qam16_demodulate
    else:
        raise ValueError(f"Unsupported modulation scheme: {modulation_scheme}")

    num_bits = _normalize_num_bits(modulation_scheme, num_bits)
    if num_bits <= 0:
        raise ValueError("num_bits is too small for the selected modulation scheme.")

    ber_values = []

    print(f"\nTesting {modulation_scheme} BER performance...")
    print(f"Bits: {num_bits}, SNR range: {snr_range[0]} to {snr_range[-1]} dB")
    print("-" * 40)

    for snr_db in snr_range:
        bits_tx = generate_random_bits(num_bits)
        symbols_tx = modulate_func(bits_tx)
        symbols_rx = add_awgn(symbols_tx, snr_db)
        bits_rx = demodulate_func(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        ber_values.append(ber)
        print(f"SNR = {snr_db:2d} dB, BER = {ber:.6f}")

    return np.array(snr_range), np.array(ber_values)


def _save_comparison_plot(snr_bpsk, ber_bpsk, snr_qpsk, ber_qpsk, snr_qam, ber_qam):
    """
    Save a BER comparison figure without relying on Matplotlib.
    """
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", "ber_comparison.png")

    from PIL import Image, ImageDraw

    width = 1000
    height = 650
    margin = 80
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((margin, margin, width - margin, height - margin), outline="black", width=2)
    draw.text((40, 30), "BER Comparison", fill="black")

    all_snr = np.concatenate([snr_bpsk, snr_qpsk, snr_qam]).astype(float)
    all_ber = np.concatenate([ber_bpsk, ber_qpsk, ber_qam]).astype(float)
    all_ber = np.maximum(all_ber, 1e-6)
    x_min = float(np.min(all_snr))
    x_max = float(np.max(all_snr))
    y_min = -6.0
    y_max = 0.0

    def map_x(value):
        return margin + (value - x_min) / (x_max - x_min) * (width - 2 * margin)

    def map_y(value):
        log_value = np.log10(max(float(value), 1e-6))
        return height - margin - (log_value - y_min) / (y_max - y_min) * (height - 2 * margin)

    series = [
        ("BPSK", snr_bpsk, ber_bpsk, (0, 102, 204)),
        ("QPSK", snr_qpsk, ber_qpsk, (204, 0, 0)),
        ("16-QAM", snr_qam, ber_qam, (0, 153, 0)),
    ]

    for index, (label, snr_values, ber_values, color) in enumerate(series):
        points = [(map_x(x), map_y(y)) for x, y in zip(snr_values, np.maximum(ber_values, 1e-6))]
        for start, end in zip(points[:-1], points[1:]):
            draw.line((start[0], start[1], end[0], end[1]), fill=color, width=3)
        for x, y in points:
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color, outline="black")
        legend_y = 70 + index * 30
        draw.rectangle((width - 220, legend_y, width - 200, legend_y + 20), fill=color, outline="black")
        draw.text((width - 190, legend_y), label, fill="black")

    draw.text((width // 2 - 30, height - 40), "SNR (dB)", fill="black")
    draw.text((20, height // 2 - 10), "log10(BER)", fill="black")
    image.save(filepath)

    print(f"\nSaved BER comparison plot to: {filepath}")


def compare_modulations():
    """
    Compare BER performance of BPSK, QPSK and 16-QAM.
    """
    print("=" * 50)
    print("Digital modulation BER comparison")
    print("=" * 50)

    snr_range = np.arange(0, 16, 2)

    snr_bpsk, ber_bpsk = test_ber_performance("BPSK", num_bits=10000, snr_range=snr_range)
    snr_qpsk, ber_qpsk = test_ber_performance("QPSK", num_bits=10000, snr_range=snr_range)
    snr_qam, ber_qam = test_ber_performance("16QAM", num_bits=10000, snr_range=snr_range)

    plot_ber_curve(snr_bpsk, ber_bpsk, title="BPSK BER Performance", filename="bpsk_ber.png")
    plot_ber_curve(snr_qpsk, ber_qpsk, title="QPSK BER Performance", filename="qpsk_ber.png")
    plot_ber_curve(snr_qam, ber_qam, title="16-QAM BER Performance", filename="16qam_ber.png")
    _save_comparison_plot(snr_bpsk, ber_bpsk, snr_qpsk, ber_qpsk, snr_qam, ber_qam)

    print("\nSummary:")
    print(f"  BPSK final BER @ {snr_range[-1]} dB: {ber_bpsk[-1]:.6f}")
    print(f"  QPSK final BER @ {snr_range[-1]} dB: {ber_qpsk[-1]:.6f}")
    print(f"  16-QAM final BER @ {snr_range[-1]} dB: {ber_qam[-1]:.6f}")
    print("\n" + "=" * 50)

    return {
        "BPSK": (snr_bpsk, ber_bpsk),
        "QPSK": (snr_qpsk, ber_qpsk),
        "16QAM": (snr_qam, ber_qam),
    }


def main():
    compare_modulations()


if __name__ == "__main__":
    main()
