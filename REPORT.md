# 数字调制解调实验报告

## 1. 实验目的
- 理解BPSK、QPSK、16-QAM等常见数字调制方式的基本原理。
- 掌握数字调制/解调算法的Python实现方法。
- 学会用Matplotlib绘制星座图，分析调制性能。
- 体验AI编程助手（Copilot）辅助开发的流程。

## 2. 实验原理
### 2.1 BPSK
- 0映射为+1，1映射为-1，星座点在实轴两端。
### 2.2 QPSK
- 每2比特一组，格雷码映射到复平面四个点，幅度归一化。
### 2.3 16-QAM
- 每4比特一组，I/Q分量取值{-3,-1,+1,+3}，格雷码映射，幅度归一化。

## 3. 实验方法与步骤
1. 阅读任务说明，配置Python环境，安装依赖。
2. 按要求实现BPSK、QPSK、16-QAM调制与解调函数。
3. 运行自动评分脚本，确保全部通过。
4. 运行性能测试，生成BER曲线。
5. 用Matplotlib绘制星座图，保存到results目录。

## 4. 实验结果
### 4.1 星座图
- ![BPSK](results/bpsk_constellation.png)
- ![QPSK](results/qpsk_constellation.png)
- ![16-QAM](results/16qam_constellation.png)

### 4.2 BER性能曲线
- ![BER对比](results/ber_comparison.png)

## 5. 结果分析与讨论
- BPSK抗噪声能力最强，16-QAM最弱，QPSK居中。
- 星座点越密集，对噪声越敏感。
- BER随SNR提升迅速下降，符合理论预期。

## 6. 实验心得与Copilot使用体会
- Copilot可自动补全注释和代码，大幅提升开发效率。
- 复杂判决逻辑和测试用例也能快速生成。
- 结合自动评分，极大减少调试时间。

## 7. 参考文献
1. 通信原理教材
2. 仓库内README与文档
3. [GitHub Copilot官方文档](https://docs.github.com/en/copilot)
