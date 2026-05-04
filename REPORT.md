**实验名称**：数字调制解调实验  
**学生姓名**：吴瑞炫  
**学号**：2024080712  
**实验日期**：2026年4月24日  
**提交日期**：2026年5月4日

---

## 1. 实验目的

• 理解数字调制的基本原理：BPSK、QPSK、16-QAM
• 掌握调制信号的生成方法和数学表达
• 理解星座图的含义及其与误码性能的关系
• 学会使用 AI 编程助手（GitHub Copilot）辅助编程
• 熟悉 GitHub 代码协作流程
• 培养通过代码验证通信理论的能力

---

## 2. 实验原理

### 2.1 BPSK调制原理

BPSK（Binary Phase Shift Keying，二进制相移键控）是最简单的数字调制方式。
• 基本映射关系：1比特/符号，比特0映射到+1，比特1映射到-1
• 星座图特征：实轴上两个点 [+1,−1] ，对应相位 0° 和 180°    
• 数学表达式: s=1−2b,b∈{0,1} ：
• 优缺点：
◦ 优点：实现简单，抗噪声性能最好
◦ 缺点：频谱效率低，仅1 bit/s/Hz

### 2.2 QPSK调制原理

QPSK（Quadrature Phase Shift Keying，四相相移键控）利用正交载波传输2比特信息。
• 基本映射关系：2比特/符号，采用格雷码映射
   00→(1+j)/ 根号2 （相位45°）
   ​01→(−1+j)/ 根号2（相位135°）
   11→(−1−j)/ 根号2（相位225°）
   ​10→(1−j)/ 根号2 （相位315°）
  
• 星座图特征：单位圆上均匀分布的4个点
• 归一化：除以根号2​使平均符号功率为1
• 优缺点：
◦ 优点：频谱效率是BPSK的2倍
◦ 缺点：抗噪声性能略差于BPSK

### 2.3 16-QAM调制原理

16-QAM（16-Quadrature Amplitude Modulation）同时改变载波的幅度和相位。
• 基本映射关系：4比特/符号，I/Q分量独立映射
◦ 前2位决定I分量（实部），后2位决定Q分量（虚部）
◦ 格雷码映射：00→+3,01→+1,11→−1,10→−3  
• 星座图特征：4×4正方形网格，共16个星座点
• 归一化：除以 根号10 使平均符号功率为1
• 优缺点：
◦ 优点：频谱效率高，4 bit/s/Hz
◦ 缺点：抗噪声性能较差，对信道质量要求高
---

## 3. 实验方法与步骤

### 3.1 环境配置

实验使用 VSCode + GitHub Copilot 进行开发。环境配置步骤：
1. 安装 VSCode 和 GitHub Copilot 扩展
2. 使用 Copilot Agent 辅助配置 Python 环境
3. 安装依赖：pip install numpy matplotlib
4. Fork 实验仓库并 Clone 到本地

### 3.2 BPSK实现

def bpsk_modulate(bits):
    symbols = 1 - 2 * bits
    symbols = symbols.astype(np.complex128)
    return symbols

### 3.3 QPSK实现

def qpsk_modulate(bits):
    if len(bits) % 2 != 0:
        raise ValueError("QPSK要求比特序列长度为偶数")
    
    bit_pairs = bits.reshape(-1, 2)
    indices = bit_pairs[:, 0] * 2 + bit_pairs[:, 1]
    
    mapping = np.array([1+1j, -1+1j, 1-1j, -1-1j], dtype=np.complex128)
    symbols = mapping[indices]
    symbols = symbols / np.sqrt(2)
    
    return symbols

### 3.4 16-QAM实现

def qam16_modulate(bits):
    if len(bits) % 4 != 0:
        raise ValueError("16-QAM要求比特序列长度为4的倍数")
    
    bit_groups = bits.reshape(-1, 4)
    
    gray_map = {(0, 0): 3, (0, 1): 1, (1, 1): -1, (1, 0): -3}
    
    I_values = np.array([gray_map[tuple(pair)] for pair in bit_groups[:, :2]])
    Q_values = np.array([gray_map[tuple(pair)] for pair in bit_groups[:, 2:]])
    
    symbols = I_values + 1j * Q_values
    symbols = symbols / np.sqrt(10)
    
    return symbols

---

## 4. 实验结果

### 4.1 BPSK星座图

https://www.kimi.com/chat/results/bpsk_constellation.png

**分析**：从图中可以看出BPSK有两个星座点，分别位于实轴上的+1和-1位置。两个点关于原点对称，相位差为180°，符合BPSK的调制原理。星座点分布在单位圆与实轴的交点处。

### 4.2 QPSK星座图
https://www.kimi.com/chat/results/qpsk_constellation.png

