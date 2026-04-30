# 教师使用说明

本文档面向教师，说明如何部署和管理数字调制解调实验平台。

---

## 1. 平台部署

### 1.1 创建GitHub模板仓库

1. 在你的 GitHub 组织或个人账号下创建新仓库：
   - 仓库名：`wireless-modulation-experiment`
   - 可见性：`Public`（便于学生访问）
   - 勾选 `Template repository`（作为模板）

2. 将本地文件推送到远程仓库：

```bash
cd wireless-modulation-experiment
git init
git add .
git commit -m "初始化数字调制解调实验平台"
git branch -M main
git remote add origin https://github.com/jwentong/wireless-modulation-experiment.git
git push -u origin main
```

### 1.2 配置GitHub Actions权限

1. 进入仓库 `Settings` → `Actions` → `General`
2. **Workflow permissions** 设置为：
   - ✅ `Read and write permissions`
   - ✅ `Allow GitHub Actions to create and approve pull requests`

### 1.3 保护评分脚本

将 `grading/` 目录设置为学生不可见（可选）：

**方法1**：使用私有子模块
```bash
# 将grading移到私有仓库
git submodule add https://github.com/jwentong/wireless-modulation-grading.git grading
```

**方法2**：在学生 fork 后删除 grading/
- 学生 fork 后，GitHub Actions 会从教师仓库拉取评分脚本
- 在 workflow 中添加：

```yaml
- name: 拉取评分脚本
  run: |
    git clone https://github.com/jwentong/wireless-modulation-grading.git grading
```

---

## 2. 学生使用流程

### 2.1 发布实验通知

在课程群或公告中发布：

```
📢 数字调制解调实验通知

实验时间：2026年4月24日（本周四）14:00-16:00
实验地点：[地点]

准备工作：
1. 确保已安装 Python 3.8+ 和 VS Code
2. 注册 GitHub 账号并申请 GitHub Student Pack（免费使用Copilot）
3. 预习实验指导：[链接]

实验模板仓库：
https://github.com/jwentong/wireless-modulation-experiment

提交截止时间：2026年5月1日 23:59

如有问题，请在群里提问或发邮件。
```

### 2.2 指导学生Fork仓库

在实验课上演示：

1. 访问模板仓库
2. 点击 `Use this template` 或 `Fork`
3. Clone 到本地
4. 安装依赖并测试环境

### 2.3 学生提交流程

学生完成实验后：

1. Commit 并 Push 到自己的仓库
2. 创建 Pull Request（Base: 教师仓库，Head: 学生仓库）
3. GitHub Actions 自动评分
4. 学生查看评分结果，可选修改后重新提交

---

## 3. 评分管理

### 3.1 自动评分规则

评分系统自动执行以下检查：

| 项目 | 分值 | 检查方式 |
|------|------|----------|
| 环境配置 | 5分 | 运行 `test_environment.py` |
| BPSK调制 | 25分 | pytest测试映射正确性、星座图 |
| QPSK调制 | 25分 | pytest测试格雷码、归一化 |
| 16-QAM调制 | 20分 | pytest测试I/Q映射、功率 |
| 实验报告 | 15分 | 检查章节完整性、字数、图片 |
| 代码质量 | -10~+5分 | pylint评分 |
| 选做加分 | +20分 | 解调函数(+10)、BER分析(+10) |

总分：75分（基础）+ 20分（选做）+ 5分（代码质量）= 100分

### 3.2 查看所有学生评分

**方法1**：导出 Pull Requests

使用 GitHub API 或第三方工具导出所有 PR 的评分结果。

**方法2**：使用脚本批量检查

创建脚本遍历所有学生的 fork：

```python
import requests

students = [
    "student1",
    "student2",
    # ...
]

for student in students:
    url = f"https://api.github.com/repos/{student}/wireless-modulation-experiment/actions/runs"
    # 获取最新评分结果
    # ...
```

### 3.3 手动复核

自动评分后，教师应复核：

1. **代码逻辑**：是否真正理解原理，还是盲目使用AI
2. **实验报告**：分析是否深入，心得是否真实
3. **星座图质量**：是否清晰、标注是否规范

调整最终分数（±5分）。

---

## 4. 常见问题处理

### 问题1：学生 GitHub Actions 失败

**原因**：
- 依赖安装失败
- 代码有语法错误
- 测试超时

**解决**：
1. 查看 Actions 日志，找到具体错误
2. 指导学生修改代码
3. 重新 Push 触发评分

### 问题2：学生报告评分过低

**原因**：
- 缺少必要章节
- 字数不足
- 没有插入图片

**解决**：
- 提供 `REPORT_TEMPLATE.md` 模板
- 说明评分标准
- 允许修改后重新提交

### 问题3：学生代码雷同

**检测方法**：
1. 使用代码相似度检测工具（如 MOSS）
2. 检查 Git 提交历史（是否一次性提交大量代码）
3. 现场抽查，要求学生解释代码

**处理**：
- 警告并要求重新完成
- 严重者按学术不诚信处理

### 问题4：AI生成代码质量差

**指导**：
- 强调理解原理比完成代码更重要
- 要求学生在报告中说明使用AI的方式
- 课堂上演示正确的 Copilot 使用方法

---

## 5. 评分调整

在 `grading/calculate_grade.py` 中可以调整各项分值：

```python
# 修改分值权重
env_score = 5      # 环境测试
bpsk_score = 25    # BPSK
qpsk_score = 25    # QPSK
qam_score = 20     # 16-QAM
report_score = 15  # 报告
```

也可以添加新的评分项：

```python
# 添加代码注释检查
comment_score = 5
if check_comments(code):
    comment_score = 5
else:
    comment_score = 0
```

---

## 6. 实验改进建议

### 6.1 难度调整

**降低难度**：
- 提供更多代码框架
- 减少必做任务数量
- 延长实验时间

**提高难度**：
- 要求实现更高阶调制（64-QAM、256-QAM）
- 要求实现信道编码（卷积码、Turbo码）
- 要求实现实时信号处理

### 6.2 扩展实验

可以基于此平台扩展更多实验：

- **实验2**：信道编码与译码
- **实验3**：OFDM调制
- **实验4**：MIMO系统仿真
- **实验5**：软件无线电实现（使用 USRP）

### 6.3 加入实时竞赛

设置排行榜，比较学生的 BER 性能或代码效率。

```python
# 在 GitHub Actions 中记录性能指标
with open('leaderboard.json', 'r+') as f:
    data = json.load(f)
    data[student_name] = {
        'ber': ber_value,
        'runtime': runtime_ms,
        'score': total_score
    }
    # 排序并更新
```

---

## 7. 技术支持

### 7.1 常用命令

```bash
# 更新模板仓库
git add .
git commit -m "更新实验要求"
git push origin main

# 查看所有fork
gh api repos/你的用户名/wireless-modulation-experiment/forks

# 批量运行测试
for repo in student_repos:
    git clone $repo
    cd repo
    pytest grading/
    cd ..
```

### 7.2 监控GitHub Actions配额

免费账号有限制：
- Public 仓库：无限
- Private 仓库：每月 2000 分钟

查看用量：`Settings` → `Billing` → `Actions`

---

## 8. 联系与反馈

如果在使用过程中遇到问题，或有改进建议，请：

- 📧 发送邮件至：[你的邮箱]
- 💬 在仓库中提 Issue
- 📝 提交 Pull Request 改进文档

---

## 9. 许可与致谢

本实验平台基于以下技术：
- Python + NumPy + Matplotlib
- GitHub + GitHub Actions
- pytest + pylint

感谢开源社区的贡献！

---

**祝教学顺利！** 🎓
