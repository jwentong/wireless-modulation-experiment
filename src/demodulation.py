"""
数字解调模块
实现BPSK、QPSK、16-QAM解调算法（选做）
"""

import numpy as np


def bpsk_demodulate(symbols):
    # 实部 > 0 -> 比特 0, 实部 <= 0 -> 比特 1
    return (np.real(symbols) <= 0).astype(int)

def qpsk_demodulate(symbols):
    I = np.real(symbols)
    Q = np.imag(symbols)
    
    # 逆向映射：实部I决定b1，虚部Q决定b0
    b1 = (I <= 0).astype(int)
    b0 = (Q <= 0).astype(int)
    
    # 组合成 (N, 2) 形状并展平为一维数组
    return np.stack((b0, b1), axis=1).flatten()

def qam16_demodulate(symbols):
    # 恢复幅度
    I = np.real(symbols) * np.sqrt(10)
    Q = np.imag(symbols) * np.sqrt(10)
    
    # I 分量判决前两比特 (b0, b1)
    b0 = (I <= 0).astype(int)
    b1 = (np.abs(I) <= 2).astype(int)
    
    # Q 分量判决后两比特 (b2, b3)
    b2 = (Q <= 0).astype(int)
    b3 = (np.abs(Q) <= 2).astype(int)
    
    # 组合成 (N, 4) 形状并展平
    return np.stack((b0, b1, b2, b3), axis=1).flatten()
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
