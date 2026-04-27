"""
总评分计算脚本
整合所有测试结果并生成最终评分
"""

import subprocess
import sys
import os
import json


def run_pytest(test_file, test_name):
    """运行pytest测试并返回结果"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', test_file, '-v', '--tb=short', '--json-report', '--json-report-file=temp_report.json'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # 尝试解析JSON报告
        if os.path.exists('temp_report.json'):
            with open('temp_report.json', 'r') as f:
                report = json.load(f)
            os.remove('temp_report.json')
            
            total = report.get('summary', {}).get('total', 0)
            passed = report.get('summary', {}).get('passed', 0)
            
            return passed, total, result.returncode == 0
        else:
            # 回退方案：解析输出文本
            if 'passed' in result.stdout:
                # 尝试从输出中提取通过的测试数
                import re
                match = re.search(r'(\d+) passed', result.stdout)
                if match:
                    passed = int(match.group(1))
                    return passed, passed, True
            
            return 0, 1, False
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️ {test_name}超时")
        return 0, 1, False
    except Exception as e:
        print(f"  ❌ {test_name}运行失败: {e}")
        return 0, 1, False


def calculate_grade():
    """计算总评分"""
    print("=" * 60)
    print("数字调制解调实验 - 自动评分系统")
    print("=" * 60)
    print()
    
    total_score = 0
    max_score = 100
    
    # 环境测试 (5分)
    print("1️⃣  环境配置测试 (5分)")
    try:
        result = subprocess.run(
            [sys.executable, 'src/test_environment.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            env_score = 5
            print("  ✅ 环境测试通过: +5分")
        else:
            env_score = 0
            print("  ❌ 环境测试失败: 0分")
    except:
        env_score = 0
        print("  ❌ 环境测试失败: 0分")
    
    total_score += env_score
    print()
    
    # BPSK测试 (25分)
    print("2️⃣  BPSK调制测试 (25分)")
    passed, total, success = run_pytest('grading/test_bpsk.py', 'BPSK')
    if total > 0:
        bpsk_score = int(25 * passed / total)
        print(f"  通过测试: {passed}/{total}")
        print(f"  得分: {bpsk_score}/25")
    else:
        bpsk_score = 0
        print("  ❌ 测试未运行: 0分")
    
    total_score += bpsk_score
    print()
    
    # QPSK测试 (25分)
    print("3️⃣  QPSK调制测试 (25分)")
    passed, total, success = run_pytest('grading/test_qpsk.py', 'QPSK')
    if total > 0:
        qpsk_score = int(25 * passed / total)
        print(f"  通过测试: {passed}/{total}")
        print(f"  得分: {qpsk_score}/25")
    else:
        qpsk_score = 0
        print("  ❌ 测试未运行: 0分")
    
    total_score += qpsk_score
    print()
    
    # 16-QAM测试 (20分)
    print("4️⃣  16-QAM调制测试 (20分)")
    passed, total, success = run_pytest('grading/test_qam16.py', '16-QAM')
    if total > 0:
        qam_score = int(20 * passed / total)
        print(f"  通过测试: {passed}/{total}")
        print(f"  得分: {qam_score}/20")
    else:
        qam_score = 0
        print("  ❌ 测试未运行: 0分")
    
    total_score += qam_score
    print()
    
    # 实验报告 (15分)
    print("5️⃣  实验报告检查 (15分)")
    try:
        result = subprocess.run(
            [sys.executable, 'grading/check_report.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        # 从输出中提取分数
        import re
        match = re.search(r'最终报告得分:\s*(\d+)', result.stdout)
        if match:
            report_score = int(match.group(1))
        else:
            report_score = 0
        print(f"  报告得分: {report_score}/15")
    except:
        report_score = 0
        print("  ❌ 报告检查失败: 0分")
    
    total_score += report_score
    print()
    
    # 代码质量检查 (pylint) (-10~+5分)
    print("6️⃣  代码质量检查 (pylint)")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pylint', 'src/modulation.py', '--score=y'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 提取pylint分数
        import re
        match = re.search(r'Your code has been rated at ([\d.]+)/10', result.stdout)
        if match:
            pylint_score_raw = float(match.group(1))
            
            if pylint_score_raw >= 8.0:
                pylint_bonus = 5
                print(f"  ✅ 代码质量优秀 ({pylint_score_raw}/10): +5分")
            elif pylint_score_raw >= 5.0:
                pylint_bonus = 0
                print(f"  ⚠️ 代码质量一般 ({pylint_score_raw}/10): 0分")
            else:
                pylint_bonus = -10
                print(f"  ❌ 代码质量较差 ({pylint_score_raw}/10): -10分")
        else:
            pylint_bonus = 0
            print("  ℹ️ 无法获取pylint分数: 0分")
    except:
        pylint_bonus = 0
        print("  ℹ️ pylint检查跳过: 0分")
    
    total_score += pylint_bonus
    print()
    
    # 选做加分项
    print("7️⃣  选做任务加分")
    bonus_score = 0
    
    # 检查解调函数
    if os.path.exists('src/demodulation.py'):
        with open('src/demodulation.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'raise NotImplementedError' not in content:
                bonus_score += 10
                print("  ✅ 解调功能已实现: +10分")
    
    # 检查性能测试
    if os.path.exists('results/ber_comparison.png') or os.path.exists('results/ber_curve.png'):
        bonus_score += 10
        print("  ✅ BER性能分析完成: +10分")
    
    if bonus_score == 0:
        print("  ℹ️ 未完成选做任务: 0分")
    
    total_score += bonus_score
    print()
    
    # 最终评分
    print("=" * 60)
    print(f"总分: {total_score}/{max_score}")
    
    if total_score >= 90:
        grade = "A (优秀)"
    elif total_score >= 80:
        grade = "B (良好)"
    elif total_score >= 70:
        grade = "C (中等)"
    elif total_score >= 60:
        grade = "D (及格)"
    else:
        grade = "F (不及格)"
    
    print(f"等级: {grade}")
    print("=" * 60)
    
    # 生成详细报告
    report = {
        'total_score': total_score,
        'max_score': max_score,
        'grade': grade,
        'breakdown': {
            'environment': env_score,
            'bpsk': bpsk_score,
            'qpsk': qpsk_score,
            'qam16': qam_score,
            'report': report_score,
            'code_quality': pylint_bonus,
            'bonus': bonus_score
        }
    }
    
    # 保存到文件
    with open('grade_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("\n详细评分报告已保存到: grade_report.json")
    
    return total_score


if __name__ == "__main__":
    calculate_grade()