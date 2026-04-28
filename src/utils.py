"""
工具函数模块
提供绘图、信号处理等辅助功能
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os


def setup_chinese_font():
    """
    设置matplotlib支持中文显示
    """
    try:
        # Windows系统使用微软雅黑
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except Exception:
        print("警告: 无法设置中文字体，图表标签可能显示为方框")


def plot_constellation(symbols, title, filename, show_grid=True):
    """
    绘制星座图
    
    参数:
        symbols: 复数符号数组
        title: 图表标题
        filename: 保存的文件名（相对于results/目录）
        show_grid: 是否显示网格
    """
    setup_chinese_font()
    
    # 创建工程根目录下的results目录（如果不存在）
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    results_dir = os.path.join(repo_root, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    plt.figure(figsize=(8, 8))
    
    # 绘制星座点
    real_parts = np.real(symbols)
    imag_parts = np.imag(symbols)
    plt.scatter(real_parts, imag_parts, s=100, c='blue', marker='o', alpha=0.6, edgecolors='black')
    
    # 设置坐标轴
    max_val = max(np.max(np.abs(real_parts)), np.max(np.abs(imag_parts))) * 1.2
    plt.xlim(-max_val, max_val)
    plt.ylim(-max_val, max_val)
    
    # 添加坐标轴线
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    
    # 网格
    if show_grid:
        plt.grid(True, alpha=0.3)
    
    # 标签
    plt.xlabel('实部 (In-phase)', fontsize=12)
    plt.ylabel('虚部 (Quadrature)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    
    # 设置相等的纵横比
    plt.gca().set_aspect('equal', adjustable='box')
    
    # 保存
    filepath = os.path.join(results_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"星座图已保存到: {filepath}")
    
    plt.close()


def add_awgn(signal, snr_db):
    """
    向信号中添加加性高斯白噪声 (AWGN)
    
    参数:
        signal: 输入信号（复数数组）
        snr_db: 信噪比（dB）
    
    返回:
        加噪后的信号
    """
    # 计算信号功率
    signal_power = np.mean(np.abs(signal) ** 2)
    
    # 计算噪声功率
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear
    
    # 生成复高斯噪声
    noise_real = np.random.normal(0, np.sqrt(noise_power / 2), signal.shape)
    noise_imag = np.random.normal(0, np.sqrt(noise_power / 2), signal.shape)
    noise = noise_real + 1j * noise_imag
    
    return signal + noise


def calculate_ber(bits_tx, bits_rx):
    """
    计算误比特率 (BER)
    
    参数:
        bits_tx: 发送的比特序列
        bits_rx: 接收的比特序列
    
    返回:
        BER值（0到1之间）
    """
    if len(bits_tx) != len(bits_rx):
        raise ValueError("发送和接收的比特序列长度不一致")
    
    errors = np.sum(bits_tx != bits_rx)
    ber = errors / len(bits_tx)
    return ber


def plot_ber_curve(snr_range, ber_values, title="BER vs SNR", filename="ber_curve.png"):
    """
    绘制BER性能曲线
    
    参数:
        snr_range: SNR值数组（dB）
        ber_values: 对应的BER值数组
        title: 图表标题
        filename: 保存的文件名
    """
    setup_chinese_font()
    
    # 创建results目录
    os.makedirs('results', exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(snr_range, ber_values, 'b-o', linewidth=2, markersize=8)
    
    plt.xlabel('SNR (dB)', fontsize=12)
    plt.ylabel('Bit Error Rate (BER)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, which='both', alpha=0.3)
    
    # 保存
    filepath = os.path.join('results', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"BER曲线已保存到: {filepath}")
    
    plt.close()


def generate_random_bits(n):
    """
    生成随机比特序列
    
    参数:
        n: 比特数量
    
    返回:
        长度为n的随机比特数组（0或1）
    """
    return np.random.randint(0, 2, n)


if __name__ == "__main__":
    print("工具函数模块测试...")
    
    # 测试随机比特生成
    bits = generate_random_bits(100)
    print(f"生成了 {len(bits)} 个随机比特")
    
    # 测试星座图绘制
    test_symbols = np.array([1+1j, -1+1j, -1-1j, 1-1j]) / np.sqrt(2)
    plot_constellation(test_symbols, "测试星座图", "test_constellation.png")
    
    print("工具函数测试完成！")
