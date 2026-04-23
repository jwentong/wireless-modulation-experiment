# 数字调制解调实验

## 📚 实验概述

本实验要求学生实现常见的数字调制方式（BPSK、QPSK、16-QAM），生成星座图，并选做性能分析。实验使用 Python + NumPy + Matplotlib，鼓励使用 AI 编程助手（GitHub Copilot / Claude Code）。

**实验时长**：2小时（120分钟）
- 第一小时：教师讲解和演示
- 第二小时：学生动手实验

**提交截止**：实验课后7天（下周四 23:59）

---

## 🎯 实验目标

1. 理解数字调制的基本原理（BPSK、QPSK、16-QAM）
2. 实现调制算法并可视化星座图
3. 学习使用 AI 编程助手辅助开发
4. 熟悉 GitHub 协作流程和自动评分系统

---

## 📝 实验任务

### 任务0：环境准备（5分）
- 使用 Copilot Agent 配置 Python 环境
- Fork 本仓库到个人账号
- Clone 到本地并安装依赖

### 任务1：BPSK 调制（25分）✅ 必做
在 `src/modulation.py` 中实现 `bpsk_modulate()` 函数：
- 输入：比特序列 `[0, 1, 0, 1, ...]`
- 输出：符号序列 `[+1, -1, +1, -1, ...]`
- 映射关系：`0 → +1`, `1 → -1`
- 生成星座图并保存到 `results/bpsk_constellation.png`

### 任务2：QPSK 调制（25分）✅ 必做
在 `src/modulation.py` 中实现 `qpsk_modulate()` 函数：
- 每2比特一组
- 格雷码映射：
  - `00 → (1+1j)/√2` (45°)
  - `01 → (-1+1j)/√2` (135°)
  - `11 → (-1-1j)/√2` (225°)
  - `10 → (1-1j)/√2` (315°)
- 生成星座图并保存到 `results/qpsk_constellation.png`

### 任务3：16-QAM 调制（20分）✅ 必做
在 `src/modulation.py` 中实现 `qam16_modulate()` 函数：
- 每4比特一组
- I/Q 分量取值：`-3, -1, +1, +3`
- 生成16个符号的星座图
- 保存到 `results/16qam_constellation.png`

### 任务4：解调实现（10分）⭐ 选做
在 `src/demodulation.py` 中实现解调函数：
- `bpsk_demodulate()`：判决准则
- `qpsk_demodulate()`：最小欧氏距离判决
- `qam16_demodulate()`：最小欧氏距离判决

### 任务5：BER 性能分析（10分）⭐ 选做
在 `src/performance_test.py` 中完成性能测试：
- 生成随机比特序列
- 调制 → 添加 AWGN 噪声 → 解调
- 扫描不同 SNR（0~15 dB）
- 绘制 BER vs SNR 曲线（对数坐标）

### 任务6：实验报告（15分）📄 可课后完成
在根目录创建 `REPORT.md`，包含：
1. 实验目的
2. 实验原理（简述BPSK/QPSK/QAM）
3. 实验方法与步骤
4. 实验结果（插入星座图）
5. 结果分析与讨论
6. 实验心得与 Copilot 使用体会
7. 参考文献

⚠️ **重要**：实验结果（代码+星座图）必须提交，实验报告可以后续完善。

---

## 🚀 快速开始

### 1. 获取实验代码（第一小时前10分钟）

#### 步骤 1.1：Fork 模板仓库

1. **访问模板仓库**：https://github.com/jwentong/wireless-modulation-experiment

2. **点击右上角的 "Fork" 按钮**（或 "Use this template"）
   - 如果看到 "Use this template" 按钮，点击它选择 "Create a new repository"
   - 如果只有 "Fork" 按钮，直接点击

3. **填写你的仓库信息**：
   - Repository name: `wireless-modulation-experiment`（保持不变）
   - Description: 数字调制解调实验
   - 选择 **Public**（推荐）或 **Private**
   - ✅ 勾选 "Copy the main branch only"
   - 点击 **"Create fork"** 或 **"Create repository"**

