# 实验报告模板

**实验名称**：数字调制解调实验  
**学生姓名**：[孟佳霖]  
**学号**：[2024280057]  
**实验日期**：2026年4月24日  
**提交日期**：2026年4月29日

---

## 1. 实验目的

- 理解数字调制的基本原理，掌握比特序列到复数星座符号的映射方法。
- 掌握BPSK、QPSK、16-QAM三种典型数字调制算法的Python实现。
- 学习使用NumPy进行数组化信号处理，并使用Matplotlib生成星座图和BER性能曲线。
- 完成BPSK、QPSK、16-QAM的解调函数，理解硬判决和最小欧氏距离判决方法。
- 通过AWGN信道仿真观察不同调制方式在不同SNR下的误比特率变化。
- 体验AI编程助手在代码补全、错误定位和实验报告整理中的辅助作用。

---

## 2. 实验原理

### 2.1 BPSK调制原理

BPSK(Binary Phase Shift Keying)是最简单的相移键控方式。它每个符号只携带1个比特，通过两个相位相差180度的星座点表示二进制信息。本实验采用复数基带表示，两个符号位于实轴的+1和-1处，虚部为0。

BPSK的基本映射关系为：比特0映射为符号+1，比特1映射为符号-1。由于两个星座点距离较远，BPSK具有较好的抗噪声性能，适合低信噪比场景；缺点是每个符号只传输1比特，频谱效率较低。

可以插入公式（使用LaTeX语法）：

比特 $b$ 映射到符号 $s$：
$$
s = 
\begin{cases}
+1, & \text{if } b = 0 \\
-1, & \text{if } b = 1
\end{cases}
$$

### 2.2 QPSK调制原理

QPSK(Quadrature Phase Shift Keying)每2个比特映射为1个复数符号，星座图中共有4个点。四个点分布在单位圆的四个象限，分别对应45度、135度、225度和315度方向。与BPSK相比，QPSK在相同符号率下每个符号可携带2比特，因此频谱效率提高一倍。

本实验采用格雷码映射，使相邻星座点之间只相差1个比特，从而降低符号判决错误时造成的比特错误数。映射关系为：

| 比特对 | 复数符号 |
|--------|----------|
| 00 | $(1+j)/\sqrt{2}$ |
| 01 | $(-1+j)/\sqrt{2}$ |
| 11 | $(-1-j)/\sqrt{2}$ |
| 10 | $(1-j)/\sqrt{2}$ |

除以 $\sqrt{2}$ 的目的是让每个QPSK符号的能量归一化为1。

### 2.3 16-QAM调制原理

16-QAM(16-Quadrature Amplitude Modulation)同时利用同相分量I和正交分量Q的幅度变化来传输信息。它每4个比特映射为1个复数符号，其中前2位决定I路分量，后2位决定Q路分量。I/Q分量均采用格雷码映射：

| 比特 | 分量取值 |
|------|----------|
| 00 | +3 |
| 01 | +1 |
| 11 | -1 |
| 10 | -3 |

16-QAM共有16个星座点，排列成4×4方阵。由于每个符号携带4比特，其频谱效率高于BPSK和QPSK，但星座点间距更近，对噪声更敏感。为了使平均符号功率归一化，调制输出需要除以 $\sqrt{10}$：

$$
s = \frac{I + jQ}{\sqrt{10}}
$$

---

## 3. 实验方法与步骤

### 3.1 环境配置

本实验使用Python环境完成，主要依赖NumPy、Matplotlib、SciPy、pytest等库。首先根据`requirements.txt`安装依赖，然后运行环境测试脚本和评分测试脚本验证环境可用性。实验过程中使用AI助手辅助理解模板要求、检查代码结构、定位TODO位置，并最终通过本地pytest测试确认调制函数正确。

主要验证命令如下：

```bash
python src/modulation.py
python src/demodulation.py
python src/performance_test.py
python -m pytest grading/test_bpsk.py grading/test_qpsk.py grading/test_qam16.py -q
```

### 3.2 BPSK实现

BPSK实现步骤为：先将输入比特转换为NumPy数组并检查其只包含0和1，然后使用数学表达式`1 - 2 * bits`完成映射。该表达式在比特为0时得到+1，在比特为1时得到-1，最后转换为复数类型以统一接口。

```python
def bpsk_modulate(bits):
    bits = _as_binary_array(bits)
    return (1 - 2 * bits).astype(complex)
```

对应解调采用硬判决方法，只判断接收符号实部的正负：实部大于0判为0，否则判为1。

### 3.3 QPSK实现

QPSK实现步骤为：检查输入比特长度是否为2的倍数，将比特序列reshape为`(N/2, 2)`，再分别生成I路和Q路分量。本实验的格雷码映射中，第二个比特决定I分量符号，第一个比特决定Q分量符号，最后除以 $\sqrt{2}$ 完成能量归一化。

