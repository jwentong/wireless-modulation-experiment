# 实验报告

**实验名称**：数字调制解调实验
**学生姓名**：王继熠
**学号**：2024280385
**实验日期**：2026年4月23日
**提交日期**：2026年4月29日

---

## 1. 实验目的

1. 理解数字调制与解调的基本原理，掌握星座图与误比特率（BER）之间的关系。
2. 完成 BPSK、QPSK、16-QAM 三种调制算法及对应解调算法的代码实现。
3. 学习使用 Python 与 NumPy 进行向量化信号处理和通信系统仿真。
4. 通过 AWGN 信道性能测试，比较不同调制方式在频谱效率和抗噪性能上的差异。
5. 体验 GitHub Copilot 辅助编程在代码实现、注释完善和调试中的作用。

---

## 2. 实验原理

### 2.1 BPSK 调制原理

BPSK（二进制相移键控）每个符号携带 1 bit 信息，通过相位 0° 与 180° 表示二进制 0 和 1。实验中采用实轴双点星座：

$$
s = 1 - 2b,
\quad b \in \{0,1\}
$$

等价写法：

$$
s = 
\begin{cases}
+1, & b=0 \\
-1, & b=1
\end{cases}
$$

解调时只需实部判决：

$$
\hat b =
\begin{cases}
0, & \Re\{r\} > 0 \\
1, & \Re\{r\} \le 0
\end{cases}
$$

特点：实现最简单、抗噪性能好，但频谱效率最低（1 bit/符号）。

### 2.2 QPSK 调制原理

QPSK（四相移键控）每个符号携带 2 bit 信息，使用四个相位点。实验采用格雷码映射：

- 00 → $(1+j)/\sqrt{2}$
- 01 → $(-1+j)/\sqrt{2}$
- 11 → $(-1-j)/\sqrt{2}$
- 10 → $(1-j)/\sqrt{2}$

其中除以 $\sqrt{2}$ 的目的是单位平均功率归一化。解调采用最小欧氏距离判决：对接收符号计算到 4 个理想星座点的距离，选择最近点并反查比特对。

特点：频谱效率高于 BPSK（2 bit/符号），在同等每比特能量条件下理论误码性能接近 BPSK，但实现复杂度有所增加。

### 2.3 16-QAM 调制原理

16-QAM 每个符号携带 4 bit 信息。将 4 bit 拆分为 I/Q 两路各 2 bit，并采用格雷码电平映射：

- 00 → +3
- 01 → +1
- 11 → -1
- 10 → -3

构造符号：

$$
s = I + jQ
$$

为保证公平比较，需要进行功率归一化。16-QAM 的平均符号能量为 10，因此：

$$
s_{norm} = \frac{s}{\sqrt{10}}
$$

解调时采用 I/Q 分离阈值判决（等价于二维最近点）：阈值取 $2/\sqrt{10}$，分别判决 I、Q 两路后拼接得到 4 bit。

特点：频谱效率最高（4 bit/符号），但星座点间距更小、抗噪性能相对较弱。

---

## 3. 实验方法与步骤

### 3.1 环境配置

1. 操作系统：Windows。
2. Python 环境：项目虚拟环境 `.venv`，Python 3.14.3。
3. 主要依赖：NumPy、Matplotlib、Pytest（见 `requirements.txt`）。
4. 使用 GitHub Copilot 辅助完成：

   - 调制/解调函数实现检查；
   - 关键算法步骤注释完善；
   - 自动测试与结果核验。

### 3.2 BPSK 实现

实现步骤：

1. 输入比特数组转为 NumPy 数组。
2. 检查输入仅包含 0/1。
3. 用向量化公式 `1 - 2*bits` 映射到符号。
4. 转为复数类型以统一接口。

关键代码：

```python
bits = np.asarray(bits)
if np.any((bits != 0) & (bits != 1)):
    raise ValueError("BPSK输入必须是只包含0和1的比特序列")
symbols = (1 - 2 * bits).astype(np.complex128)
```