4. **等待几秒**，仓库会出现在你的账号下：
   - `https://github.com/你的用户名/wireless-modulation-experiment`

#### 步骤 1.2：Clone 到本地

**Windows 用户（PowerShell）**：
```powershell
# 1. 打开 PowerShell，进入你的工作目录
cd C:\Users\你的用户名\Desktop

# 2. Clone 仓库（替换成你的用户名）
git clone https://github.com/你的用户名/wireless-modulation-experiment.git

# 3. 进入目录
cd wireless-modulation-experiment
```

**Mac/Linux 用户**：
```bash
# 1. 打开终端，进入工作目录
cd ~/Desktop

# 2. Clone 仓库（替换成你的用户名）
git clone https://github.com/你的用户名/wireless-modulation-experiment.git

# 3. 进入目录
cd wireless-modulation-experiment
```

#### 步骤 1.3：在 VS Code 中打开

```bash
# 方法1: 使用命令行
code .

# 方法2: 手动打开
# 启动 VS Code → File → Open Folder → 选择 wireless-modulation-experiment
```

### 2. 环境配置（第一小时 10-20 分钟）

#### 方法1：使用 Copilot Agent 自动配置（推荐）⭐

1. **打开 VS Code Copilot Chat**（快捷键：`Ctrl+I` 或 `Cmd+I`）

2. **输入提示词**：
   ```
   @workspace 请帮我配置 Python 开发环境，需要安装以下依赖：
   - numpy
   - scipy
   - matplotlib
   - pytest
   - pylint
   ```

3. **等待 Copilot Agent 执行**，它会自动：
   - 检测 Python 版本
   - 创建虚拟环境（如果需要）
   - 安装所有依赖包

4. **确认安装成功**

#### 方法2：手动安装（备选）

**使用 pip 安装**：
```bash
# 确保 Python 版本 >= 3.8
python --version

# 安装依赖
pip install -r requirements.txt

# 或者使用国内镜像（更快）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**使用 conda 安装**：
```bash
# 创建新环境
conda create -n modulation python=3.11

# 激活环境
conda activate modulation

# 安装依赖
pip install -r requirements.txt
```

#### 步骤 2.3：验证环境

运行环境测试脚本：

```bash
python src/test_environment.py
```

**预期输出**：
```
==================================================
数字调制解调实验 - 环境测试
==================================================

1. 检查Python版本...
Python版本: 3.11.x
✅ Python版本符合要求

2. 检查依赖包...
✅ NumPy 1.24.0 已安装
✅ SciPy 1.10.0 已安装
✅ Matplotlib 3.7.0 已安装
✅ Pytest 7.3.0 已安装

3. 测试NumPy操作...
✅ NumPy基本操作测试通过

4. 测试Matplotlib绘图...
✅ Matplotlib绘图测试通过

