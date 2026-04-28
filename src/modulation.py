"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""

import numpy as np
from utils import plot_constellation


def bpsk_modulate(bits):
    """
    BPSK调制函数
    将比特映射为BPSK符号
    """
    # 0 -> 1, 1 -> -1
    # 使用数学运算 1 - 2*bits 完成映射
    symbols = 1.0 - 2.0 * bits
    return symbols + 0j  # 统一返回复数类型

def qpsk_modulate(bits):
    """
    QPSK调制函数
    将比特序列映射为QPSK符号
    """
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")

    bits_reshaped = bits.reshape(-1, 2)
    # 格雷码映射规则分析：
    # b0 b1 -> I Q
    # 0  0  ->  1  1
    # 0  1  -> -1  1
    # 1  1  -> -1 -1
    # 1  0  ->  1 -1
    # 结论：实部 I 由 b1 决定，虚部 Q 由 b0 决定
    i_part = 1.0 - 2.0 * bits_reshaped[:, 1]
    q_part = 1.0 - 2.0 * bits_reshaped[:, 0]

    symbols = (i_part + 1j * q_part) / np.sqrt(2)
    return symbols

def qam16_modulate(bits):
    """
    16-QAM调制函数
    """
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")

    bits_reshaped = bits.reshape(-1, 4)
    # 构造查找表 (LUT): 二进制索引 (b0*2+b1) 对应的映射值
    # 00(0) -> 3, 01(1) -> 1, 10(2) -> -3, 11(3) -> -1
    lut = np.array([3, 1, -3, -1])

    # 计算 I 和 Q 分量的索引
    i_idx = bits_reshaped[:, 0] * 2 + bits_reshaped[:, 1]
    q_idx = bits_reshaped[:, 2] * 2 + bits_reshaped[:, 3]

    i_part = lut[i_idx]
    q_part = lut[q_idx]

    symbols = (i_part + 1j * q_part) / np.sqrt(10)
    return symbols


def test_modulation():
    """
    测试调制函数并生成星座图
    """
    print("=" * 50)
    print("数字调制测试")
    print("=" * 50)
    
    # 测试BPSK
    print("\n1. 测试BPSK调制...")
    try:
        bits_bpsk = np.random.randint(0, 2, 1000)
        symbols_bpsk = bpsk_modulate(bits_bpsk)
        print(f"   输入比特数: {len(bits_bpsk)}")
        print(f"   输出符号数: {len(symbols_bpsk)}")
        print(f"   唯一符号: {np.unique(symbols_bpsk)}")
        
        # 绘制星座图
        plot_constellation(symbols_bpsk[:100], 
                          "BPSK星座图", 
                          "bpsk_constellation.png")
        print("   ✅ BPSK测试通过")
    except NotImplementedError:
        print("   ⏸️ BPSK尚未实现")
    except Exception as e:
        print(f"   ❌ BPSK测试失败: {e}")
    
    # 测试QPSK
    print("\n2. 测试QPSK调制...")
    try:
        bits_qpsk = np.random.randint(0, 2, 1000)
        symbols_qpsk = qpsk_modulate(bits_qpsk)
        print(f"   输入比特数: {len(bits_qpsk)}")
        print(f"   输出符号数: {len(symbols_qpsk)}")
        print(f"   符号幅度: {np.abs(symbols_qpsk[:4])}")
        
        # 绘制星座图
        plot_constellation(symbols_qpsk[:200], 
                          "QPSK星座图", 
                          "qpsk_constellation.png")
        print("   ✅ QPSK测试通过")
    except NotImplementedError:
        print("   ⏸️ QPSK尚未实现")
    except Exception as e:
        print(f"   ❌ QPSK测试失败: {e}")
    
    # 测试16-QAM
    print("\n3. 测试16-QAM调制...")
    try:
        bits_qam = np.random.randint(0, 2, 1000)
        symbols_qam = qam16_modulate(bits_qam)
        print(f"   输入比特数: {len(bits_qam)}")
        print(f"   输出符号数: {len(symbols_qam)}")
        print(f"   唯一符号数量: {len(np.unique(symbols_qam))}")
        
        # 绘制星座图
        plot_constellation(symbols_qam[:250], 
                          "16-QAM星座图", 
                          "16qam_constellation.png")
        print("   ✅ 16-QAM测试通过")
    except NotImplementedError:
        print("   ⏸️ 16-QAM尚未实现")
    except Exception as e:
        print(f"   ❌ 16-QAM测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！请检查results/目录中的星座图。")
    print("=" * 50)


if __name__ == "__main__":
    test_modulation()
