# 实验报告

**实验名称**：数字调制解调实验  
**学生姓名**：郭晓冰
**学号**：2024080708
**实验日期**：2026年4月24日  
**提交日期**：2026年4月23日

---

## 1. 实验目的

本实验的主要目的是：
- 理解数字调制的基本原理，包括BPSK、QPSK和16-QAM
- 掌握使用Python和NumPy实现数字调制算法
- 学习信号处理和星座图的可视化
- 体验AI编程助手在代码开发中的辅助作用

---

## 2. 实验原理

### 2.1 BPSK调制原理

BPSK（Binary Phase Shift Keying，二进制相移键控）是一种最简单的数字调制方式。它将每个二进制比特映射到一个相位不同的载波上。

- **映射关系**：比特0映射到相位0°（+1），比特1映射到相位180°（-1）
- **星座图特征**：两个点位于实轴上，对称分布
- **优缺点**：实现简单，抗噪声性能好，但频谱效率低（1 bit/symbol）

公式：
$$
s = 1 - 2b
$$
其中b为二进制比特（0或1）。

### 2.2 QPSK调制原理

QPSK（Quadrature Phase Shift Keying，正交相移键控）使用两个正交载波，每个符号携带2个比特。

- **映射关系**：使用格雷码映射，四个星座点位于单位圆上
- **星座图特征**：四个点等间距分布在圆周上
- **优缺点**：频谱效率是BPSK的两倍，抗噪声性能稍差于BPSK

符号映射：
- 00 → (1+1j)/√2
- 01 → (-1+1j)/√2  
- 11 → (-1-1j)/√2
- 10 → (1-1j)/√2

### 2.3 16-QAM调制原理

16-QAM（16-Quadrature Amplitude Modulation，16正交幅度调制）每个符号携带4个比特。

- **映射关系**：I/Q分量取{-3,-1,1,3}，使用格雷码
- **星座图特征**：16个点排列成4×4方格
- **优缺点**：频谱效率高，但对噪声更敏感

归一化后平均功率为1。

---

## 3. 实验方法与步骤

### 3.1 环境配置

使用GitHub Copilot配置Python环境，安装了numpy、scipy、matplotlib包。环境配置顺利，无问题。

### 3.2 BPSK实现

BPSK实现使用数学运算：`symbols = (1 - 2 * bits).astype(complex)`

```python
def bpsk_modulate(bits):
    symbols = (1 - 2 * bits).astype(complex)
    return symbols
```

### 3.3 QPSK实现

将比特序列reshape成(N/2, 2)，然后根据格雷码映射计算I/Q分量，最后归一化。

```python
def qpsk_modulate(bits):
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")
    
    bits_reshaped = bits.reshape(-1, 2)
    I = 1 - 2 * bits_reshaped[:, 0]
    Q = 1 - 2 * bits_reshaped[:, 1]
    symbols = (I + 1j * Q) / np.sqrt(2)
    
    return symbols
```

### 3.4 16-QAM实现

将比特序列reshape成(N/4, 4)，前2位映射I分量，后2位映射Q分量，使用格雷码映射{-3,-1,1,3}，然后归一化。

```python
def qam16_modulate(bits):
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")
    
    bits_reshaped = bits.reshape(-1, 4)
    I_bits = bits_reshaped[:, :2]
    Q_bits = bits_reshaped[:, 2:]
    
    def map_bits(b):
        if np.array_equal(b, [0, 0]): return 3
        elif np.array_equal(b, [0, 1]): return 1
        elif np.array_equal(b, [1, 1]): return -1
        else: return -3
    
    I = np.array([map_bits(row) for row in I_bits])
    Q = np.array([map_bits(row) for row in Q_bits])
    symbols = (I + 1j * Q) / np.sqrt(10)
    
    return symbols
```

---

## 4. 实验结果

### 4.1 BPSK星座图

![BPSK星座图](results/bpsk_constellation.png)

**分析**：BPSK星座图显示两个点位于实轴的+1和-1位置，符合理论预期。所有符号都严格位于实轴上。

### 4.2 QPSK星座图

![QPSK星座图](results/qpsk_constellation.png)

**分析**：QPSK星座图显示四个点位于单位圆的四个象限，幅度均为1/√2 ≈ 0.707，相位分别为45°、135°、225°、315°，符合格雷码映射。

### 4.3 16-QAM星座图

![16-QAM星座图](results/16qam_constellation.png)

**分析**：16-QAM星座图显示16个点排列成正方形网格，I/Q分量取值{-3,-1,1,3}/√10，形成了完整的16-QAM星座图。

### 4.4 性能测试结果（选做）

![BER性能曲线](results/ber_comparison.png)

**分析**：
- BPSK在低SNR下表现最好，0 dB时BER约为0.079，6 dB时BER降到0.0025，8 dB以后基本达到0。
- QPSK在0 dB时BER约为0.16，8 dB时BER约为0.0062，10 dB以内性能逐步改善。
- 16-QAM的抗噪声能力最弱，0 dB时BER约为0.29，10 dB时仍有约0.0607，14 dB时才接近0.01。

从BER对比图可以看出，随着调制阶数增加，频谱效率提高的同时，对噪声的敏感度也显著增加。

---

## 5. 结果分析与讨论

### 5.1 星座图对比分析

- **BPSK**：最简单，只有两个点，抗噪声能力最强
- **QPSK**：四个点，频谱效率提高一倍，相邻点距离相同
- **16-QAM**：16个点，频谱效率最高，但星座点密集，对噪声敏感

### 5.2 性能对比分析

| 调制方式 | 比特率 | 抗噪声性能 | 实现复杂度 |
|---------|-------|-----------|-----------|
| BPSK    | 1 bit/symbol | 最好     | 最低     |
| QPSK    | 2 bit/symbol | 良好     | 中等     |
| 16-QAM  | 4 bit/symbol | 最差     | 最高     |

从本次BER性能测试结果看，BPSK的抗噪声能力最强，QPSK次之，16-QAM对噪声最为敏感。

### 5.3 遇到的问题与解决方法

1. **问题**：初始实现16-QAM时映射错误
   - **原因分析**：对格雷码映射理解不准确
   - **解决方法**：查阅资料确认映射关系并修正代码

2. **问题**：运行测试时模块导入错误
   - **原因分析**：Python路径问题
   - **解决方法**：添加src目录到sys.path

---

## 6. 实验心得与Copilot使用体会

### 6.1 实验心得

通过本实验，深入理解了数字调制的原理和实现方法，掌握了使用NumPy进行信号处理的技巧，提高了调试Python代码的能力。

### 6.2 AI助手使用体会

GitHub Copilot在代码实现和环境配置方面提供了很大帮助，能够快速生成代码框架和修复错误，但在算法理解和逻辑设计方面仍需人工思考。

### 6.3 改进建议

建议增加更多性能测试内容，如BER曲线绘制。

---

## 7. 参考文献

1. John G. Proakis, Masoud Salehi. 《数字通信（第五版）》. 电子工业出版社, 2011.
2. [维基百科 - 相移键控](https://zh.wikipedia.org/wiki/%E7%9B%B8%E7%A7%BB%E9%94%AE%E6%8E%A7)
3. [NumPy官方文档](https://numpy.org/doc/)

---

**声明**：本实验报告内容真实，所有代码均为本人编写（在AI助手辅助下完成），未抄袭他人成果。

**签名**：郭晓冰
**日期**：2026年4月23日