==================================================
🎉 所有测试通过！环境配置正确。
你可以开始实验了！
==================================================
```

如果看到 🎉，说明环境配置成功！

### 3. 完成实验（第一小时 20 分钟 - 第二小时 40 分钟）

#### 步骤 3.1：阅读理论文档（10分钟）

在开始编码前，先理解原理：

1. **BPSK原理**：阅读 [docs/theory_bpsk.md](docs/theory_bpsk.md)
   - 理解比特到符号的映射关系
   - 查看星座图示例：[examples/bpsk_constellation.png](examples/bpsk_constellation.png)

2. **QPSK原理**：阅读 [docs/theory_qpsk.md](docs/theory_qpsk.md)
   - 理解格雷码映射
   - 查看星座图示例：[examples/qpsk_constellation.png](examples/qpsk_constellation.png)

3. **16-QAM原理**：阅读 [docs/theory_qam.md](docs/theory_qam.md)
   - 理解I/Q分量映射
   - 查看星座图示例：[examples/16qam_constellation.png](examples/16qam_constellation.png)

#### 步骤 3.2：实现 BPSK 调制（20分钟）

1. **打开代码文件**：
   - 在 VS Code 中打开 `src/modulation.py`
   - 找到 `bpsk_modulate()` 函数

2. **阅读函数文档**：
   ```python
   def bpsk_modulate(bits):
       """
       BPSK (Binary Phase Shift Keying) 调制
       
       任务要求：
       - 输入：二进制比特序列（NumPy数组），元素为0或1
       - 输出：调制后的复数符号序列
       - 映射规则：
           比特 0 → 符号 +1
           比特 1 → 符号 -1
       """
   ```

3. **使用 Copilot 辅助编写**：
   
   **方法1：通过注释引导**
   ```python
   def bpsk_modulate(bits):
       # 将比特0映射到+1，比特1映射到-1
       # 使用numpy的向量化操作
       
       # [按 Tab 键，Copilot 会自动补全]
   ```

   **方法2：使用 Copilot Chat**
   - 选中整个函数
   - 按 `Ctrl+I` 打开 Copilot Chat
   - 输入提示词：
     ```
     请实现这个BPSK调制函数，要求：
     1. 比特0映射到+1，比特1映射到-1
     2. 使用numpy的向量化操作，避免循环
     3. 返回复数数组
     ```

4. **运行测试**：
   ```bash
   python src/modulation.py
   ```

   **预期输出**：
   ```
   1. 测试BPSK调制...
      输入比特数: 1000
      输出符号数: 1000
      唯一符号: [-1.+0.j  1.+0.j]
      ✅ BPSK测试通过
   ```

5. **检查星座图**：
   - 打开 `results/bpsk_constellation.png`
   - 确认有两个点在 +1 和 -1 位置

#### 步骤 3.3：实现 QPSK 调制（30分钟）

1. **找到 `qpsk_modulate()` 函数**

2. **提示词示例**：
   ```
   请实现QPSK调制，要求：
   1. 每2个比特映射到1个符号
   2. 使用格雷码映射：00→(1+1j)/√2, 01→(-1+1j)/√2, 11→(-1-1j)/√2, 10→(1-1j)/√2
   3. 符号归一化到单位能量
   ```

3. **运行测试并检查星座图**

#### 步骤 3.4：实现 16-QAM 调制（30分钟）

1. **找到 `qam16_modulate()` 函数**

2. **提示词示例**：
   ```
   请实现16-QAM调制：
   1. 每4个比特映射到1个符号
   2. 前2位映射到I分量，后2位映射到Q分量
   3. 使用格雷码：00→+3, 01→+1, 11→-1, 10→-3
   4. 除以√10进行归一化
   ```

3. **运行测试并检查星座图**

#### 步骤 3.5：编写实验报告（40分钟）

1. **复制报告模板**：
   ```bash
   cp REPORT_TEMPLATE.md REPORT.md
   ```

2. **打开 `REPORT.md` 填写内容**：
   - 实验目的
   - 实验原理（可参考 docs/ 中的文档）
   - 实验方法与步骤
   - 实验结果（插入星座图）
   - 结果分析与讨论
   - 实验心得与 Copilot 使用体会
   - 参考文献

3. **插入星座图**：
   ```markdown
   ![BPSK星座图](results/bpsk_constellation.png)
   ```

4. **报告要求**：
   - 字数 ≥ 1000 字
   - 包含至少 3 张星座图
   - 分析要有深度，不能只是描述
   - 说明 AI 助手的使用情况

### 4. 提交到 GitHub（第二小时 40-50 分钟）

#### 步骤 4.1：保存并提交代码

**在 VS Code 中**：

1. **保存所有修改的文件**（`Ctrl+S` 或 `Cmd+S`）

2. **打开源代码管理面板**：
   - 点击左侧的 "Source Control" 图标（或按 `Ctrl+Shift+G`）

3. **查看修改的文件**：
   - 你会看到所有修改的文件列表
   - `src/modulation.py`（红色M表示Modified）
   - `results/` 目录下的星座图

4. **暂存所有更改**：
   - 点击 "Changes" 旁边的 `+` 号
   - 或者点击每个文件旁边的 `+`

5. **填写提交信息**：
   - 在上方输入框输入：`完成 BPSK 和 QPSK 调制实现`
   - 点击 ✓ 提交（或按 `Ctrl+Enter`）

**或使用命令行**：

```bash
# 查看修改的文件
git status

