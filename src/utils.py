"""
Utility helpers for plotting and simple communication experiments.
"""

import os

import numpy as np
from PIL import Image, ImageDraw


def setup_chinese_font():
    """
    Configure Matplotlib fonts so Chinese labels render when available.
    """
    try:
        import matplotlib.pyplot as plt

        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
        plt.rcParams["axes.unicode_minus"] = False
    except Exception:
        print("Warning: unable to configure Chinese fonts for Matplotlib.")


def plot_constellation(symbols, title, filename, show_grid=True):
    """
    Plot a constellation diagram and save it into the results directory.
    """
    os.makedirs("results", exist_ok=True)

    symbols = np.asarray(symbols)
    real_parts = np.real(symbols)
    imag_parts = np.imag(symbols)
    filepath = os.path.join("results", filename)

    _plot_constellation_with_pillow(real_parts, imag_parts, title, filepath, show_grid)
    print(f"Saved constellation plot to: {filepath}")


def _plot_constellation_with_pillow(real_parts, imag_parts, title, filepath, show_grid):
    """
    Lightweight fallback renderer used when Matplotlib cannot be imported.
    """
    width = 900
    height = 900
    margin = 90
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    max_component = max(np.max(np.abs(real_parts)), np.max(np.abs(imag_parts)), 1.0)
    limit = max_component * 1.2
    plot_size = min(width, height) - 2 * margin

    def map_x(value):
        return margin + (value + limit) / (2 * limit) * plot_size

    def map_y(value):
        return height - (margin + (value + limit) / (2 * limit) * plot_size)

    if show_grid:
        for fraction in np.linspace(-1, 1, 5):
            x = map_x(fraction * limit)
            y = map_y(fraction * limit)
            draw.line((x, margin, x, height - margin), fill=(220, 220, 220), width=1)
            draw.line((margin, y, width - margin, y), fill=(220, 220, 220), width=1)

    draw.rectangle((margin, margin, width - margin, height - margin), outline="black", width=2)
    draw.line((map_x(0), margin, map_x(0), height - margin), fill="black", width=2)
    draw.line((margin, map_y(0), width - margin, map_y(0)), fill="black", width=2)

    for real_value, imag_value in zip(real_parts, imag_parts):
        x = map_x(real_value)
        y = map_y(imag_value)
        radius = 8
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(0, 102, 204), outline="black")

    draw.text((margin, 20), title, fill="black")
    draw.text((width // 2 - 35, height - 40), "In-phase", fill="black")
    draw.text((20, height // 2 - 10), "Quadrature", fill="black")
    image.save(filepath)


def add_awgn(signal, snr_db):
    """
    Add complex AWGN to a signal for a given SNR in dB.
    """
    signal = np.asarray(signal)
    signal_power = np.mean(np.abs(signal) ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear

    noise_real = np.random.normal(0, np.sqrt(noise_power / 2), signal.shape)
    noise_imag = np.random.normal(0, np.sqrt(noise_power / 2), signal.shape)
    noise = noise_real + 1j * noise_imag
    return signal + noise


def calculate_ber(bits_tx, bits_rx):
    """
    Calculate bit error rate.
    """
    bits_tx = np.asarray(bits_tx)
    bits_rx = np.asarray(bits_rx)
    if len(bits_tx) != len(bits_rx):
        raise ValueError("Transmitted and received bit sequences must have the same length.")

    errors = np.sum(bits_tx != bits_rx)
    return errors / len(bits_tx)


def plot_ber_curve(snr_range, ber_values, title="BER vs SNR", filename="ber_curve.png"):
    """
    Plot and save a BER curve.
    """
    os.makedirs("results", exist_ok=True)

    filepath = os.path.join("results", filename)

    width = 1000
    height = 600
    margin = 80
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((margin, margin, width - margin, height - margin), outline="black", width=2)
    draw.text((margin, 20), title, fill="black")

    snr_range = np.asarray(snr_range, dtype=float)
    ber_values = np.asarray(ber_values, dtype=float)
    ber_values = np.maximum(ber_values, 1e-6)

    x_min = float(np.min(snr_range))
    x_max = float(np.max(snr_range))
    y_min = -6.0
    y_max = 0.0

    def map_x(value):
        if x_max == x_min:
            return width / 2
        return margin + (value - x_min) / (x_max - x_min) * (width - 2 * margin)

    def map_y(value):
        log_value = np.log10(value)
        return height - margin - (log_value - y_min) / (y_max - y_min) * (height - 2 * margin)

    points = [(map_x(x), map_y(y)) for x, y in zip(snr_range, ber_values)]
    for point in points:
        x, y = point
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(0, 102, 204), outline="black")
    for start, end in zip(points[:-1], points[1:]):
        draw.line((start[0], start[1], end[0], end[1]), fill=(0, 102, 204), width=3)

    draw.text((width // 2 - 30, height - 40), "SNR (dB)", fill="black")
    draw.text((20, height // 2 - 10), "log10(BER)", fill="black")
    image.save(filepath)

    print(f"Saved BER curve to: {filepath}")


def generate_random_bits(n):
    """
    Generate a random binary sequence of length n.
    """
    return np.random.randint(0, 2, n)


if __name__ == "__main__":
    print("Utility module self-test...")
    bits = generate_random_bits(100)
    print(f"Generated {len(bits)} random bits")
    test_symbols = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j]) / np.sqrt(2)
    plot_constellation(test_symbols, "Test Constellation", "test_constellation.png")
    print("Utility module self-test completed")
