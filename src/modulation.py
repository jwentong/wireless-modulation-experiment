"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""

import numpy as np
from utils import plot_constellation
import matplotlib.pyplot as plt
import os

def bpsk_modulate(bits):
    """
    BPSK调制函数
    :param bits: 二进制序列（0/1的列表或numpy数组）
    :return: BPSK调制符号（+1/-1的numpy数组）
    """
    # 1. 确保输入是numpy数组，避免类型问题
    bits_np = np.asarray(bits, dtype=int)
    
    # 2. BPSK调制映射（严格按照要求：0→+1，1→-1）
    symbols = 1 - 2 * bits_np
    
    # 3. 创建保存星座图的目录
    os.makedirs('results', exist_ok=True)
    
    # 4. 绘制BPSK星座图（增加异常处理，避免影响主逻辑）
    try:
        plt.figure(figsize=(6, 6))
        plt.scatter(symbols, np.zeros_like(symbols), color='blue', marker='o', label='BPSK Symbols')
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        plt.grid(True, alpha=0.3)
        plt.title('BPSK Constellation Diagram')
        plt.xlabel('In-phase (I)')
        plt.ylabel('Quadrature (Q)')
        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig('results/bpsk_constellation.png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"星座图绘制时出现警告{e}")
    
    return symbols


def qpsk_modulate(bits):
    """
    QPSK调制函数，格雷码映射
    :param bits: 二进制序列（0/1的列表或numpy数组，长度需为偶数）
    :return: QPSK调制后的复数符号数组
    """
    # 1. 确保输入为numpy数组，且长度为偶数
    bits_np = np.asarray(bits, dtype=int)
    if len(bits_np) % 2 != 0:
        raise ValueError("输入比特序列长度必须为偶数，才能映射为QPSK符号")
    
    # 2. 每2个比特为一组，格雷码映射
    symbols = []
    sqrt2 = np.sqrt(2)
    for i in range(0, len(bits_np), 2):
        b1, b0 = bits_np[i], bits_np[i+1]
        if b1 == 0 and b0 == 0:
            symbols.append((1 + 1j) / sqrt2)
        elif b1 == 0 and b0 == 1:
            symbols.append((-1 + 1j) / sqrt2)
        elif b1 == 1 and b0 == 1:
            symbols.append((-1 - 1j) / sqrt2)
        elif b1 == 1 and b0 == 0:
            symbols.append((1 - 1j) / sqrt2)
    symbols = np.array(symbols)
    
    # 3. 创建保存星座图的目录
    os.makedirs('results', exist_ok=True)
    
    # 4. 绘制QPSK星座图（带异常捕获，不影响主逻辑）
    try:
        plt.figure(figsize=(6, 6))
        plt.scatter(np.real(symbols), np.imag(symbols), color='red', marker='o', label='QPSK Symbols')
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        plt.grid(True, alpha=0.3)
        plt.title('QPSK Constellation Diagram')
        plt.xlabel('In-phase (I)')
        plt.ylabel('Quadrature (Q)')
        plt.xlim(-1.2, 1.2)
        plt.ylim(-1.2, 1.2)
        plt.legend()
        plt.tight_layout()
        plt.savefig('results/qpsk_constellation.png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"星座图绘制时出现警告（不影响调制结果）: {e}")
    
    return symbols


import numpy as np

def qam16_modulate(bits):
    """
    16-QAM (16-Quadrature Amplitude Modulation) 调制
    
    任务要求：
    - 输入：二进制比特序列（长度必须是4的倍数）
    - 输出：调制后的复数符号序列
    - 每4个比特映射到1个符号
    - I路和Q路分量取值：{-3, -1, +1, +3}
    - 使用格雷码映射（推荐）
    
    参数:
        bits: 二进制比特数组，长度必须是4的倍数
    
    返回:
        symbols: 复数符号数组，长度是bits的四分之一
    
    提示：
    - 16-QAM有16个星座点，排列成4×4的方格
    - 可以将4个比特分成两组：前2位决定I分量，后2位决定Q分量
    - I/Q分量的映射（格雷码）：
        00 → +3
        01 → +1
        11 → -1
        10 → -3
    - 需要对星座图进行功率归一化
    - 平均功率 = (3²+1²+1²+3²)/4 = 5，归一化因子 = √10
    
    示例：
        >>> bits = np.array([0, 0, 0, 0, 0, 1, 0, 1])
        >>> symbols = qam16_modulate(bits)
        # 应该得到两个符号在正确位置
    """
    
    # 检查输入长度
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")
    
    # 格雷码映射字典
    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3
    }

    # 1. 将比特序列reshape为 (符号数, 4) 的二维数组
    bit_groups = bits.reshape(-1, 4)
    
    # 2. 分离每组的前2位(I路)和后2位(Q路)
    i_bits = bit_groups[:, :2]  # 前2位 → I分量（实部）
    q_bits = bit_groups[:, 2:]  # 后2位 → Q分量（虚部）
    
    # 3. 根据格雷码映射得到I、Q原始值
    i_values = np.array([gray_map[tuple(bits)] for bits in i_bits])
    q_values = np.array([gray_map[tuple(bits)] for bits in q_bits])
    
    # 4. 功率归一化：除以√10
    norm_factor = np.sqrt(10)
    i_normalized = i_values / norm_factor
    q_normalized = q_values / norm_factor
    
    # 5. 组合为复数符号
    symbols = i_normalized + 1j * q_normalized
    
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