# 添加所有修改
git add .

# 提交（写清楚做了什么）
git commit -m "完成 BPSK 和 QPSK 调制实现

- 实现了 bpsk_modulate 函数
- 实现了 qpsk_modulate 函数
- 生成了对应的星座图"

# 推送到 GitHub
git push origin main
```

**提交信息建议**：
- ✅ `完成 BPSK 和 QPSK 调制`
- ✅ `实现 16-QAM 调制和星座图生成`
- ✅ `添加 BER 性能测试`
- ❌ `update`（太简略）
- ❌ `作业提交`（不够具体）

#### 步骤 4.2：创建 Pull Request

1. **访问你的 GitHub 仓库**：
   - `https://github.com/你的用户名/wireless-modulation-experiment`

2. **GitHub 会显示黄色横幅**：
   - "Your recently pushed branches: main (x minutes ago)"
   - 点击 **"Compare & pull request"** 按钮

   如果没有看到，手动创建：
   - 点击 "Pull requests" 标签
   - 点击绿色的 "New pull request" 按钮

3. **设置 PR 的目标**：
   - **Base repository**: `jwentong/wireless-modulation-experiment`（教师仓库）
   - **Base branch**: `main`
   - **Head repository**: `你的用户名/wireless-modulation-experiment`（你的仓库）
   - **Compare branch**: `main`

4. **填写 PR 信息**：

   **标题示例**：
   ```
   [学号] 姓名 - 数字调制解调实验提交
   ```
   例如：`[2021001] 张三 - 数字调制解调实验提交`

   **描述示例**：
   ```markdown
   ## 完成情况

   - [x] 任务0: 环境配置
   - [x] 任务1: BPSK调制
   - [x] 任务2: QPSK调制
   - [x] 任务3: 16-QAM调制
   - [ ] 任务4: 解调实现（选做）
   - [ ] 任务5: BER性能分析（选做）
   - [x] 任务6: 实验报告

   ## 说明

   - 所有必做任务已完成
   - 星座图已正确生成在 `results/` 目录
   - 使用 GitHub Copilot 辅助完成代码编写
   - 实验报告见根目录 `REPORT.md`

   ## 遇到的问题

   1. 初始对格雷码映射理解有误，后查阅文档修正
   2. 星座图归一化时忘记除以√10，已修复

   ## 实验心得

   通过本次实验，我深入理解了数字调制的原理...
   ```

5. **点击 "Create pull request"** 绿色按钮

### 5. 查看自动评分（第二小时 50-60 分钟）

#### 步骤 5.1：等待 GitHub Actions 运行

1. **PR 创建后**，页面会跳转到你的 PR 详情页

2. **查看运行状态**：
   - 在 PR 页面中间，你会看到 **"自动评分系统"** 的检查项
   - 状态图标：
     - 🟡 黄色圆圈：正在运行
     - ✅ 绿色对勾：运行成功
     - ❌ 红色叉号：运行失败

3. **点击 "Details" 查看详情**（可选）：
   - 可以看到每个步骤的执行过程
   - 环境安装、测试运行、评分计算等

#### 步骤 5.2：查看评分结果

**等待 3-5 分钟后**，机器人会在 PR 下方发布评论：

```
🤖 自动评分结果

总分: 80/100
等级: B (良好)

==================================================

1️⃣ 环境配置测试 (5分)
  ✅ 环境测试通过: +5分

2️⃣ BPSK调制测试 (25分)
  通过测试: 6/6
  得分: 25/25
  ✅ 基本映射规则 ✅
  ✅ 全0输入测试 ✅
  ✅ 全1输入测试 ✅
  ✅ 符号取值验证 ✅
  ✅ 随机序列测试 ✅
  ✅ 星座图文件存在 ✅

3️⃣ QPSK调制测试 (25分)
  通过测试: 9/9
  得分: 25/25
  ✅ 所有测试通过

4️⃣ 16-QAM调制测试 (20分)
  通过测试: 8/9
  得分: 18/20
  ⚠️ 部分测试未通过：
  - 符号分布均匀性测试失败

5️⃣ 实验报告检查 (15分)
  报告得分: 12/15
  📋 章节完整性: 5/6
  ✅ 字数达标 (1523字)
  ✅ 包含图片引用 (4张)
  ⚠️ 缺少"参考文献"章节

6️⃣ 代码质量检查
  pylint评分: 8.5/10
  ✅ 代码质量优秀: +5分

==================================================

💡 改进建议：
1. 检查16-QAM的符号生成是否真正随机
2. 补充实验报告的"参考文献"章节
3. 部分代码注释可以更详细

⏰ 评分时间: 2026-04-21 15:23:45 (UTC+8)
```