### 3.3 QPSK 实现

实现步骤：

1. 校验输入为偶数长度且为 0/1。
2. `reshape(-1, 2)` 按 2 比特分组。
3. 使用格雷码字典查表映射到复平面点。
4. 除以 $\sqrt{2}$ 做单位功率归一化。

关键代码：

```python
bit_pairs = bits.reshape(-1, 2)
gray_map = {
    (0, 0): (1 + 1j),
    (0, 1): (-1 + 1j),
    (1, 1): (-1 - 1j),
    (1, 0): (1 - 1j),
}
symbols = np.array([gray_map[tuple(pair)] for pair in bit_pairs], dtype=np.complex128)
symbols /= np.sqrt(2)
```

### 3.4 16-QAM 实现

实现步骤：

1. 校验输入长度为 4 的倍数且为 0/1。
2. `reshape(-1, 4)` 按 4 比特分组。
3. 前两位映射 I、后两位映射 Q。
4. 构造复符号并除以 $\sqrt{10}$ 归一化。

关键代码：

```python
bit_groups = bits.reshape(-1, 4)
i_levels = np.array([gray_map[tuple(group[:2])] for group in bit_groups], dtype=np.float64)
q_levels = np.array([gray_map[tuple(group[2:])] for group in bit_groups], dtype=np.float64)
symbols = (i_levels + 1j * q_levels).astype(np.complex128)
symbols /= np.sqrt(10)
```

### 3.5 解调实现（选做，已完成）

1. BPSK：实部阈值判决。
2. QPSK：最小欧氏距离到 4 个参考点。
3. 16-QAM：I/Q 两路阈值分段判决后组合比特。

关键代码：

```python
real_part = np.real(symbols)
bits = np.where(real_part > 0, 0, 1).astype(np.int8)

ref_indices = np.array([0, 1, 3, 2])
ref_points = np.array([
   (1 + 1j) / np.sqrt(2),
   (-1 + 1j) / np.sqrt(2),
   (-1 - 1j) / np.sqrt(2),
   (1 - 1j) / np.sqrt(2),
], dtype=np.complex128)

bits_out = []
for sym in symbols:
   distances = np.abs(sym - ref_points) ** 2
   nearest_idx = ref_indices[np.argmin(distances)]
   bits_out.extend({0: (0, 0), 1: (0, 1), 3: (1, 1), 2: (1, 0)}[int(nearest_idx)])

threshold = 2 / np.sqrt(10)
def level_to_bits(x):
   if x > threshold:
      return (0, 0)
   if x > 0:
      return (0, 1)
   if x >= -threshold:
      return (1, 1)
   return (1, 0)

bits_out = []
for sym in symbols:
   bits_out.extend(level_to_bits(np.real(sym)))
   bits_out.extend(level_to_bits(np.imag(sym)))
```

---

## 4. 实验结果

### 4.1 BPSK 星座图

![BPSK星座图](results/bpsk_constellation.png)

分析：星座点集中在实轴两侧（约 +1 与 -1），虚部接近 0，符合 BPSK 双点星座特征。

### 4.2 QPSK 星座图

![QPSK星座图](results/qpsk_constellation.png)

分析：星座点分布在四个象限，点幅度接近 1，说明归一化正确；象限位置与格雷码映射一致。

### 4.3 16-QAM 星座图

![16-QAM星座图](results/16qam_constellation.png)

分析：形成规则 4×4 点阵，I/Q 分量取值在归一化后的四个离散电平，符合 16-QAM 结构。

### 4.4 BER 性能测试结果

![BER性能曲线](results/ber_comparison.png)

基于 10000 比特、SNR=0~14 dB（步长 2 dB）测试结果如下：


