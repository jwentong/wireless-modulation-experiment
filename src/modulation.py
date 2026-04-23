"""
数字调制模块
实现BPSK、QPSK、16-QAM调制算法
"""

import numpy as np
from utils import plot_constellation


def bpsk_modulate(bits):
    """
    BPSK (Binary Phase Shift Keying) 调制
    
    任务要求：
    - 输入：二进制比特序列（NumPy数组），元素为0或1
    - 输出：调制后的复数符号序列
    - 映射规则：
        比特 0 → 符号 +1
        比特 1 → 符号 -1
    
    参数:
        bits: 二进制比特数组，例如 np.array([0, 1, 0, 1, 1, 0])
    
    返回:
        symbols: 复数符号数组，例如 np.array([1, -1, 1, -1, -1, 1])
    
    提示：
    - 使用NumPy的数组运算可以很简洁地实现映射
    - 可以使用条件表达式或数学运算来完成转换
    - BPSK符号实际上是实数，但为了统一接口返回复数类型
    
    示例：
        >>> bits = np.array([0, 1, 0, 1])
        >>> symbols = bpsk_modulate(bits)
        >>> print(symbols)
        [ 1.+0.j -1.+0.j  1.+0.j -1.+0.j]
    """
    
    # 实现BPSK调制：0→+1, 1→-1，返回复数类型
    symbols = 1 - 2 * bits  # 0->1, 1->-1
    symbols = symbols.astype(np.complex128)  # 转为复数类型
    # 绘制并保存星座图
    plot_constellation(
        symbols,
        title="BPSK星座图",
        filename="bpsk_constellation.png"
    )
    return symbols


def qpsk_modulate(bits):
    """
    QPSK (Quadrature Phase Shift Keying) 调制
    
    任务要求：
    - 输入：二进制比特序列（长度必须是2的倍数）
    - 输出：调制后的复数符号序列
    - 每2个比特映射到1个符号（格雷码映射）：
        00 → (1+1j)/√2   (第一象限，45°)
        01 → (-1+1j)/√2  (第二象限，135°)
        11 → (-1-1j)/√2  (第三象限，225°)
        10 → (1-1j)/√2   (第四象限，315°)
    
    参数:
        bits: 二进制比特数组，长度必须是偶数
    
    返回:
        symbols: 复数符号数组，长度是bits的一半
    
    提示：
    - 先将比特序列按2个一组进行分组
    - 可以使用reshape: bits.reshape(-1, 2)
    - 符号的幅度应该归一化到单位功率：除以√2
    - 格雷码可以避免相邻星座点之间有多个比特差异
    
    示例：
        >>> bits = np.array([0, 0, 0, 1, 1, 1, 1, 0])
        >>> symbols = qpsk_modulate(bits)
        >>> print(symbols)
        [ 0.707+0.707j -0.707+0.707j -0.707-0.707j  0.707-0.707j]
    """
    
    # 检查输入长度
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")

    bits = np.asarray(bits)
    bit_pairs = bits.reshape(-1, 2)
    # 格雷码映射
    mapping = {
        (0, 0): (1 + 1j),   # 00 → 45°
        (0, 1): (-1 + 1j),  # 01 → 135°
        (1, 1): (-1 - 1j),  # 11 → 225°
        (1, 0): (1 - 1j)    # 10 → 315°
    }
    symbols = np.array([mapping[tuple(pair)] for pair in bit_pairs], dtype=np.complex128)
    symbols /= np.sqrt(2)  # 归一化
    # 绘制星座图
    plot_constellation(
        symbols,
        title="QPSK星座图",
        filename="qpsk_constellation.png"
    )
    return symbols


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
    
    # TODO: 在这里实现16-QAM调制
    # 提示步骤：
    # 1. 将比特序列reshape成(N/4, 4)的形状
    # 2. 对每组4个比特：
    #    - 前2位映射到I分量（实部）
    #    - 后2位映射到Q分量（虚部）
    # 3. 使用格雷码映射：00→+3, 01→+1, 11→-1, 10→-3
    # 4. 归一化：除以√10使平均功率为1
    
    # 格雷码映射字典（可选使用）
    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3
    }
    
    bits = np.asarray(bits)
    groups = bits.reshape(-1, 4)
    gray_map = {
        (0, 0): 3,
        (0, 1): 1,
        (1, 1): -1,
        (1, 0): -3
    }
    I = np.array([gray_map[tuple(g[:2])] for g in groups])
    Q = np.array([gray_map[tuple(g[2:])] for g in groups])
    symbols = (I + 1j * Q) / np.sqrt(10)
    # 绘制星座图
    plot_constellation(
        symbols,
        title="16-QAM星座图",
        filename="16qam_constellation.png"
    )
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
