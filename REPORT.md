# 数字调制解调实验报告

**实验名称**：数字调制解调实验
**学生姓名**：卫宏林
**学号**：2022300013
**实验日期**：2026年4月22日
**提交日期**：2026年4月22日

---

## 1. 实验目的

本实验旨在：

- 理解数字调制的基本原理，包括BPSK、QPSK和16-QAM。
- 掌握基于Python和NumPy的数字调制算法实现。
- 学习使用Matplotlib绘制星座图，直观分析调制符号分布。
- 体验AI编程助手（GitHub Copilot）在信号处理代码开发中的辅助作用。

---

## 2. 实验原理

### 2.1 BPSK调制原理

二进制相移键控（BPSK）使用两个相位表示两个比特值。映射关系如下：

比特 $b$ 映射到符号 $s$：

$$
 s = \begin{cases}
 +1, & b = 0 \\
 -1, & b = 1
 \end{cases}
$$

在本实验中，BPSK符号以复数形式表示为 $+1+0j$ 和 $-1+0j$，便于与其他复数调制方式统一处理。BPSK星座图只有两个点，分别位于实轴上的正、负方向。

优点：实现简单、抗噪声能力强。
缺点：频谱效率低，每个符号仅承载1比特信息。

### 2.2 QPSK调制原理

正交相移键控（QPSK）使用四个相位表示4种比特组合。实验采用格雷码映射，减少相邻星座点之间的比特翻转：

- `00 → (1+1j)/√2`
- `01 → (-1+1j)/√2`
- `11 → (-1-1j)/√2`
- `10 → (1-1j)/√2`

符号幅度归一化为单位功率，四个点分布在单位圆的45°、135°、225°、315°位置。

优点：频谱效率是BPSK的两倍，抗干扰性能仍较好。
缺点：解调复杂度较BPSK略高。

### 2.3 16-QAM调制原理

16-QAM通过幅度和相位组合实现16个星座点，每个符号承载4比特信息。I路和Q路分量取值为：`-3, -1, +1, +3`，并采用格雷码映射：

- `00 → +3`
- `01 → +1`
- `11 → -1`
- `10 → -3`

由于所有点平均功率为5，因此归一化因子为 $\sqrt{10}$，符号表示为：
$$ s = \frac{I + jQ}{\sqrt{10}} $$

16-QAM星座点排列为4×4方阵，频谱效率高，适合高数据速率场景，但对噪声更敏感。

---

## 3. 实验方法与步骤

### 3.1 环境配置

本实验使用Python 3.12、NumPy和Matplotlib。

实验过程中使用GitHub Copilot辅助编写和调试代码，主要步骤：

- 读取实验模板和任务说明
- 在 `src/modulation.py` 中实现调制函数
- 在 `src/utils.py` 中使用模板函数绘制星座图
- 运行Python脚本生成结果图像

### 3.2 BPSK实现

在 `src/modulation.py` 中实现了 `bpsk_modulate(bits)`：

```python
symbols = (1 - 2 * bits).astype(np.complex128)
```

该实现将比特0映射为 `+1`，比特1映射为 `-1`，并转换为复数类型。

### 3.3 QPSK实现

在 `src/modulation.py` 中实现了 `qpsk_modulate(bits)`：

- 先将比特序列重塑为 `(N/2, 2)`
- 对每两个比特计算索引 `2*b0 + b1`
- 按格雷码映射到归一化复数符号

映射数组为：

```python
gray_symbols = np.array([
    (1 + 1j) / np.sqrt(2),
    (-1 + 1j) / np.sqrt(2),
    (1 - 1j) / np.sqrt(2),
    (-1 - 1j) / np.sqrt(2)
])
```

### 3.4 16-QAM实现

在 `src/modulation.py` 中实现了 `qam16_modulate(bits)`：

- 将比特序列重塑为 `(N/4, 4)`
- 前两位映射I路，后两位映射Q路
- 使用格雷码数组 `[3, 1, -3, -1]`
- 最后除以 $\sqrt{10}$ 进行归一化

该实现生成的复数符号满足16-QAM星座点分布和平均功率归一化要求。

---

## 4. 实验结果

### 4.1 BPSK星座图

![BPSK星座图](results/bpsk_constellation.png)

**分析**：

- 星座图显示两个点，分别位于 `+1` 和 `-1`。
- 符号仅分布在实轴上，说明BPSK只使用相位变化传输比特。

### 4.2 QPSK星座图

![QPSK星座图](results/qpsk_constellation.png)

**分析**：

