# 数字调制解调实验报告

**实验名称**：数字调制解调实验  
**学生姓名**：[学生姓名]  
**学号**：[学号]  
**实验日期**：2026年4月23日  
**提交日期**：2026年4月23日

---

## 1. 实验目的

- 理解数字调制的基本原理（BPSK、QPSK、16-QAM）
- 掌握三种调制方式的星座点映射规则和实现方法
- 通过Python实现调制和解调算法
- 学习信号处理和性能分析的工程方法
- 体验AI编程助手在实际开发中的应用价值

---

## 2. 实验原理

### 2.1 BPSK调制原理

BPSK（二进制相移键控）是最简单的数字调制方式，每个比特对应一个不同的载波相位。

**映射规则**：
$$
s = \begin{cases}
+1, & \text{if } b = 0 \\
-1, & \text{if } b = 1
\end{cases}
$$

**星座图特征**：
- 符号点数：2个，分布在实轴上
- 相位差：180°
- 星座效率：1 bit/symbol
- 幅度：均为1

**优缺点**：
- ✅ 实现简单，抗噪声能力强
- ❌ 频谱效率低，只有1 bit/symbol

### 2.2 QPSK调制原理

QPSK（正交相移键控）在I/Q两个正交方向同时调制，每2个比特映射为1个符号。

**格雷码映射规则**：

| 比特对 | 符号值 | 相位 |
|--------|--------|------|
| 00 | $(1+1j)/\sqrt{2}$ | 45° |
| 01 | $(-1+1j)/\sqrt{2}$ | 135° |
| 11 | $(-1-1j)/\sqrt{2}$ | 225° |
| 10 | $(1-1j)/\sqrt{2}$ | 315° |

**星座图特征**：
- 符号点数：4个，均匀分布在单位圆上
- 相位间隔：90°
- 星座效率：2 bit/symbol
- 幅度：均为$1/\sqrt{2}$

**优缺点**：
- ✅ 频谱效率是BPSK的两倍
- ❌ 抗噪声能力比BPSK略低

### 2.3 16-QAM调制原理

16-QAM（16级正交幅度调制）在I/Q方向同时调制幅度和相位，16个符号排列成4×4的方格。

**映射规则**：
- I/Q分量使用格雷码映射：$00 \to +3$，$01 \to +1$，$11 \to -1$，$10 \to -3$
- 4个比特分组：前2位→I分量，后2位→Q分量
- 功率归一化因子：$\sqrt{10}$（平均功率为1）

**星座图特征**：
- 符号点数：16个，排成4×4方形网格
- I/Q分量值：$\{-3, -1, +1, +3\}/\sqrt{10}$
- 星座效率：4 bit/symbol
- 幅度：变化（从小到大）

**优缺点**：
- ✅ 频谱效率高（4 bit/symbol），适合带宽受限应用
- ❌ 对噪声敏感，需要更高的SNR


---

## 3. 实验方法与步骤

### 3.1 环境配置

使用GitHub Copilot AI编程助手辅助配置Python开发环境。

**依赖包**：
- NumPy：数组运算和信号处理
- Matplotlib：数据可视化和星座图绘制
- SciPy：科学计算辅助

项目结构：
```
src/
  ├── modulation.py       # 调制函数实现
  ├── demodulation.py     # 解调函数实现（选做）
  ├── performance_test.py # BER性能测试（选做）
  ├── utils.py            # 工具函数
  └── test_environment.py # 环境测试
results/                   # 输出结果目录
```

### 3.2 BPSK实现

**实现思路**：
1. 比特序列进行数学变换：`0 → +1`，`1 → -1`
2. 使用公式 `s = 1 - 2*bits` 完成映射
3. 转换为复数类型保持接口一致

**核心代码**：
```python
def bpsk_modulate(bits):
    symbols = 1 - 2 * bits
    return symbols.astype(np.complex128)
```

**关键参数**：
- 输入：一维比特数组 `[0,1,0,1,...]`
- 输出：复数符号数组

### 3.3 QPSK实现

**实现思路**：
1. 验证比特序列长度为偶数
2. 将比特按2个一组重新分组 `reshape(-1, 2)`
3. 根据格雷码映射生成I/Q分量
4. 使用公式生成归一化符号