#### 步骤 5.3：根据反馈修改（可选）

如果评分未达到预期：

1. **查看失败的测试项**
2. **在本地修改代码**
3. **重新提交**：
   ```bash
   git add .
   git commit -m "修复16-QAM符号分布问题"
   git push origin main
   ```
4. **GitHub Actions 会自动重新评分**
5. **可以多次提交**，系统会取最新的评分

#### 步骤 5.4：下载详细报告

1. 在 PR 页面点击 **"Checks"** 标签
2. 点击 **"自动评分系统"**
3. 滚动到底部，找到 **"Artifacts"** 部分
4. 点击 **"grading-report"** 下载压缩包
5. 解压后可查看详细的测试日志和评分细节

---

## 💡 使用 AI 助手的提示

### 推荐的提问模板

**调制实现**：
```
"请用 Python 实现 BPSK 调制，输入二进制序列，
输出复数符号序列，0映射到+1，1映射到-1"
```

**星座图绘制**：
```
"请用 matplotlib 画出 QPSK 的星座图，
四个点在单位圆上均匀分布"
```

**代码调试**：
```
"我的代码报错了：[粘贴错误信息]，请帮我找出问题"
```

**代码解释**：
```
"请解释这段代码的含义：[粘贴代码]"
```

### AI 助手使用建议

✅ 先理解原理，再使用 AI 生成代码  
✅ 生成的代码要仔细阅读理解  
✅ 可以让 AI 解释代码的实现逻辑  
✅ 遇到错误时，将完整错误信息粘贴给 AI  
✅ 尝试修改参数观察结果变化  

❌ 不要完全依赖 AI，要培养独立思考能力  
❌ 不要直接提交 AI 生成的代码而不理解其含义  

---

## 📊 评分标准

| 评分项 | 分值 | 评分细则 |
|--------|------|----------|
| 环境配置 | 5分 | 成功运行环境测试脚本 |
| BPSK调制 | 25分 | 映射正确(15分) + 星座图(10分) |
| QPSK调制 | 25分 | 映射正确(15分) + 星座图(10分) |
| 16-QAM调制 | 20分 | 映射正确(12分) + 星座图(8分) |
| 解调实现 | 10分 | 正确实现解调算法（选做加分） |
| BER性能 | 10分 | 生成BER曲线并分析（选做加分） |
| 实验报告 | 15分 | 完整性(8分) + 分析深度(7分) |
| 代码质量 | -10~+5分 | pylint评分 > 8.0加分，< 5.0扣分 |

**总分**：基础任务（0-3+报告）满分75分，选做任务可额外加分20分。

---

## 📁 仓库结构

```
wireless-modulation-experiment/
├── README.md                    # 本文件
├── REQUIREMENTS.md              # 详细任务要求
├── .github/workflows/
│   └── grading.yml              # 自动评分工作流
├── docs/
│   ├── theory_bpsk.md           # BPSK原理
│   ├── theory_qpsk.md           # QPSK原理
│   ├── theory_qam.md            # QAM原理
│   └── copilot_guide.md         # Copilot使用指南
├── src/
│   ├── modulation.py            # 调制函数（学生填充）
│   ├── demodulation.py          # 解调函数（学生填充）
│   ├── performance_test.py      # 性能测试（学生填充）
│   ├── utils.py                 # 工具函数（已实现）
│   └── test_environment.py      # 环境测试脚本
├── grading/                     # 评分脚本（学生不可见）
│   ├── test_bpsk.py
│   ├── test_qpsk.py
│   ├── test_qam16.py
│   ├── check_report.py
│   └── calculate_grade.py
├── examples/                    # 示例输出
│   ├── bpsk_constellation.png
│   ├── qpsk_constellation.png
│   └── ber_curve_example.png
├── results/                     # 学生结果（自动创建）
├── requirements.txt             # Python依赖
├── .gitignore
└── REPORT_TEMPLATE.md           # 报告模板
```

