# 实验报告

**实验名称**：数字调制解调实验  
**学生姓名**：梁萱  
**学号**：2024280303  
**实验日期**：2026年4月24日  
**提交日期**：2026年4月28日

---

## 1. 实验目的

- 理解BPSK、QPSK、16-QAM三种数字调制方式的基本原理
- 使用Python实现调制和解调算法并可视化星座图
- 分析不同调制方式在噪声环境下的误码率性能
- 学习使用AI编程助手（Claude）辅助开发，熟悉GitHub协作流程

---

## 2. 实验原理

### 2.1 BPSK调制原理

BPSK每个符号携带1比特信息，映射规则如下：

$$s = \begin{cases} +1, & \text{if } b = 0 \\ -1, & \text{if } b = 1 \end{cases}$$

星座图上只有两个点，分布在实轴两端，Q分量为零。抗噪声能力最强，但频谱效率最低（1 bit/符号）。

### 2.2 QPSK调制原理

QPSK每个符号携带2比特信息，使用格雷码映射到四个复数点：

- 00 → $(1+j)/\sqrt{2}$（第一象限，45°）
- 01 → $(-1+j)/\sqrt{2}$（第二象限，135°）
- 11 → $(-1-j)/\sqrt{2}$（第三象限，225°）
- 10 → $(1-j)/\sqrt{2}$（第四象限，315°）

频谱效率是BPSK的两倍（2 bit/符号），抗噪声性能略低于BPSK。

### 2.3 16-QAM调制原理

16-QAM每个符号携带4比特信息，16个星座点排列成4×4网格。I/Q分量各取±1、±3四个值（归一化后为±0.316、±0.949）。频谱效率最高（4 bit/符号），但抗噪声性能最弱。

---

## 3. 实验方法与步骤

### 3.1 环境配置

使用Anaconda中的Python 3.13.5环境，安装numpy、matplotlib、scipy、pytest等依赖包。通过`python src/test_environment.py`验证环境配置成功。使用Claude AI助手辅助完成代码编写。

### 3.2 BPSK实现

```python
def bpsk_modulate(bits):
    symbols = 1 - 2 * bits  # 比特0→+1，比特1→-1
    return symbols
```

### 3.3 QPSK实现

```python
def qpsk_modulate(bits):
    bits = bits.reshape(-1, 2)
    mapping = {
        (0,0): (1+1j)/np.sqrt(2),
        (0,1): (-1+1j)/np.sqrt(2),
        (1,1): (-1-1j)/np.sqrt(2),
        (1,0): (1-1j)/np.sqrt(2),
    }
    symbols = np.array([mapping[(b[0],b[1])] for b in bits])
    return symbols
```

### 3.4 16-QAM实现

```python
def qam16_modulate(bits):
    bits = bits.reshape(-1, 4)
    gray_map = {(0,0):1, (0,1):3, (1,1):-3, (1,0):-1}
    symbols = []
    for b in bits:
        I = gray_map[(b[0],b[1])]
        Q = gray_map[(b[2],b[3])]
        symbols.append(complex(I, Q))
    return np.array(symbols) / np.sqrt(10)
```

---

## 4. 实验结果

### 4.1 BPSK星座图

![BPSK星座图](results/bpsk_constellation.png)

**分析**：两个星座点分别位于实轴(+1, 0)和(-1, 0)，Q分量为零，符合理论预期。

### 4.2 QPSK星座图

![QPSK星座图](results/qpsk_constellation.png)

**分析**：四个点均匀分布在单位圆上，每个象限各一个点，使用格雷码映射使相邻点只差1比特。

### 4.3 16-QAM星座图

![16-QAM星座图](results/16qam_constellation.png)

**分析**：16个点排列成规则的4×4网格，归一化后I/Q分量分别取±0.316和±0.949。

### 4.4 BER性能曲线

![BER性能曲线](results/ber_performance.png)

**分析**：BPSK在SNR=10dB时误码率接近零；QPSK性能比BPSK差约3dB；16-QAM需要更高SNR，但频谱效率最高。

---

## 5. 结果分析与讨论

### 5.1 星座图对比

三种调制方式的星座点数量分别为2、4、16，对应频谱效率1、2、4 bit/符号。星座点越多，相邻点间距越小，越容易因噪声导致误判。

### 5.2 性能对比

| 调制方式 | 频谱效率 | 抗噪声性能 | 实现复杂度 |
|---------|---------|-----------|-----------|
| BPSK | 1 bit/符号 | 最强 | 最低 |
| QPSK | 2 bit/符号 | 中等 | 中等 |
| 16-QAM | 4 bit/符号 | 最弱 | 最高 |

### 5.3 遇到的问题与解决方法

1. **问题**：git push时出现网络连接重置错误
   - **原因**：网络访问GitHub不稳定
   - **解决方法**：改用GitHub网页直接上传文件

2. **问题**：16-QAM星座图初始只显示4个点
   - **原因**：测试数据比特数不足，未覆盖全部16个状态
   - **解决方法**：使用所有16种4比特组合生成完整星座图

---

## 6. 实验心得

### 6.1 实验心得

通过本实验深刻理解了数字调制中频谱效率与抗噪声性能之间的权衡关系。BPSK最稳健但效率最低，16-QAM效率最高但对信道质量要求更高，这也是为什么4G/5G会根据信道质量动态切换调制方式。

### 6.2 AI助手使用体会

本实验使用Claude AI助手辅助完成代码编写。AI在代码框架生成、调试错误分析方面帮助很大，但理解算法原理和验证结果正确性仍需要自己思考。AI辅助编程可以大幅提高开发效率，但不能完全替代对原理的理解。

---

## 7. 参考文献

1. John G. Proakis, Masoud Salehi. 《数字通信（第五版）》. 电子工业出版社, 2011.
2. [NumPy官方文档](https://numpy.org/doc/)
3. [Matplotlib官方文档](https://matplotlib.org/)

---

**声明**：本实验报告内容真实，代码在AI助手辅助下完成，理解和验证均为本人独立完成。

**签名**：梁萱  
**日期**：2026年4月28日
