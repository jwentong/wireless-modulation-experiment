"""
QPSK调制自动评分测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from modulation import qpsk_modulate


class TestQPSK:
    """QPSK调制测试类"""
    
    def test_input_length_validation(self):
        """测试输入长度验证"""
        # 奇数长度应该抛出异常
        bits_odd = np.array([0, 1, 0])
        with pytest.raises(ValueError):
            qpsk_modulate(bits_odd)
    
    def test_output_length(self):
        """测试输出长度"""
        bits = np.array([0, 0, 0, 1, 1, 1, 1, 0])
        symbols = qpsk_modulate(bits)
        assert len(symbols) == len(bits) // 2, "QPSK输出符号数应为输入比特数的一半"
    
    def test_gray_code_mapping(self):
        """测试格雷码映射"""
        # 测试所有4种可能的比特对
        test_cases = [
            ([0, 0], (1 + 1j) / np.sqrt(2)),   # 00 → 45°
            ([0, 1], (-1 + 1j) / np.sqrt(2)),  # 01 → 135°
            ([1, 1], (-1 - 1j) / np.sqrt(2)),  # 11 → 225°
            ([1, 0], (1 - 1j) / np.sqrt(2))    # 10 → 315°
        ]
        
        for bits, expected in test_cases:
            bits_array = np.array(bits)
            symbols = qpsk_modulate(bits_array)
            np.testing.assert_almost_equal(symbols[0], expected, decimal=5,
                                          err_msg=f"格雷码映射错误：{bits} → {symbols[0]} (期望 {expected})")
    
    def test_unit_energy(self):
        """测试符号能量归一化"""
        bits = np.random.randint(0, 2, 100)
        symbols = qpsk_modulate(bits)
        
        # 所有符号的幅度应该接近1
        magnitudes = np.abs(symbols)
        np.testing.assert_array_almost_equal(magnitudes, np.ones(len(symbols)), decimal=4,
                                            err_msg="QPSK符号幅度应为1（单位能量）")
    
    def test_four_constellation_points(self):
        """测试星座点数量"""
        bits = np.random.randint(0, 2, 1000)
        symbols = qpsk_modulate(bits)
        
        # 对符号进行四舍五入并去重
        symbols_rounded = np.round(symbols, decimals=5)
        unique_symbols = np.unique(symbols_rounded)
        
        assert len(unique_symbols) == 4, f"QPSK应有4个不同的星座点，实际有{len(unique_symbols)}个"
    
    def test_phase_distribution(self):
        """测试相位分布"""
        bits = np.random.randint(0, 2, 1000)
        symbols = qpsk_modulate(bits)
        
        # 计算相位（弧度）
        phases = np.angle(symbols)
        
        # 期望的相位（45°, 135°, -135°, -45°）
        expected_phases = [np.pi/4, 3*np.pi/4, -3*np.pi/4, -np.pi/4]
        
        # 检查每个符号的相位是否接近期望值之一
        for phase in phases:
            min_diff = min(abs(phase - exp) for exp in expected_phases)
            assert min_diff < 0.01, f"相位{np.degrees(phase):.1f}°不在期望范围内"
    
    def test_average_power(self):
        """测试平均功率"""
        bits = np.random.randint(0, 2, 10000)
        symbols = qpsk_modulate(bits)
        
        avg_power = np.mean(np.abs(symbols) ** 2)
        assert np.isclose(avg_power, 1.0, atol=0.01), \
            f"QPSK平均功率应为1，实际为{avg_power:.4f}"
    
    def test_consecutive_pairs(self):
        """测试连续比特对的正确映射"""
        bits = np.array([0, 0, 0, 1, 1, 1, 1, 0])
        symbols = qpsk_modulate(bits)
        
        # 手动计算期望值
        expected = np.array([
            (1 + 1j) / np.sqrt(2),    # 00
            (-1 + 1j) / np.sqrt(2),   # 01
            (-1 - 1j) / np.sqrt(2),   # 11
            (1 - 1j) / np.sqrt(2)     # 10
        ])
        
        np.testing.assert_array_almost_equal(symbols, expected, decimal=5,
                                            err_msg="连续比特对映射错误")


def test_constellation_file_exists():
    """测试是否生成了星座图文件"""
    constellation_file = os.path.join('src', 'results', 'qpsk_constellation.png')
    
    if not os.path.exists(constellation_file):
        pytest.skip("QPSK星座图文件不存在，请运行modulation.py生成")
    
    file_size = os.path.getsize(constellation_file)
    assert file_size > 1000, "QPSK星座图文件过小，可能未正确生成"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