---

## ❓ 常见问题

### 环境配置相关

**Q1: Python版本要求是什么？**  
A: Python 3.8 或更高版本。推荐使用 Python 3.11。

查看版本：
```bash
python --version
```

**Q2: 依赖安装失败怎么办？**  
A: 尝试使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q3: `ModuleNotFoundError: No module named 'numpy'`**  
A: 说明依赖未正确安装，重新运行：
```bash
pip install numpy scipy matplotlib pytest pylint
```

**Q4: VS Code 找不到 Python 解释器？**  
A: 
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Python: Select Interpreter"
3. 选择正确的 Python 版本

### Git 和 GitHub 相关

**Q5: 我不会用 Git，怎么办？**  
A: 参考 [Git 快速入门](docs/git_quickstart.md)，或者课上会有 10 分钟的快速演示。

**Q6: GitHub Copilot 需要付费吗？**  
A: 学生可以免费使用！访问 https://education.github.com/ 申请 GitHub Student Pack。

**Q7: 忘记提交某个文件怎么办？**  
A: 
```bash
git add 遗漏的文件
git commit --amend --no-edit
git push -f origin main  # 注意：-f 会强制覆盖
```

**Q8: 如何撤销上一次提交？**  
A:
```bash
# 保留修改，只撤销commit
git reset --soft HEAD~1

# 完全撤销，丢弃修改
git reset --hard HEAD~1
```

### 实验代码相关

**Q9: 我的代码运行报错，怎么办？**  
A: 
1. 仔细阅读错误信息
2. 将错误信息复制给 Copilot Chat 求助
3. 检查数组维度、数据类型是否正确
4. 向教师/助教求助

**Q10: 星座图应该是什么样的？**  
A: 查看 `examples/` 目录中的示例图片：
- BPSK: 2个点在实轴上
- QPSK: 4个点在单位圆上，呈十字形
- 16-QAM: 16个点排列成4×4方阵

**Q11: 如何调试 NumPy 数组？**  
A: 使用 `print()` 查看数组内容：
```python
print(f"数组形状: {symbols.shape}")
print(f"数组内容: {symbols[:10]}")  # 显示前10个元素
print(f"唯一值: {np.unique(symbols)}")
```

**Q12: 生成的星座图不对？**  
A: 检查：
1. 映射关系是否正确
2. 归一化因子是否正确（QPSK: √2, 16-QAM: √10）
3. 比特分组是否正确
4. 是否使用了格雷码映射

### 提交和评分相关

**Q13: 我可以多次提交吗？**  
A: 可以！在截止时间前可以随意修改和提交，系统会取**最后一次评分**。

**Q14: GitHub Actions 运行失败怎么办？**  
A: 
1. 点击 PR 页面的 "Checks" 标签
2. 查看失败的步骤和错误日志
3. 常见原因：
   - 代码有语法错误
   - 测试未通过
   - 文件路径不正确

**Q15: 自动评分结果不对？**  
A: 
1. 检查是否所有必需的文件都已提交
2. 确认星座图文件在 `results/` 目录下
3. 确认 `REPORT.md` 文件存在
4. 查看详细测试日志找出问题

**Q16: 如何提高代码质量评分？**  
A: 
```bash
# 运行 pylint 检查
pylint src/modulation.py

# 根据提示修改代码
# 目标：评分 > 8.0
```

### AI 助手使用相关

**Q17: Copilot 生成的代码不对怎么办？**  
A: 
1. 检查提示词是否足够详细
2. 尝试查看其他建议（按 `Alt+]`）
3. 手动修改生成的代码
4. 参考理论文档，确保理解原理