**分析**：QPSK星座图显示4个点均匀分布在单位圆上，相位分别为45°、135°、225°、315°。每个点对应2比特信息，采用格雷码映射使得相邻星座点之间只有1位比特差异，降低误码时的比特错误率。

### 4.3 16-QAM星座图

https://www.kimi.com/chat/results/16qam_constellation.png

**分析**：16-QAM星座图呈现4×4的正方形网格结构，共16个星座点。I路和Q路分量分别取值为±0.949和±0.316（归一化后），形成规则的网格分布。每个点对应4比特信息，频谱效率是QPSK的2倍。

### 4.4 性能测试结果（选做）

如果完成了BER性能测试，请在此展示结果：

![BER性能曲线](results/ber_comparison.png)

**分析**：从曲线可以看出...

---

## 5. 结果分析与讨论

### 5.1 星座图对比分析

从三种调制方式的星座图可以清晰看出：
• BPSK 只利用相位信息，实现最简单
• QPSK 利用相位和正交分量，频谱效率提升
• 16-QAM 同时利用幅度和相位，频谱效率最高但抗噪声性能最差

### 5.2 性能对比分析

频谱效率：BPSK(1) < QPSK(2) < 16-QAM(4)
• 抗噪声性能：BPSK > QPSK > 16-QAM
• 实现复杂度：BPSK < QPSK < 16-QAM
实际系统中需要根据信道条件选择合适的调制方式：信道质量好时选择高阶调制（如16-QAM），信道质量差时选择低阶调制（如BPSK）。

### 5.3 遇到的问题与解决方法

描述实验过程中遇到的问题及解决方法：

1. 问题：.gitignore 文件忽略了 results/ 目录，导致星座图无法提交到GitHub
• 原因分析：默认的 .gitignore 配置将 results/ 和 *.png 加入了忽略列表
• 解决方法：修改 .gitignore，删除或注释掉 results/ 和 *.png 的忽略规则，然后重新提交图片
2. 问题：git push 连接GitHub失败，报错 "Could not connect to server"
• 原因分析：网络连接问题或HTTPS被限制
• 解决方法：配置SSH密钥，使用SSH方式连接GitHub；或更换网络环境重试
3. 问题：运行测试时提示 ModuleNotFoundError: No module named 'pytest'
• 原因分析：未安装pytest测试框架
• 解决方法：执行 pip install pytest 安装依赖

---

## 6. 实验心得与Copilot使用体会

### 6.1 实验心得

通过本次实验，我对数字调制技术有了更深入的理解：
• 理论与实践结合：通过Python代码实现调制算法，验证了课堂上学到的理论知识，加深了对BPSK、QPSK、16-QAM原理的理解
• 星座图的直观性：星座图是分析调制性能的有力工具，可以直观地看出不同调制方式的差异
• 归一化的重要性：理解了为什么需要对星座图进行功率归一化，保证不同调制方式的公平比较
• 格雷码的优势：认识到格雷码映射在降低误码率方面的作用

### 6.2 AI助手使用体会

在本次实验中，我大量使用了 GitHub Copilot 辅助编程：
AI帮助很大的地方：
• 快速生成代码框架和函数模板
• 提供数学公式实现的建议（如格雷码映射）
• 帮助调试错误和解释报错信息
• 生成matplotlib绘图代码
需要人工思考的地方：
• 验证AI生成代码的正确性（如映射关系是否正确）
• 理解代码背后的数学原理
• 根据实验要求调整参数（如归一化因子）
• 代码的整合和模块化设计
对AI辅助编程的看法：AI编程助手是强大的工具，可以显著提高开发效率，但不能完全替代人工思考。使用AI时，需要理解其生成的代码，并能够独立验证正确性。

### 6.3 改进建议

1. 实验平台：建议优化 .gitignore 模板，避免默认忽略评分需要的文件
2. 测试框架：可以提供更详细的测试用例说明，帮助学生理解评分标准
3. 网络问题：建议提供国内镜像或代理配置指南，方便学生推送代码

---

## 7. 参考文献

1. John G. Proakis, Masoud Salehi. 《数字通信（第五版）》. 电子工业出版社, 2011.
2. [维基百科 - 相移键控](https://zh.wikipedia.org/wiki/%E7%9B%B8%E7%A7%BB%E9%94%AE%E6%8E%A7)
3. [NumPy官方文档](https://numpy.org/doc/)
4. 其他参考资料...

---

## 附录：完整代码

如果需要，可以在此附上完整的代码实现。

```python
# modulation.py 完整代码
...
```

---

**声明**：本实验报告内容真实，所有代码均为本人编写（或在AI助手辅助下完成），未抄袭他人成果。

**签名**：________  
**日期**：________
