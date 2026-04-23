"""
原始总评分计算脚本（备份）
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
    
    # 评分细则略 ...
    # 见原脚本
    
    # 输出最终得分
    print(f"\n最终得分: {total_score}/{max_score}")
    return total_score

if __name__ == "__main__":
    calculate_grade()