- 星座图显示四个对称点，位于单位圆的45°、135°、225°、315°。
- 由于归一化，所有点的幅度相等，符合单位功率要求。

### 4.3 16-QAM星座图

![16-QAM星座图](results/16qam_constellation.png)

**分析**：

- 星座图呈现4×4网格结构，I/Q分量分别为 `-3,-1,1,3`。
- 通过归一化处理，星座点分布在界限内，且点间距一致。

### 4.4 性能测试结果（选做）

本实验阶段主要完成了调制实现与星座图生成。当前项目中 `src/demodulation.py` 和 `src/performance_test.py` 包含解调及BER测试框架，后续可继续实现完整性能分析。

---

## 5. 结果分析与讨论

### 5.1 星座图对比分析

- BPSK：两个点，频谱效率最低，但对噪声最鲁棒。
- QPSK：四个点，频谱效率是BPSK的两倍，适合中低速率稳健通信。
- 16-QAM：16个点，频谱效率最高，但点间距离较小，对噪声敏感。

### 5.2 性能对比分析

- 频谱效率：16-QAM > QPSK > BPSK。
- 抗噪声性能：BPSK最强，其次是QPSK，16-QAM最弱。
- 实现复杂度：BPSK最简单，QPSK次之，16-QAM逻辑更复杂。

### 5.3 遇到的问题与解决方法

1. **问题**：一开始没有对QPSK符号幅度归一化。
   - **原因分析**：若不归一化，不同符号的功率不统一，影响比较。
   - **解决方法**：在符号生成时除以 `np.sqrt(2)`。

2. **问题**：16-QAM映射时容易混淆格雷码顺序。
   - **原因分析**：I/Q分量必须按 `00->3, 01->1, 11->-1, 10->-3` 映射。
   - **解决方法**：使用固定的映射数组 `np.array([3, 1, -3, -1])`。

3. **问题**：星座图显示比例不一致。
   - **原因分析**：Matplotlib坐标轴比例未设置为等比例。
   - **解决方法**：调用 `plt.gca().set_aspect('equal', adjustable='box')`。

---

## 6. 实验心得与Copilot使用体会

### 6.1 实验心得

通过本实验，我加深了对数字调制方式的理解，掌握了BPSK、QPSK和16-QAM的计算机实现方法。实际编程过程中，我也体会到数值归一化和符号映射对信号处理结果的重要性。

### 6.2 AI助手使用体会

本实验使用GitHub Copilot辅助参考函数实现和优化代码结构：

- Copilot帮助我快速生成 `reshape` 和映射逻辑代码。
- 对于归一化系数、格雷码映射等细节，Copilot提供了有用的提示。
- 最终代码仍由我自己检查和理解，避免直接复制。

### 6.3 改进建议

- 实验指导书可增加“解调与BER性能分析”的完整示例。
- 希望提供更多调制方案对比实验数据，例如QAM阶数扩展和AWGN性能曲线。
- 建议在模板中补充“常见错误解析”，帮助学生更快定位问题。

---

## 7. 参考文献

1. John G. Proakis, Masoud Salehi. 《数字通信（第五版）》. 电子工业出版社, 2011.
2. [维基百科 - 相移键控](https://zh.wikipedia.org/wiki/%E7%9B%B8%E7%A7%BB%E9%94%AE%E6%8E%A7)
3. [NumPy官方文档](https://numpy.org/doc/)
4. [Matplotlib官方文档](https://matplotlib.org/stable/index.html)

---

## 附录：关键代码

```python
# src/modulation.py

def bpsk_modulate(bits):
    symbols = (1 - 2 * bits).astype(np.complex128)
    return symbols


def qpsk_modulate(bits):
    bits_reshaped = bits.reshape(-1, 2)
    indices = bits_reshaped[:, 0] * 2 + bits_reshaped[:, 1]
    gray_symbols = np.array([
        (1 + 1j) / np.sqrt(2),
        (-1 + 1j) / np.sqrt(2),
        (1 - 1j) / np.sqrt(2),
        (-1 - 1j) / np.sqrt(2)
    ])
    return gray_symbols[indices]


def qam16_modulate(bits):
    bits_reshaped = bits.reshape(-1, 4)
    i_indices = bits_reshaped[:, 0] * 2 + bits_reshaped[:, 1]
    q_indices = bits_reshaped[:, 2] * 2 + bits_reshaped[:, 3]
    gray_values = np.array([3, 1, -3, -1])
    symbols = (gray_values[i_indices] + 1j * gray_values[q_indices]) / np.sqrt(10)
    return symbols
```

**声明**：本实验报告内容真实，以上代码为本人理解后完成。
