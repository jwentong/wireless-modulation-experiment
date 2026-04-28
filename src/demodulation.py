"""
数字解调模块
实现BPSK、QPSK、16-QAM解调算法（选做）
"""

# 强制全局UTF-8编码，根治Windows终端乱码
import sys
sys.stdout.reconfigure(encoding='utf-8')

import numpy as np


def bpsk_demodulate(symbols):
    """
    BPSK解调
    
    任务要求：
    - 输入：接收到的复数符号序列（可能带噪声）
    - 输出：恢复的比特序列
    - 判决准则：
        实部 > 0 → 比特 0
        实部 ≤ 0 → 比特 1
    """
    # 实部 > 0 → 0，否则 → 1
    bits = (np.real(symbols) <= 0).astype(int)
    return bits


def qpsk_demodulate(symbols):
    """
    QPSK解调（最小欧氏距离判决）
    """
    # 参考星座点 + 比特映射
    constellation = np.array([
        (1 + 1j) / np.sqrt(2),   # 00
        (-1 + 1j) / np.sqrt(2),  # 01
        (-1 - 1j) / np.sqrt(2),  # 11
        (1 - 1j) / np.sqrt(2)    # 10
    ])
    
    bit_map = [[0,0], [0,1], [1,1], [1,0]]
    bits = []
    
    for s in symbols:
        # 计算到4个星座点的距离
        dist = np.abs(s - constellation)
        # 找最近点
        idx = np.argmin(dist)
        # 输出对应比特
        bits.extend(bit_map[idx])
    
    return np.array(bits)


def qam16_demodulate(symbols):
    """
    16-QAM解调（I/Q 分别判决 + 格雷码）
    """
    # 去归一化
    symbols = symbols * np.sqrt(10)
    I = np.real(symbols)
    Q = np.imag(symbols)
    
    def decide(v):
        bits = np.zeros((len(v), 2), dtype=int)
        bits[v > 2] = [0,0]
        bits[(v > 0) & (v <= 2)] = [0,1]
        bits[(v > -2) & (v <= 0)] = [1,1]
        bits[v <= -2] = [1,0]
        return bits
    
    i_bits = decide(I)
    q_bits = decide(Q)
    
    bits = np.hstack([i_bits, q_bits]).flatten()
    return bits


def test_demodulation():
    """
    测试解调函数
    需要先完成调制函数才能运行
    """
    from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
    from utils import add_awgn, calculate_ber
    
    print("=" * 50)
    print("解调测试")
    print("=" * 50)
    
    # 测试BPSK
    print("\n1. 测试BPSK解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = bpsk_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=10)
        bits_rx = bpsk_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=10dB)")
        print("   BPSK解调测试通过")
    except NotImplementedError:
        print("   BPSK解调尚未实现")
    except Exception as e:
        print(f"   BPSK解调测试失败: {e}")
    
    # 测试QPSK
    print("\n2. 测试QPSK解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = qpsk_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=10)
        bits_rx = qpsk_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=10dB)")
        print("   QPSK解调测试通过")
    except NotImplementedError:
        print("   QPSK解调尚未实现")
    except Exception as e:
        print(f"   QPSK解调测试失败: {e}")
    
    # 测试16-QAM
    print("\n3. 测试16-QAM解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = qam16_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=15)
        bits_rx = qam16_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=15dB)")
        print("   16-QAM解调测试通过")
    except NotImplementedError:
        print("   16-QAM解调尚未实现")
    except Exception as e:
        print(f"   16-QAM解调测试失败: {e}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    test_demodulation()