**关键映射**：
- 第一列bit决定Q分量：`q = 1 - 2*bit_pair[:,0]`
- 第二列bit决定I分量：`i = 1 - 2*bit_pair[:,1]`
- 符号 = `(i + 1j*q) / √2`

**核心代码**：
```python
bit_pairs = bits.reshape(-1, 2)
i = 1 - 2 * bit_pairs[:, 1]
q = 1 - 2 * bit_pairs[:, 0]
symbols = (i + 1j * q) / np.sqrt(2)
```

### 3.4 16-QAM实现

**实现思路**：
1. 验证比特序列长度为4的倍数
2. 将比特按4个一组重新分组
3. 分别提取前2位和后2位应用格雷码映射
4. 组合I/Q分量并用√10归一化

**格雷码映射函数**：
```python
gray_map = {
    (0, 0): 3,
    (0, 1): 1,
    (1, 1): -1,
    (1, 0): -3
}
```

**核心代码**：
```python
symbol_groups = bits.reshape(-1, 4)
i_bits = symbol_groups[:, :2]
q_bits = symbol_groups[:, 2:]
i = np.array([gray_map[tuple(pair)] for pair in i_bits])
q = np.array([gray_map[tuple(pair)] for pair in q_bits])
symbols = (i + 1j * q) / np.sqrt(10)
```

### 3.5 星座图绘制（解调和性能测试为选做项）

使用Matplotlib在results/目录生成星座图PNG文件，包含：
- 星座点散点分布
- 网格和参考坐标轴
- 中文标签和标题
- 300 dpi高分辨率输出


---

## 4. 实验结果

### 4.1 BPSK星座图

![BPSK星座图](results/bpsk_constellation.png)

**分析**：从图中可以看出BPSK有2个星座点分别位于实轴的+1和-1位置。相位相差180°，符号间距最大，对噪声最为鲁棒。

### 4.2 QPSK星座图

![QPSK星座图](results/qpsk_constellation.png)

**分析**：QPSK的4个星座点均匀分布在单位圆上，相位间隔为90°。相比BPSK，星座效率提升一倍（2 bit/symbol），但符号间距减小，抗噪声能力略弱。

### 4.3 16-QAM星座图

![16-QAM星座图](results/16qam_constellation.png)

**分析**：16个星座点排成4×4的规则方格，星座效率达到4 bit/symbol。符号点最密集，对噪声最敏感。I/Q分量值为 $\{\pm1, \pm3\}/\sqrt{10}$，体现了幅度和相位的联合调制。

### 4.4 性能测试结果

![BER性能对比曲线](results/ber_comparison.png)

**性能数据表**：

| SNR(dB) | BPSK BER | QPSK BER | 16-QAM BER |
|---------|----------|----------|-----------|
| 0 | 0.0834 | 0.1603 | 0.2907 |
| 2 | 0.0380 | 0.1070 | 0.2381 |
| 4 | 0.0126 | 0.0566 | 0.1813 |
| 6 | 0.0030 | 0.0202 | 0.1396 |
| 8 | 0.0004 | 0.0066 | 0.0986 |
| 10 | 0.0000 | 0.0012 | 0.0592 |
| 12 | 0.0000 | 0.0001 | 0.0249 |
| 14 | 0.0000 | 0.0000 | 0.0087 |

**关键观察**：
- BPSK在SNR ≥ 8 dB时BER趋近于0
- QPSK需要SNR ≥ 10 dB才能达到极低BER
- 16-QAM在SNR = 14 dB时BER仍为0.87%


---

## 5. 结果分析与讨论

### 5.1 星座图对比分析

三种调制方式在星座点数和密集度上的权衡：

| 特性 | BPSK | QPSK | 16-QAM |
|------|------|------|--------|
| 星座点数 | 2 | 4 | 16 |
| 星座效率 | 1 bit/s | 2 bit/s | 4 bit/s |
| 符号间距 | 最大 | 中等 | 最小 |
| 噪声鲁棒性 | 最强 | 中等 | 最弱 |

### 5.2 性能对比分析

从BER曲线可以看出频谱效率和抗噪声的权衡：

1. **BPSK性能最优**
   - SNR = 8 dB时BER < 0.04%
   - 符号间距大，噪声鲁棒性强

2. **QPSK性能次之**
   - 需要额外2~3 dB SNR才能达到BPSK的性能
   - 星座效率提升一倍的代价

