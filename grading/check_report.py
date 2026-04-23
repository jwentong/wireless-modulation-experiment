"""
实验报告检查脚本
"""

import os
import re


def check_report_exists():
    """检查报告文件是否存在"""
    report_files = ['REPORT.md', 'report.md', 'Report.md']
    
    for filename in report_files:
        if os.path.exists(filename):
            return filename
    return None


def check_report_content(filepath):
    """检查报告内容完整性"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 必需的章节
    required_sections = [
        '实验目的',
        '实验原理',
        '实验方法',
        '实验结果',
        '结果分析',
        '实验心得'
    ]
    
    score = 0
    feedback = []
    
    # 检查字数（至少1000字）
    char_count = len(content)
    if char_count >= 1000:
        score += 3
        feedback.append(f"✅ 字数达标 ({char_count}字)")
    else:
        feedback.append(f"⚠️ 字数不足 ({char_count}字，建议至少1000字)")
    
    # 检查章节完整性
    sections_found = 0
    for section in required_sections:
        if section in content or section.lower() in content.lower():
            sections_found += 1
    
    section_score = sections_found * 2
    score += section_score
    feedback.append(f"📋 章节完整性: {sections_found}/{len(required_sections)} ({section_score}分)")
    
    # 检查是否包含图片引用
    image_refs = re.findall(r'!\[.*?\]\(.*?\)', content)
    if len(image_refs) >= 3:
        score += 2
        feedback.append(f"✅ 包含图片引用 ({len(image_refs)}张)")
    else:
        feedback.append(f"⚠️ 图片引用不足 ({len(image_refs)}张，建议至少3张)")
    
    # 检查是否包含代码块
    code_blocks = re.findall(r'```[\s\S]*?```', content)
    if len(code_blocks) >= 1:
        score += 1
        feedback.append(f"✅ 包含代码示例 ({len(code_blocks)}处)")
    
    # 检查参考文献
    if '参考文献' in content or '参考资料' in content:
        score += 1
        feedback.append("✅ 包含参考文献")
    
    # 最大15分
    score = min(score, 15)
    
    return score, feedback


def generate_report_score():
    """生成报告评分"""
    print("=" * 50)
    print("实验报告检查")
    print("=" * 50)
    
    # 检查文件是否存在
    report_file = check_report_exists()
    
    if report_file is None:
        print("❌ 未找到实验报告文件 (REPORT.md)")
        print("扣分: -15分")
        return 0
    
    print(f"✅ 找到报告文件: {report_file}")
    
    # 检查内容
    try:
        score, feedback = check_report_content(report_file)
        
        print("\n评分详情:")
        for item in feedback:
            print(f"  {item}")
        
        print(f"\n报告得分: {score}/15")
        
        return score
        
    except Exception as e:
        print(f"❌ 报告检查失败: {e}")
        return 0


if __name__ == "__main__":
    score = generate_report_score()
    print(f"\n最终报告得分: {score}")