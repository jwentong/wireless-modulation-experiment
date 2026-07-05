"""
数字解调模块
实现BPSK、QPSK、16-QAM解调算法（选做）
"""

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
    
    参数:
        symbols: 接收到的复数符号数组
    
    返回:
        bits: 恢复的比特数组
    
    提示：
    - BPSK符号主要在实轴上
    - 只需要判断实部的正负即可
    - 噪声会使符号偏离理想位置，但判决准则仍然有效
    
    示例：
        >>> symbols = np.array([0.9+0.1j, -1.1-0.05j, 0.85+0.2j])
        >>> bits = bpsk_demodulate(symbols)
        >>> print(bits)
        [0 1 0]
    """
    
    return (np.real(symbols) < 0).astype(int)


def qpsk_demodulate(symbols):
    """
    QPSK解调
    
    任务要求：
    - 输入：接收到的复数符号序列
    - 输出：恢复的比特序列（长度是符号数的2倍）
    - 使用最小欧氏距离判决
    
    参数:
        symbols: 接收到的复数符号数组
    
    返回:
        bits: 恢复的比特数组
    
    提示：
    - QPSK有4个参考星座点（理想位置）
    - 对每个接收符号，计算它到4个参考点的距离
    - 选择距离最小的那个点，输出对应的比特对
    - 参考点（格雷码）：
        (1+1j)/√2 → 00
        (-1+1j)/√2 → 01
        (-1-1j)/√2 → 11
        (1-1j)/√2 → 10
    
    示例：
        >>> symbols = np.array([0.6+0.6j, -0.7+0.8j])
        >>> bits = qpsk_demodulate(symbols)
        >>> print(bits)  # 应该是 [0, 0, 0, 1]
    """
    
    # 定义QPSK参考星座点（格雷码）
    ref = np.array([
        (1 + 1j) / np.sqrt(2),    # 00 → index 0
        (-1 + 1j) / np.sqrt(2),   # 01 → index 1
        (-1 - 1j) / np.sqrt(2),   # 11 → index 3
        (1 - 1j) / np.sqrt(2)     # 10 → index 2
    ])
    gray_idx = np.array([0, 1, 3, 2])  # 实际格雷码索引
    symbols = np.asarray(symbols, dtype=complex)
    bits_out = np.zeros(len(symbols) * 2, dtype=int)
    for i, s in enumerate(symbols):
        dists = np.abs(s - ref) ** 2
        nearest = gray_idx[np.argmin(dists)]
        bits_out[2 * i] = (nearest >> 1) & 1
        bits_out[2 * i + 1] = nearest & 1
    return bits_out


def qam16_demodulate(symbols):
    """
    16-QAM解调
    
    任务要求：
    - 输入：接收到的复数符号序列
    - 输出：恢复的比特序列（长度是符号数的4倍）
    - 使用最小欧氏距离判决
    
    参数:
        symbols: 接收到的复数符号数组
    
    返回:
        bits: 恢复的比特数组
    
    提示：
    - 16-QAM有16个参考星座点
    - 可以分别对I路和Q路进行判决，简化计算
    - I/Q分量的判决（格雷码）：
        > 2/√10 → 00
        0 ~ 2/√10 → 01
        -2/√10 ~ 0 → 11
        < -2/√10 → 10
    """
    
    # 分别对I路和Q路进行格雷码判决
    symbols = np.asarray(symbols, dtype=complex)
    norm = 1.0 / np.sqrt(10)
    # 判决阈值: -2, 0, +2 (乘以norm后)
    thresholds = np.array([-2, 0, 2]) * norm
    gray_bits = np.array([[1, 0], [1, 1], [0, 1], [0, 0]])  # 10,11,01,00
    bits_out = np.zeros(len(symbols) * 4, dtype=int)
    for i, s in enumerate(symbols):
        i_val = s.real
        q_val = s.imag
        i_idx = np.digitize(i_val, thresholds)  # 0-3
        q_idx = np.digitize(q_val, thresholds)
        i_idx = max(0, min(3, i_idx))
        q_idx = max(0, min(3, q_idx))
        bits_out[4 * i:4 * i + 2] = gray_bits[i_idx]
        bits_out[4 * i + 2:4 * i + 4] = gray_bits[q_idx]
    return bits_out


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
        symbols_rx = add_awgn(symbols, snr_db=10)  # 添加10dB噪声
        bits_rx = bpsk_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=10dB)")
        print("   ✅ BPSK解调测试通过")
    except NotImplementedError:
        print("   ⏸️ BPSK解调尚未实现")
    except Exception as e:
        print(f"   ❌ BPSK解调测试失败: {e}")
    
    # 测试QPSK
    print("\n2. 测试QPSK解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = qpsk_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=10)
        bits_rx = qpsk_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=10dB)")
        print("   ✅ QPSK解调测试通过")
    except NotImplementedError:
        print("   ⏸️ QPSK解调尚未实现")
    except Exception as e:
        print(f"   ❌ QPSK解调测试失败: {e}")
    
    # 测试16-QAM
    print("\n3. 测试16-QAM解调...")
    try:
        bits_tx = np.random.randint(0, 2, 100)
        symbols = qam16_modulate(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db=15)  # QAM需要更高SNR
        bits_rx = qam16_demodulate(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        print(f"   BER = {ber:.4f} (SNR=15dB)")
        print("   ✅ 16-QAM解调测试通过")
    except NotImplementedError:
        print("   ⏸️ 16-QAM解调尚未实现")
    except Exception as e:
        print(f"   ❌ 16-QAM解调测试失败: {e}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    test_demodulation()
