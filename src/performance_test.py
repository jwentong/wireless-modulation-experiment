"""
性能测试模块
测试调制解调系统在不同SNR下的BER性能（选做）
"""

import numpy as np
from modulation import bpsk_modulate, qpsk_modulate, qam16_modulate
from demodulation import bpsk_demodulate, qpsk_demodulate, qam16_demodulate
from utils import add_awgn, calculate_ber, plot_ber_curve, generate_random_bits, setup_chinese_font


def test_ber_performance(modulation_scheme='BPSK', num_bits=10000, snr_range=None):
    """
    测试指定调制方式的BER性能
    
    参数:
        modulation_scheme: 'BPSK', 'QPSK', 或 '16QAM'
        num_bits: 用于测试的比特数量
        snr_range: SNR范围（dB），例如 np.arange(0, 16, 2)
    
    返回:
        snr_db: SNR值数组
        ber_values: 对应的BER值数组
    """
    
    if snr_range is None:
        snr_range = np.arange(0, 16, 2)  # 0, 2, 4, ..., 14 dB
    
    ber_values = []
    
    print(f"\n测试 {modulation_scheme} 性能...")
    print(f"比特数: {num_bits}, SNR范围: {snr_range[0]}~{snr_range[-1]} dB")
    print("-" * 40)
    
    # 选择调制/解调函数
    if modulation_scheme == 'BPSK':
        modulate_func = bpsk_modulate
        demodulate_func = bpsk_demodulate
    elif modulation_scheme == 'QPSK':
        modulate_func = qpsk_modulate
        demodulate_func = qpsk_demodulate
    elif modulation_scheme == '16QAM':
        modulate_func = qam16_modulate
        demodulate_func = qam16_demodulate
    else:
        raise ValueError(f"不支持的调制方式: {modulation_scheme}")
    
    if modulation_scheme == 'BPSK':
        valid_num_bits = num_bits
    elif modulation_scheme == 'QPSK':
        valid_num_bits = (num_bits // 2) * 2
    else:
        valid_num_bits = (num_bits // 4) * 4
    
    if valid_num_bits == 0:
        raise ValueError("num_bits过小，无法满足当前调制方式的分组要求")
    
    if valid_num_bits != num_bits:
        print(f"输入比特数 {num_bits} 已调整为 {valid_num_bits}，以满足 {modulation_scheme} 分组要求")
    
    # 对每个SNR值进行测试
    for snr_db in snr_range:
        # TODO: 完成性能测试的主循环
        # 提示步骤：
        # 1. 生成随机比特序列
        # 2. 调制
        # 3. 添加AWGN噪声
        # 4. 解调
        # 5. 计算BER
        # 6. 将BER添加到ber_values列表
        
        # 你的代码：
        bits_tx = generate_random_bits(valid_num_bits)
        symbols = modulate_func(bits_tx)
        symbols_rx = add_awgn(symbols, snr_db)
        bits_rx = demodulate_func(symbols_rx)
        ber = calculate_ber(bits_tx, bits_rx)
        
        ber_values.append(ber)
        print(f"SNR = {snr_db:2d} dB, BER = {ber:.6f}")
    
    return snr_range, np.array(ber_values)


def compare_modulations():
    """
    比较不同调制方式的性能
    绘制BER对比曲线
    """
    
    print("=" * 50)
    print("数字调制性能对比测试")
    print("=" * 50)
    
    snr_range = np.arange(0, 16, 2)
    
    try:
        # 测试BPSK
        snr_bpsk, ber_bpsk = test_ber_performance('BPSK', num_bits=10000, snr_range=snr_range)
        
        # 测试QPSK
        snr_qpsk, ber_qpsk = test_ber_performance('QPSK', num_bits=10000, snr_range=snr_range)
        
        # 测试16-QAM
        snr_qam, ber_qam = test_ber_performance('16QAM', num_bits=10000, snr_range=snr_range)
        
        # 绘制对比图
        import matplotlib.pyplot as plt
        import os
        
        setup_chinese_font()
        plt.figure(figsize=(10, 6))
        plt.semilogy(snr_bpsk, ber_bpsk, 'b-o', label='BPSK', linewidth=2)
        plt.semilogy(snr_qpsk, ber_qpsk, 'r-s', label='QPSK', linewidth=2)
        plt.semilogy(snr_qam, ber_qam, 'g-^', label='16-QAM', linewidth=2)
        
        plt.xlabel('SNR (dB)', fontsize=12)
        plt.ylabel('Bit Error Rate (BER)', fontsize=12)
        plt.title('数字调制方式性能对比', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, which='both', alpha=0.3)
        
        os.makedirs('results', exist_ok=True)
        filepath = os.path.join('results', 'ber_comparison.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"\n[OK] 性能对比图已保存到: {filepath}")
        
        plt.close()
        
        plot_ber_curve(snr_bpsk, ber_bpsk, title="BPSK BER性能", filename="bpsk_ber.png")
        plot_ber_curve(snr_qpsk, ber_qpsk, title="QPSK BER性能", filename="qpsk_ber.png")
        plot_ber_curve(snr_qam, ber_qam, title="16-QAM BER性能", filename="16qam_ber.png")
        
    except NotImplementedError as e:
        print(f"\n[TODO] 部分函数尚未实现: {e}")
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
    
    print("\n" + "=" * 50)


def main():
    """
    主测试函数
    """
    # 你可以选择运行单个调制方式测试或对比测试
    
    # 选项1: 测试单个调制方式
    # snr_range, ber_values = test_ber_performance('BPSK', num_bits=10000)
    # plot_ber_curve(snr_range, ber_values, title="BPSK BER性能", filename="bpsk_ber.png")
    
    # 选项2: 对比测试（推荐）
    compare_modulations()


if __name__ == "__main__":
    main()