| SNR(dB) | BPSK BER | QPSK BER | 16-QAM BER |
| ------: | -------: | -------: | ---------: |
|       0 |   0.0810 |   0.1624 |     0.2804 |
|       2 |   0.0376 |   0.1053 |     0.2318 |
|       4 |   0.0118 |   0.0581 |     0.1854 |
|       6 |   0.0021 |   0.0232 |     0.1452 |
|       8 |   0.0001 |   0.0065 |     0.0977 |
|      10 |   0.0000 |   0.0007 |     0.0564 |
|      12 |   0.0000 |   0.0001 |     0.0241 |
|      14 |   0.0000 |   0.0000 |     0.0089 |

分析：随着 SNR 增加，三种方式 BER 都下降；在相同信噪比下，BPSK 最优、QPSK 次之、16-QAM 最差，与星座点最小距离大小规律一致。

---

## 5. 结果分析与讨论

### 5.1 星座图对比分析

1. BPSK 仅两个星座点，距离最大，判决最稳健。
2. QPSK 四点均匀分布，兼顾效率与可靠性。
3. 16-QAM 点数最多、最密集，对噪声和幅相失真最敏感。

### 5.2 性能对比分析

1. 频谱效率：BPSK（1 bit/符号） < QPSK（2 bit/符号） < 16-QAM（4 bit/符号）。
2. 抗噪声性能：BPSK > QPSK > 16-QAM（本实验 BER 数据验证了该趋势）。
3. 实现复杂度：BPSK 最低，QPSK 中等，16-QAM 最高（映射/判决状态更多、对归一化更敏感）。

### 5.3 遇到的问题与解决方法

1. 问题：初始代码中部分函数保留了 TODO 提示，容易与“未完成实现”混淆。

   - 原因分析：教学模板与已实现代码混合存在。
   - 解决方法：在关键算法步骤加入必要注释，明确映射、归一化和判决逻辑。
2. 问题：BER 对比图保存时出现中文字体缺失警告。

   - 原因分析：Matplotlib 默认字体不包含中文字形。
   - 解决方法：可在绘图代码中统一调用中文字体配置函数，或将标题改为英文避免警告。

---

## 6. 实验心得与 Copilot 使用体会

### 6.1 实验心得

1. 通过“调制-加噪-解调-BER”完整链路，建立了数字通信系统级认识。
2. 对格雷码映射和功率归一化的重要性有了更直观理解。
3. 掌握了 NumPy 向量化实现，可在保证可读性的同时提高计算效率。

### 6.2 AI 助手使用体会

1. 在样板代码补全、注释整理、测试执行方面，Copilot 明显提升了效率。
2. 在映射规则、阈值判决等通信原理问题上，仍需人工核对与理论验证。
3. AI 更适合作为“实现加速器”和“代码审阅助手”，而不是替代工程判断。

### 6.3 改进建议

1. 在实验模板中区分“必做/选做”函数，减少 TODO 与已实现代码的混淆。
2. 增加固定随机种子与多次蒙特卡洛平均，以提升 BER 曲线平滑性与可复现性。
3. 增加理论 BER 曲线叠加模块，便于实验结果与理论对照。

---

## 7. 参考文献

1. John G. Proakis, Masoud Salehi. 《数字通信（第五版）》. 电子工业出版社, 2011.
2. [维基百科 - 相移键控](https://zh.wikipedia.org/wiki/%E7%9B%B8%E7%A7%BB%E9%94%AE%E6%8E%A7)
3. [维基百科 - 正交振幅调制](https://zh.wikipedia.org/wiki/%E6%AD%A3%E4%BA%A4%E6%8C%AF%E5%B9%85%E8%B0%83%E5%88%B6)
4. [NumPy 官方文档](https://numpy.org/doc/)
5. [Matplotlib 官方文档](https://matplotlib.org/stable/users/index.html)

---

## 附录：可复现实验命令

```bash
python src/modulation.py
python src/demodulation.py
python src/performance_test.py
pytest grading/test_bpsk.py grading/test_qpsk.py grading/test_qam16.py -q
```

---

**声明**：本实验报告内容真实，所有代码均为本人编写（在 AI 助手辅助下完成），未抄袭他人成果。
**签名**：__王继熠__
**日期**：2026年4月23日
