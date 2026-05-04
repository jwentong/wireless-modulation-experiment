"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""

import numpy as np
from utils import plot_constellation


def bpsk_modulate(bits):
    
    symbols = 1 - 2 *bits
    
    # 转换为复数类型（统一接口）
    symbols = symbols.astype(np.complex128)
    
    
    #raise NotImplementedError("请实现QPSK调制函数")
    
    return symbols


def qpsk_modulate(bits):
    
    # 检查输入长度
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")
    
     
    # 将比特序列reshape成(N/2, 2)，每行是一对比特
    bit_pairs = bits.reshape(-1, 2)
    
    # 将每对比特转换为十进制索引：00→0, 01→1, 10→2, 11→3
    indices = bit_pairs[:, 0] * 2 + bit_pairs[:, 1]
    
    # 格雷码映射对应的复数符号（未归一化）
    mapping = np.array([1+1j, -1+1j, 1-1j, -1-1j], dtype=np.complex128)
    
    # 根据索引获取对应的符号
    symbols = mapping[indices]
    
    # 归一化：除以√2，使符号功率为1
    symbols = symbols / np.sqrt(2)

    #raise NotImplementedError("请实现QPSK调制函数")
    
    return symbols


def qam16_modulate(bits):
   
    # 检查输入长度
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")
    
    # 格雷码映射字典（可选使用）
    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3
    }
    
    # 你的代码：
    # 检查输入长度
    
    
    # 将比特序列reshape成(N/4, 4)
    bit_groups = bits.reshape(-1, 4)
    
    
    # 格雷码映射：00→+3, 01→+1, 11→-1, 10→-3
    gray_map = {
        
(0, 0): 3,
        
(0, 1): 1,
        
(1, 1): -1,
        
(1, 0): -3
    
}
    
    
# 前2位决定I分量（实部），后2位决定Q分量（虚部）
    I_values = np.array([gray_map[tuple(pair)] for pair in bit_groups[:, :2]])
    Q_values = np.array([gray_map[tuple(pair)] for pair in bit_groups[:, 2:]])
    
    
# 组合成复数符号
    symbols = I_values + 1j * Q_values
    
    
# 归一化：除以√10使平均功率为1
    symbols = symbols / np.sqrt(10)
 
    #raise NotImplementedError("请实现16-QAM调制函数")
    
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
