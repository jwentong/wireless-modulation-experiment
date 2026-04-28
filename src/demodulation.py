import numpy as np

def bpsk_demodulate(symbols):
    """
    BPSK 解调
    判决准则：real(symbol) > 0 → 比特0，否则 → 比特1
    """
    bits = (np.real(symbols) < 0).astype(int)
    return bits

def qpsk_demodulate(symbols):
    """
    QPSK 解调 - 最小欧氏距离判决
    """
    constellation = np.array([
        (1 + 1j) / np.sqrt(2),   # 00
        (-1 + 1j) / np.sqrt(2),  # 01
        (-1 - 1j) / np.sqrt(2),  # 11
        (1 - 1j) / np.sqrt(2),   # 10
    ])
    mapping = [(0,0), (0,1), (1,1), (1,0)]
    
    bits = []
    for s in symbols:
        idx = np.argmin(np.abs(s - constellation))
        bits.extend(mapping[idx])
    return np.array(bits)

def qam16_demodulate(symbols):
    """
    16-QAM 解调 - 最小欧氏距离判决
    """
    gray_map = {(0,0): 1, (0,1): 3, (1,1): -3, (1,0): -1}
    inv_gray = {v: k for k, v in gray_map.items()}
    levels = np.array([-3, -1, 1, 3]) / np.sqrt(10)
    
    bits = []
    for s in symbols:
        I_idx = np.argmin(np.abs(np.real(s) - levels))
        Q_idx = np.argmin(np.abs(np.imag(s) - levels))
        I_val = int(round(np.real(s) * np.sqrt(10)))
        Q_val = int(round(np.imag(s) * np.sqrt(10)))
        I_val = min([-3,-1,1,3], key=lambda x: abs(x-I_val))
        Q_val = min([-3,-1,1,3], key=lambda x: abs(x-Q_val))
        bits.extend(inv_gray[I_val])
        bits.extend(inv_gray[Q_val])
    return np.array(bits)

def calculate_ber(tx_bits, rx_bits):
    """计算误码率"""
    errors = np.sum(tx_bits != rx_bits)
    ber = errors / len(tx_bits)
    return ber
