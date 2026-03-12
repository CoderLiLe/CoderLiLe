#!/usr/bin/env python3
"""
GitHub Profile README 优化脚本
优化 CoderLiLe/CoderLiLe 仓库的 README.md 文件
"""

import re
import os
from datetime import datetime

def read_readme():
    """读取 README.md 文件"""
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

def write_readme(content):
    """写入 README.md 文件"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

def add_table_of_contents(content):
    """添加目录导航"""
    toc_lines = []
    
    # 查找所有标题
    headings = re.findall(r'^(#{2,4})\s+(.+)$', content, re.MULTILINE)
    
    if len(headings) > 3:  # 如果有足够多的标题才添加目录
        toc = "## 📑 目录导航\n\n"
        for level, title in headings:
            if level == "##":  # 只处理二级标题
                # 生成锚点链接
                anchor = re.sub(r'[^\w\s-]', '', title.lower())
                anchor = re.sub(r'[-\s]+', '-', anchor).strip('-')
                toc += f"- [{title}](#{anchor})\n"
        
        # 在第一个二级标题后插入目录
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('## ') and not line.startswith('## 📑'):
                lines.insert(i + 1, '\n' + toc + '\n')
                return '\n'.join(lines)
    
    return content

def optimize_images(content):
    """优化图片加载"""
    # 添加图片懒加载属性
    content = re.sub(
        r'!\[(.*?)\]\((.*?)\)',
        r'![\1](\2){:loading="lazy"}',
        content
    )
    
    # 为统计卡片添加尺寸限制
    content = re.sub(
        r'<img height="(\d+)" src="(https://github-readme-stats[^"]+)"',
        r'<img height="\1" width="\1" src="\2" loading="lazy"',
        content
    )
    
    return content

def update_last_updated(content):
    """更新最后更新时间"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 查找并更新最后更新时间
    if "最后更新" in content:
        content = re.sub(
            r'最后更新于\s*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}',
            f'最后更新于 {current_time}',
            content
        )
    else:
        # 在文件末尾添加更新时间
        if not content.endswith('\n'):
            content += '\n'
        content += f'\n---\n\n最后更新于 {current_time} | 由 AI 助手优化\n'
    
    return content

def group_skill_badges(content):
    """按类别分组技能徽章"""
    # 查找技能徽章部分
    skill_section = re.search(
        r'### My Skill Set.*?(?=\n###|\n---|\n```|\n<div|\n<h|\n<style|\n<script|\n</div|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    
    if skill_section:
        skill_text = skill_section.group(0)
        
        # 按语言类型分组
        languages = ['Java', 'Python', 'JavaScript', 'C', 'C++', 'SQL', 'Swift', 'Go']
        frontend = ['HTML', 'CSS', 'React', 'Vue', 'TypeScript']
        backend = ['Spring', 'Django', 'Flask', 'Node.js', 'Express']
        tools = ['Git', 'Docker', 'Linux', 'AWS', 'MySQL', 'PostgreSQL']
        
        # 创建分组徽章
        grouped_badges = "### 🛠️ 技术栈\n\n"
        
        grouped_badges += "#### 编程语言\n"
        for lang in languages:
            if lang.lower() in skill_text.lower():
                grouped_badges += f'![](https://img.shields.io/badge/{lang}-3776AB?style=flat-square&logo={lang.lower()}&logoColor=white) '
        grouped_badges += "\n\n"
        
        grouped_badges += "#### 前端技术\n"
        for tech in frontend:
            if tech.lower() in skill_text.lower():
                grouped_badges += f'![](https://img.shields.io/badge/{tech}-61DAFB?style=flat-square&logo={tech.lower()}&logoColor=white) '
        grouped_badges += "\n\n"
        
        grouped_badges += "#### 后端技术\n"
        for tech in backend:
            if tech.lower() in skill_text.lower():
                grouped_badges += f'![](https://img.shields.io/badge/{tech}-6DB33F?style=flat-square&logo=spring&logoColor=white) '
        grouped_badges += "\n\n"
        
        grouped_badges += "#### 开发工具\n"
        for tool in tools:
            if tool.lower() in skill_text.lower():
                grouped_badges += f'![](https://img.shields.io/badge/{tool}-2496ED?style=flat-square&logo={tool.lower()}&logoColor=white) '
        
        # 替换原技能部分
        content = content.replace(skill_text, grouped_badges)
    
    return content

def main():
    print("开始优化 README.md...")
    
    # 读取原始内容
    content = read_readme()
    original_length = len(content)
    
    # 应用优化
    content = add_table_of_contents(content)
    content = optimize_images(content)
    content = group_skill_badges(content)
    content = update_last_updated(content)
    
    # 写入优化后的内容
    write_readme(content)
    
    optimized_length = len(content)
    print(f"优化完成！")
    print(f"原始长度: {original_length} 字符")
    print(f"优化后长度: {optimized_length} 字符")
    print(f"变化: {optimized_length - original_length} 字符")

if __name__ == "__main__":
    main()