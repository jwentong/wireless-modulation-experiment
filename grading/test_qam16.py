"""
16-QAM调制自动评分测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from modulation import qam16_modulate


class TestQAM16:
    """16-QAM调制测试类"""
    
    def test_input_length_validation(self):
        """测试输入长度验证"""
        # 非4的倍数应该抛出异常
        for length in [1, 2, 3, 5, 6, 7]:
            bits = np.random.randint(0, 2, length)
            with pytest.raises(ValueError):
                qam16_modulate(bits)
    
    def test_output_length(self):
        """测试输出长度"""
        for length in [4, 8, 12, 16, 100]:
            bits = np.random.randint(0, 2, length)
            symbols = qam16_modulate(bits)
            assert len(symbols) == length // 4, \
                f"16-QAM输出符号数应为输入比特数的1/4，输入{length}比特应输出{length//4}符号"
    
    def test_sixteen_constellation_points(self):
        """测试星座点数量"""
        # 确保有足够的比特生成所有16个可能的符号
        bits = np.random.randint(0, 2, 1000)
        symbols = qam16_modulate(bits)
        
        # 对符号进行四舍五入并去重
        symbols_rounded = np.round(symbols, decimals=4)
        unique_symbols = np.unique(symbols_rounded)
        
        # 可能不是所有16个点都出现，但至少应该有10个以上
        assert len(unique_symbols) >= 10, \
            f"16-QAM星座点数量不足，期望至少10个，实际{len(unique_symbols)}个"
    
    def test_iq_component_values(self):
        """测试I/Q分量取值"""
        bits = np.random.randint(0, 2, 400)
        symbols = qam16_modulate(bits)
        
        # 归一化前的I/Q分量应该是{-3, -1, +1, +3}
        # 归一化后应该是这些值除以√10
        norm_factor = np.sqrt(10)
        expected_values = np.array([-3, -1, 1, 3]) / norm_factor
        
        real_parts = np.real(symbols)
        imag_parts = np.imag(symbols)
        
        # 检查实部
        for val in np.unique(np.round(real_parts, 4)):
            min_diff = min(abs(val - exp) for exp in expected_values)
            assert min_diff < 0.01, f"实部值{val:.4f}不在期望范围内"
        
        # 检查虚部
        for val in np.unique(np.round(imag_parts, 4)):
            min_diff = min(abs(val - exp) for exp in expected_values)
            assert min_diff < 0.01, f"虚部值{val:.4f}不在期望范围内"
    
    def test_power_normalization(self):
        """测试功率归一化"""
        bits = np.random.randint(0, 2, 10000)
        symbols = qam16_modulate(bits)
        
        # 计算平均功率
        avg_power = np.mean(np.abs(symbols) ** 2)
        
        # 平均功率应接近1
        assert np.isclose(avg_power, 1.0, atol=0.05), \
            f"16-QAM平均功率应为1，实际为{avg_power:.4f}"
    
    def test_gray_code_mapping(self):
        """测试格雷码映射（部分测试用例）"""
        # 测试几个特定的比特组合
        test_cases = [
            [0, 0, 0, 0],  # I=+3, Q=+3
            [0, 1, 0, 1],  # I=+1, Q=+1
            [1, 1, 1, 1],  # I=-1, Q=-1
            [1, 0, 1, 0],  # I=-3, Q=-3
        ]
        
        norm = np.sqrt(10)
        expected_iq = [
            (3 + 3j) / norm,
            (1 + 1j) / norm,
            (-1 - 1j) / norm,
            (-3 - 3j) / norm
        ]
        
        for bits, expected in zip(test_cases, expected_iq):
            bits_array = np.array(bits)
            symbols = qam16_modulate(bits_array)
            np.testing.assert_almost_equal(symbols[0], expected, decimal=4,
                                          err_msg=f"格雷码映射错误：{bits}")
    
    def test_symbol_distribution(self):
        """测试符号分布均匀性"""
        # 大量随机比特应该产生相对均匀的符号分布
        np.random.seed(42)
        bits = np.random.randint(0, 2, 10000)
        symbols = qam16_modulate(bits)
        
        # 统计每个符号出现的次数
        symbols_rounded = np.round(symbols, decimals=3)
        unique, counts = np.unique(symbols_rounded, return_counts=True)
        
        # 每个符号期望出现次数约为 total/16
        expected_count = len(symbols) / 16
        
        # 允许一定的偏差（例如±40%）
        for count in counts:
            ratio = count / expected_count
            assert 0.3 < ratio < 1.7, \
                f"符号分布不均匀：某符号出现{count}次，期望约{expected_count:.0f}次"
    
    def test_corner_points(self):
        """测试四个角点的功率"""
        # 四个角点功率最大
        bits_corners = np.array([
            [0, 0, 0, 0],  # 右上角
            [1, 0, 0, 0],  # 左上角
            [1, 0, 1, 0],  # 左下角
            [0, 0, 1, 0],  # 右下角
        ]).flatten()
        
        symbols = qam16_modulate(bits_corners)
        powers = np.abs(symbols) ** 2
        
        # 角点功率应该相等且最大
        assert np.allclose(powers, powers[0], atol=0.01), "四个角点功率应该相等"
        
        # 角点功率 = (3^2 + 3^2) / 10 = 1.8
        expected_corner_power = 18 / 10
        assert np.isclose(powers[0], expected_corner_power, atol=0.01), \
            f"角点功率应为{expected_corner_power:.2f}，实际为{powers[0]:.2f}"


def test_constellation_file_exists():
    """测试是否生成了星座图文件"""
    constellation_file = os.path.join('results', '16qam_constellation.png')
    
    if not os.path.exists(constellation_file):
        pytest.skip("16-QAM星座图文件不存在，请运行modulation.py生成")
    
    file_size = os.path.getsize(constellation_file)
    assert file_size > 1000, "16-QAM星座图文件过小，可能未正确生成"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])