```python
def qpsk_modulate(bits):
    bits = _as_binary_array(bits)
    if len(bits) % 2 != 0:
        raise ValueError("QPSK requires an even number of bits")

    bit_pairs = bits.reshape(-1, 2)
    i_values = np.where(bit_pairs[:, 1] == 0, 1, -1)
    q_values = np.where(bit_pairs[:, 0] == 0, 1, -1)
    return (i_values + 1j * q_values).astype(complex) / np.sqrt(2)
```

QPSK解调使用最小欧氏距离判决。程序预先定义四个理想星座点和对应比特对，对每个接收符号计算到四个参考点的距离，选择距离最小的点并输出对应比特。

### 3.4 16-QAM实现

16-QAM实现步骤为：检查输入比特长度是否为4的倍数，将每4个比特分为一组，其中前两位映射到I分量，后两位映射到Q分量。分量映射采用格雷码`00 -> +3, 01 -> +1, 11 -> -1, 10 -> -3`，最后组合为复数并除以 $\sqrt{10}$。

```python
def qam16_modulate(bits):
    bits = _as_binary_array(bits)
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM requires the number of bits to be a multiple of 4")

    bit_groups = bits.reshape(-1, 4)

    def component_levels(two_bit_groups):
        first = two_bit_groups[:, 0]
        second = two_bit_groups[:, 1]
        return np.where(first == 0, 3 - 2 * second, -3 + 2 * second)

    i_values = component_levels(bit_groups[:, :2])
    q_values = component_levels(bit_groups[:, 2:])
    return (i_values + 1j * q_values).astype(complex) / np.sqrt(10)
```

16-QAM解调同样采用最小距离思想，但分别对I路和Q路进行判决。程序将实部和虚部分别与归一化后的四个电平`-3, -1, +1, +3`比较，选择最近电平并恢复对应的2比特格雷码。

---

## 4. 实验结果

### 4.1 BPSK星座图

![BPSK星座图](results/bpsk_constellation.png)

**分析**：从图中可以看出BPSK有两个星座点，分别位于实轴的+1和-1附近，虚部约为0。这说明BPSK只通过相位翻转表示二进制信息。两个点之间距离较大，因此在加入一定噪声时仍容易通过实部正负进行判决。

### 4.2 QPSK星座图

![QPSK星座图](results/qpsk_constellation.png)

**分析**：QPSK星座图中有四个星座点，分布在四个象限，幅度均为1。每个点对应2个比特，使用格雷码映射后，相邻点之间只差1位。与BPSK相比，QPSK在同样符号数下能够传输更多比特，但点间最小距离变小，抗噪声能力略低。

### 4.3 16-QAM星座图

![16-QAM星座图](results/16qam_constellation.png)

**分析**：16-QAM星座图呈4×4方阵，共16个星座点。每个符号携带4个比特，频谱效率最高。图中星座点分布在不同幅度和相位位置，说明16-QAM同时利用幅度和相位传递信息。由于点间距离小于BPSK和QPSK，在相同SNR下更容易发生判决错误。

### 4.4 性能测试结果（选做）

如果完成了BER性能测试，请在此展示结果：

![BER性能曲线](results/ber_comparison.png)

**分析**：从曲线可以看出，三种调制方式的BER都随SNR升高而下降。根据本次仿真输出，BPSK在0 dB时BER约为0.0745，在8 dB时降至0.0003，10 dB及以上基本没有误码；QPSK在0 dB时BER约为0.1605，在10 dB时降至0.0006；16-QAM在0 dB时BER约为0.2915，在14 dB时仍约为0.0102。结果符合理论预期：在相同噪声条件下，星座点越密集，抗噪声性能越差。

---

## 5. 结果分析与讨论

### 5.1 星座图对比分析

对比三种调制方式的星座图可以看出，BPSK结构最简单，只有两个点并且位于实轴上；QPSK有四个点，均匀分布在单位圆四个象限；16-QAM有十六个点，按4×4网格排列。星座点数量越多，每个符号携带的信息量越大，但在固定平均功率下，星座点之间的间隔会减小。

BPSK每个符号携带1比特，抗噪声性能最好；QPSK每个符号携带2比特，在频谱效率和可靠性之间取得平衡；16-QAM每个符号携带4比特，频谱效率最高，但要求更高的信噪比。实际通信系统会根据信道质量选择调制方式，例如信道较差时采用BPSK或QPSK，信道较好时采用16-QAM或更高阶QAM。

### 5.2 性能对比分析

对比三种调制方式的性能，包括：
- 频谱效率：BPSK每符号1比特，QPSK每符号2比特，16-QAM每符号4比特。因此16-QAM频谱效率最高，BPSK最低。
- 抗噪声性能：BPSK星座点间距最大，误判概率最低；QPSK次之；16-QAM星座点最密集，在低SNR下BER最高。
- 实现复杂度：BPSK只需要一维实部判决，实现最简单；QPSK需要I/Q两路和四点判决；16-QAM需要幅度电平判决和功率归一化，实现复杂度最高。