3. **16-QAM性能最差**
   - 需要SNR > 14 dB才能达到低误码率
   - 星座点密集，对噪声极其敏感

### 5.3 频谱效率与性能的权衡

实际应用中的选择准则：
- **低SNR信道**：优先选择BPSK
- **中等SNR信道**：选择QPSK获得2倍效率
- **高SNR信道/带宽受限**：选择16-QAM获得4倍效率

### 5.4 遇到的问题与解决

**问题**：初次运行 `compare_modulations()` 时遇到中文编码错误

- **原因**：Windows命令行默认编码为GBK，Matplotlib的emoji字符导致编码冲突
- **解决**：修改输出提示为ASCII字符，绘图保存正常进行


---

## 6. 实验心得与Copilot使用体会

### 6.1 实验心得

- **理论联系实践**：通过代码实现加深了对调制原理的理解，特别是格雷码映射的必要性和功率归一化的意义
- **工程工具掌握**：学会了NumPy向量化运算、Matplotlib数据可视化、AWGN模型的信号处理方法
- **性能指标理解**：通过BER曲线深刻认识到频谱效率与抗噪声能力的本质权衡
- **问题求解能力**：遇到编码、维度等问题时能够快速定位和修正

### 6.2 AI助手使用体会

**有效场景**：
- ✅ 快速生成框架代码和规范模板
- ✅ 提供NumPy/Matplotlib等库函数的正确用法
- ✅ 帮助调试运行时错误和数组维度问题
- ✅ 给出性能优化和代码风格建议

**需要谨慎的地方**：
- ⚠️ 不能盲目复制粘贴，必须理解每一行代码的含义
- ⚠️ 生成的代码有时存在细微逻辑错误，需要验证
- ⚠️ 过度依赖AI会削弱独立思考和问题求解能力

**建议**：
1. 先充分理解调制原理，再使用AI辅助代码实现
2. 充分测试AI生成的代码，特别是复杂的数学运算
3. 对AI提供的建议要有批判性思维

### 6.3 改进建议

- 可增加更多调制方式（OFDM、FSK等）进行对比
- 引入实际信道模型（多径、多普勒效应）
- 考虑硬判决之外的软判决解调算法
- 增加GNU Radio或SDR设备的实时处理实验


---

## 7. 参考文献

1. Proakis, J. G., & Salehi, M. (2008). *Digital Communications* (5th ed.). McGraw-Hill.
2. 樊昌信, 曾志民. (2017). *通信原理* (7版). 国防工业出版社.
3. Richard D. Gitlin, Jeremiah F. Hayes, Stephen B. Weinstein. (1992). *Data Communications Principles*. Plenum Press.
4. NumPy官方文档: https://numpy.org/doc/
5. Matplotlib官方文档: https://matplotlib.org/

---

## 附录：完整代码

本实验的关键函数签名如下：

**调制函数** (`src/modulation.py`)：
```python
def bpsk_modulate(bits: np.ndarray) -> np.ndarray
    """输入比特数组，输出复数符号"""

def qpsk_modulate(bits: np.ndarray) -> np.ndarray
    """输入偶数长比特数组，输出QPSK符号"""

def qam16_modulate(bits: np.ndarray) -> np.ndarray
    """输入4倍数长比特数组，输出16-QAM符号"""
```

**解调函数** (`src/demodulation.py`)：
```python
def bpsk_demodulate(symbols: np.ndarray) -> np.ndarray
    """基于实部符号判决"""

def qpsk_demodulate(symbols: np.ndarray) -> np.ndarray
    """最小欧氏距离判决"""

def qam16_demodulate(symbols: np.ndarray) -> np.ndarray
    """分别对I/Q路进行判决"""
```

**性能测试** (`src/performance_test.py`)：
```python
def test_ber_performance(modulation_scheme, num_bits=10000, snr_range=None)
    """测试单种调制方式的BER性能"""

def compare_modulations()
    """对比三种调制方式并绘制BER曲线"""
```

---

**声明**：本实验报告内容真实，所有代码均为本人在GitHub Copilot AI助手辅助下完成，核心算法和逻辑为本人设计。实验结果经过验证，所有星座图和性能曲线均由本人代码生成。

**签名**：_____________  
**日期**：2026年4月23日