**Q18: 如何提高 Copilot 的准确率？**  
A: 
- 编写详细的函数文档和注释
- 提供示例输入输出
- 使用清晰的变量命名
- 参考：[Copilot 使用指南](docs/copilot_guide.md)

**Q19: 没有 Copilot 可以完成实验吗？**  
A: 可以！Copilot 只是辅助工具。你可以：
- 参考理论文档中的实现提示
- 使用在线 AI（ChatGPT、Claude等）
- 查阅 NumPy 官方文档
- 向同学、助教请教

### 实验报告相关

**Q20: 实验报告有字数要求吗？**  
A: 建议至少 1000 字，包含：
- 实验目的、原理、方法、结果、分析、心得
- 至少 3 张星座图
- 参考文献

**Q21: 报告可以课后完成吗？**  
A: 可以！但**实验结果（代码+星座图）必须在实验课上提交**。报告可以在截止日期前完善。

**Q22: 报告用什么格式？**  
A: Markdown 格式（`.md` 文件）。参考 [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)。

### 其他问题

**Q23: 选做任务必须做吗？**  
A: 不是必须的。基础任务（0-3+报告）满分 75 分，选做任务是加分项（最多+20分）。

**Q24: 实验时间不够怎么办？**  
A: 
- 优先完成必做任务
- 选做任务可以课后完成
- 提交截止时间是实验课后 7 天

**Q25: 可以参考同学的代码吗？**  
A: 
- ❌ 不可以直接复制粘贴
- ✅ 可以讨论思路和方法
- ✅ 使用 AI 助手辅助是允许的
- ⚠️ 所有提交的代码你必须能够解释

**Q26: 如果被检测到代码雷同怎么办？**  
A: 
- 第一次：警告并要求重新完成
- 严重者：按学术不诚信处理
- 建议：独立完成，理解每一行代码

---

## 📖 参考资料

### 理论文档

- [BPSK原理详解](docs/theory_bpsk.md) - 二进制相移键控完整说明
- [QPSK原理详解](docs/theory_qpsk.md) - 正交相移键控与格雷码
- [QAM原理详解](docs/theory_qam.md) - 正交幅度调制详解

### 工具指南

- [GitHub Copilot 使用指南](docs/copilot_guide.md) - 如何有效使用AI助手（必读⭐）
- [Git 快速入门](docs/git_quickstart.md) - Git命令速查表

### 示例文件

- [examples/bpsk_constellation.png](examples/bpsk_constellation.png) - BPSK星座图参考
- [examples/qpsk_constellation.png](examples/qpsk_constellation.png) - QPSK星座图参考
- [examples/16qam_constellation.png](examples/16qam_constellation.png) - 16-QAM星座图参考
- [examples/ber_curve_example.png](examples/ber_curve_example.png) - BER性能曲线参考

### 外部资源

- **Python文档**：
  - [NumPy官方文档](https://numpy.org/doc/stable/)
  - [Matplotlib官方文档](https://matplotlib.org/stable/contents.html)
  - [SciPy官方文档](https://docs.scipy.org/doc/scipy/)

- **数字通信教材**：
  - John G. Proakis, *Digital Communications* (5th ed.)
  - [维基百科 - 相移键控](https://zh.wikipedia.org/wiki/%E7%9B%B8%E7%A7%BB%E9%94%AE%E6%8E%A7)
  - [维基百科 - 正交幅度调制](https://zh.wikipedia.org/wiki/%E6%AD%A3%E4%BA%A4%E5%B9%85%E5%BA%A6%E8%B0%83%E5%88%B6)

- **GitHub资源**：
  - [GitHub Student Pack](https://education.github.com/) - 免费申请Copilot
  - [GitHub Actions文档](https://docs.github.com/actions)

### 视频教程（可选）

- B站搜索："数字调制原理"、"QPSK调制"、"QAM调制"
- YouTube: "Digital Modulation Tutorial"

---

## 📧 联系方式

如有问题，请通过以下方式联系：
- 课程群：[课程群号]
- 邮箱：[教师邮箱]
- Office Hours：[时间地点]

---

**祝实验顺利！🎉**
#   KmՋG i t H u b   A c t i o n s ꁨRċR�|�~
 
 