本次性能测试还说明，单纯提高每个符号携带的比特数并不总是最优选择。高阶调制能够提高传输速率，但必须以足够好的信道质量为前提，否则误码率会明显上升。

### 5.3 遇到的问题与解决方法

描述实验过程中遇到的问题及解决方法：

1. **问题**：初始实现的BPSK星座图显示异常
   - **原因分析**：输入比特如果没有统一转换为NumPy数组，后续数学运算可能出现类型不一致或不能正确进行向量化计算的问题。
   - **解决方法**：增加`_as_binary_array()`辅助函数，将输入统一转换为一维整数数组，并检查取值只能为0或1。

2. **问题**：QPSK格雷码映射容易写反I/Q分量
   - **原因分析**：QPSK映射需要严格满足`00, 01, 11, 10`对应四个象限，如果直接凭直觉写条件判断，容易把某一位对应的轴搞反。
   - **解决方法**：先根据模板列出四个目标星座点，再反推I/Q分量的计算公式，并使用评分脚本中的测试用例验证四种比特对的输出。

3. **问题**：16-QAM平均功率需要归一化
   - **原因分析**：未归一化时I/Q电平为`±1, ±3`，平均符号功率不是1，会影响星座图尺度和BER性能比较。
   - **解决方法**：按照16-QAM理论平均功率计算归一化因子，输出符号统一除以 $\sqrt{10}$。

---

## 6. 实验心得与Copilot使用体会

### 6.1 实验心得

通过本实验，我对数字调制中的“比特到星座点映射”有了更直观的认识。BPSK、QPSK和16-QAM并不只是公式上的不同，它们在星座图中表现为点数、点距和几何结构的变化，而这些变化直接影响频谱效率和误码性能。

实验也加深了我对NumPy数组化编程的理解。使用`reshape`、`np.where`和复数数组可以非常简洁地表达调制过程，比逐个循环处理更清晰，也更适合信号处理仿真。通过BER测试，我进一步理解了SNR提高会降低误码率，以及高阶调制对噪声更敏感的原因。

### 6.2 AI助手使用体会

AI助手在本实验中对代码补全、解释映射关系、检查语法错误和整理报告结构帮助较大。特别是在处理QPSK和16-QAM格雷码映射时，AI可以快速给出实现思路和测试方法，提高开发效率。

但实验中的关键判断仍需要人工理解。例如，QPSK四个象限与比特对的对应关系、16-QAM为什么除以 $\sqrt{10}$、BER曲线为什么呈现不同下降速度，这些都不能只依赖代码生成结果，而需要结合通信原理进行验证。AI辅助编程更适合作为学习和调试工具，最终仍要通过测试和理论分析确认代码正确。

### 6.3 改进建议

建议实验平台可以在模板中增加一张标准星座图示例，方便学生对照检查输出结果；也可以补充一段关于SNR、AWGN和BER的简短说明，帮助学生理解性能测试曲线。对于选做部分，可以提供更明确的解调测试样例，使学生更容易判断自己的解调函数是否正确。

---

## 7. 参考文献

1. John G. Proakis, Masoud Salehi. 《数字通信（第五版）》. 电子工业出版社, 2011.
2. [维基百科 - 相移键控](https://zh.wikipedia.org/wiki/%E7%9B%B8%E7%A7%BB%E9%94%AE%E6%8E%A7)
3. [NumPy官方文档](https://numpy.org/doc/)
4. 本实验仓库`docs/theory_bpsk.md`、`docs/theory_qpsk.md`、`docs/theory_qam.md`理论说明文档。

---

## 附录：完整代码

如果需要，可以在此附上完整的代码实现。

```python
# modulation.py 完整代码
def bpsk_modulate(bits):
    bits = _as_binary_array(bits)
    return (1 - 2 * bits).astype(complex)


def qpsk_modulate(bits):
    bits = _as_binary_array(bits)
    if len(bits) % 2 != 0:
        raise ValueError("QPSK requires an even number of bits")

    bit_pairs = bits.reshape(-1, 2)
    i_values = np.where(bit_pairs[:, 1] == 0, 1, -1)
    q_values = np.where(bit_pairs[:, 0] == 0, 1, -1)
    return (i_values + 1j * q_values).astype(complex) / np.sqrt(2)


def qam16_modulate(bits):
    bits = _as_binary_array(bits)
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM requires the number of bits to be a multiple of 4")

    bit_groups = bits.reshape(-1, 4)

    def component_levels(two_bit_groups):
        first = two_bit_groups[:, 0]
        second = two_bit_groups[:, 1]
        return np.where(first == 0, 3 - 2 * second, -3 + 2 * second)

    i_values = component_levels(bit_groups[:, :2])
    q_values = component_levels(bit_groups[:, 2:])
    return (i_values + 1j * q_values).astype(complex) / np.sqrt(10)
```

---

**声明**：本实验报告内容真实，所有代码均为本人编写（或在AI助手辅助下完成），未抄袭他人成果。

**签名**：孟佳霖
**日期**：2026年4月29日
