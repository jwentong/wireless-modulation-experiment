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
    
    # TODO：BPSK解调实现
    # 提示：使用np.real()获取实部，然后判断正负
    # BPSK只需看实部符号：实部>0判0，否则判1
    symbols = np.asarray(symbols)
    real_part = np.real(symbols)
    bits = np.where(real_part > 0, 0, 1).astype(np.int8)
    return bits


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
    constellation = {
        0: (1 + 1j) / np.sqrt(2),    # 00
        1: (-1 + 1j) / np.sqrt(2),   # 01
        3: (-1 - 1j) / np.sqrt(2),   # 11
        2: (1 - 1j) / np.sqrt(2)     # 10
    }
    
    # TODO: 实现QPSK解调
    # 提示步骤：
    # 1. 对每个接收符号，计算到4个参考点的欧氏距离
    # 2. 找到距离最小的参考点
    # 3. 将参考点的索引转换为2个比特
    # 统一为复数数组，后续做距离判决
    symbols = np.asarray(symbols, dtype=np.complex128)

    # 索引到比特对的映射：0->00, 1->01, 3->11, 2->10
    idx_to_bits = {
        0: (0, 0),
        1: (0, 1),
        3: (1, 1),
        2: (1, 0),
    }

    # 参考点与索引保持同序，便于最近点回查比特
    ref_indices = np.array(list(constellation.keys()))
    ref_points = np.array(list(constellation.values()), dtype=np.complex128)

    bits_out = []
    for sym in symbols:
        # 最小欧氏距离判决
        distances = np.abs(sym - ref_points) ** 2
        nearest_idx = ref_indices[np.argmin(distances)]
        bits_out.extend(idx_to_bits[int(nearest_idx)])

    return np.array(bits_out, dtype=np.int8)


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
    
    # TODO: 实现16-QAM解调
    # 提示：可以采用两种方法
    # 方法1：遍历16个参考点，找最小距离（简单但慢）
    # 方法2：分别判决I路和Q路（快速且实用）
    # 分别对I/Q分量做分段判决，等价于二维最近点判决
    symbols = np.asarray(symbols, dtype=np.complex128)
    threshold = 2 / np.sqrt(10)

    def level_to_bits(x):
        # 与调制端格雷码一致：+3,+1,-1,-3 对应 00,01,11,10
        if x > threshold:
            return (0, 0)
        if x > 0:
            return (0, 1)
        if x >= -threshold:
            return (1, 1)
        return (1, 0)

    bits_out = []
    for sym in symbols:
        i_bits = level_to_bits(np.real(sym))
        q_bits = level_to_bits(np.imag(sym))
        bits_out.extend(i_bits)
        bits_out.extend(q_bits)

    return np.array(bits_out, dtype=np.int8)


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
