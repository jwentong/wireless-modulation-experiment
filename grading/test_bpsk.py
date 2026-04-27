"""
BPSK调制自动评分测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from modulation import bpsk_modulate


class TestBPSK:
    """BPSK调制测试类"""
    
    def test_basic_mapping(self):
        """测试基本映射规则"""
        bits = np.array([0, 1, 0, 1])
        symbols = bpsk_modulate(bits)
        
        # 检查长度
        assert len(symbols) == len(bits), "输出符号数量应等于输入比特数量"
        
        # 检查映射：0→+1, 1→-1
        expected = np.array([1, -1, 1, -1])
        np.testing.assert_array_almost_equal(np.real(symbols), expected, decimal=5,
                                            err_msg="BPSK映射错误：0应映射到+1，1应映射到-1")
    
    def test_all_zeros(self):
        """测试全0输入"""
        bits = np.zeros(10, dtype=int)
        symbols = bpsk_modulate(bits)
        assert np.allclose(np.real(symbols), 1), "全0比特应映射到全+1符号"
    
    def test_all_ones(self):
        """测试全1输入"""
        bits = np.ones(10, dtype=int)
        symbols = bpsk_modulate(bits)
        assert np.allclose(np.real(symbols), -1), "全1比特应映射到全-1符号"
    
    def test_symbol_values(self):
        """测试符号取值正确性"""
        bits = np.random.randint(0, 2, 100)
        symbols = bpsk_modulate(bits)
        
        unique_real = np.unique(np.round(np.real(symbols), 5))
        assert len(unique_real) <= 2, "BPSK符号实部应只有两个取值"
        assert set(unique_real).issubset({-1.0, 1.0}), "BPSK符号应为+1或-1"
    
    def test_random_sequence(self):
        """测试随机比特序列"""
        np.random.seed(42)
        bits = np.random.randint(0, 2, 1000)
        symbols = bpsk_modulate(bits)
        
        # 验证每个符号
        for i, bit in enumerate(bits):
            expected = 1 if bit == 0 else -1
            actual = np.real(symbols[i])
            assert np.isclose(actual, expected, atol=1e-5), \
                f"第{i}个比特{bit}映射错误，期望{expected}，得到{actual}"
    
    def test_large_sequence(self):
        """测试大规模比特序列"""
        bits = np.random.randint(0, 2, 10000)
        symbols = bpsk_modulate(bits)
        
        assert len(symbols) == 10000, "大规模测试失败：输出长度不正确"
        
        # 统计符号分布（应该接近50%:50%）
        num_positive = np.sum(np.real(symbols) > 0)
        ratio = num_positive / len(symbols)
        assert 0.45 < ratio < 0.55, f"符号分布异常：正符号比例={ratio:.2%}（应接近50%）"


def test_constellation_file_exists():
    """测试是否生成了星座图文件"""
    constellation_file = os.path.join('results', 'bpsk_constellation.png')
    
    # 如果文件不存在，尝试运行modulation.py生成
    if not os.path.exists(constellation_file):
        pytest.skip("BPSK星座图文件不存在，请运行modulation.py生成")
    
    # 检查文件大小（至少应该有几KB）
    file_size = os.path.getsize(constellation_file)
    assert file_size > 1000, "BPSK星座图文件过小，可能未正确生成"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])