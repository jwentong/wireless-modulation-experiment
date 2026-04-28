import numpy as np
import matplotlib.pyplot as plt
import os

def bpsk_modulate(bits):
    """
    BPSK 调制
    参数: bits: numpy.ndarray, 二进制序列 [0, 1, 0, 1, ...]
    返回: symbols: numpy.ndarray, 调制符号 [+1, -1, +1, -1, ...]
    """
    symbols = 1 - 2 * bits  # 比特0→+1，比特1→-1
    return symbols

def qpsk_modulate(bits):
    """
    QPSK 调制
    参数: bits: numpy.ndarray, 二进制序列（长度为偶数）
    返回: symbols: numpy.ndarray, 复数符号序列
    """
    bits = bits.reshape(-1, 2)  # 每2比特一组
    mapping = {
        (0, 0): (1 + 1j) / np.sqrt(2),
        (0, 1): (-1 + 1j) / np.sqrt(2),
        (1, 1): (-1 - 1j) / np.sqrt(2),
        (1, 0): (1 - 1j) / np.sqrt(2),
    }
    symbols = np.array([mapping[(b[0], b[1])] for b in bits])
    return symbols

def qam16_modulate(bits):
    """
    16-QAM 调制
    参数: bits: numpy.ndarray, 二进制序列（长度为4的倍数）
    返回: symbols: numpy.ndarray, 复数符号序列
    """
    bits = bits.reshape(-1, 4)  # 每4比特一组
    # 格雷码映射 2比特→I或Q分量
    gray_map = {(0,0): 1, (0,1): 3, (1,1): -3, (1,0): -1}
    symbols = []
    for b in bits:
        I = gray_map[(b[0], b[1])]
        Q = gray_map[(b[2], b[3])]
        symbols.append(complex(I, Q))
    symbols = np.array(symbols) / np.sqrt(10)  # 归一化
    return symbols

def plot_constellation(symbols, title, filename):
    """绘制星座图"""
    os.makedirs('results', exist_ok=True)
    plt.figure(figsize=(6, 6))
    plt.scatter(np.real(symbols), np.imag(symbols),
                s=100, alpha=0.6, edgecolors='blue')
    plt.grid(True, alpha=0.3)
    plt.xlabel('In-phase (I)', fontsize=12)
    plt.ylabel('Quadrature (Q)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 星座图已保存到: {filename}")

if __name__ == '__main__':
    print("=== 测试 BPSK 调制 ===")
    bits_bpsk = np.array([0, 1, 0, 1, 1, 0, 0, 1])
    symbols_bpsk = bpsk_modulate(bits_bpsk)
    print(f"输入比特: {bits_bpsk}")
    print(f"输出符号: {symbols_bpsk}")
    plot_constellation(symbols_bpsk, 'BPSK Constellation',
                      'results/bpsk_constellation.png')

    print("\n=== 测试 QPSK 调制 ===")
    bits_qpsk = np.array([0, 0, 0, 1, 1, 1, 1, 0])
    symbols_qpsk = qpsk_modulate(bits_qpsk)
    print(f"输入比特: {bits_qpsk}")
    print(f"输出符号: {symbols_qpsk}")
    plot_constellation(symbols_qpsk, 'QPSK Constellation',
                      'results/qpsk_constellation.png')

    print("\n=== 测试 16-QAM 调制 ===")
    bits_qam = np.array([0,0,0,0, 0,1,0,1, 1,1,1,1, 1,0,1,0])
    symbols_qam = qam16_modulate(bits_qam)
    print(f"输入比特: {bits_qam}")
    print(f"输出符号: {symbols_qam}")
    plot_constellation(symbols_qam, '16-QAM Constellation',
                      'results/16qam_constellation.png')
    
    print("\n✅ 全部完成！请检查 results/ 文件夹查看星座图。")
