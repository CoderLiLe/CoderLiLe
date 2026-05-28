#!/usr/bin/env python3
"""
GitHub Profile README 优化脚本
优化 CoderLiLe/CoderLiLe 仓库的 README.md 文件
"""

import re
import sys
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Tuple, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

README_PATH = Path("README.md")
CST = timezone(timedelta(hours=8))

# 配置常量
TOC_TITLE = "📑 目录"
TECH_STACK_TITLE = "🛠️ Tech Stack"
MIN_HEADINGS_FOR_TOC = 2


def read_readme(path: Path = README_PATH) -> str:
    """读取 README 文件"""
    if not path.exists():
        logger.error(f"文件不存在: {path}")
        raise FileNotFoundError(f"{path} 不存在")
    
    try:
        content = path.read_text(encoding="utf-8")
        logger.info(f"成功读取 README 文件，大小: {len(content)} 字符")
        return content
    except Exception as e:
        logger.error(f"读取文件失败: {e}")
        raise


def write_readme(content: str, path: Path = README_PATH) -> None:
    """写入 README 文件"""
    try:
        path.write_text(content, encoding="utf-8")
        logger.info(f"成功写入 README 文件，大小: {len(content)} 字符")
    except Exception as e:
        logger.error(f"写入文件失败: {e}")
        raise


def _generate_anchor(title: str) -> str:
    """
    生成 GitHub 兼容的锚点
    规则: 转小写，保留中英文、数字和连字符，空格转换为连字符
    """
    anchor = title.lower().strip()
    # 移除不支持的特殊字符，保留中文、英文、数字、空格和连字符
    anchor = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", anchor)
    # 将连续的空格转换为单个连字符
    anchor = re.sub(r"[\s]+", "-", anchor)
    # 移除首尾的连字符
    anchor = anchor.strip("-")
    return anchor


def _has_table_of_contents(content: str) -> bool:
    """检查是否已存在目录"""
    return bool(re.search(rf"^## {re.escape(TOC_TITLE)}", content, re.MULTILINE))


def _remove_existing_toc(content: str) -> str:
    """移除已存在的目录"""
    # 移除所有现有的目录部分（从 ## 📑 目录 到下一个 ## 或文件末尾）
    content = re.sub(
        rf"^## {re.escape(TOC_TITLE)}\n(?:.*?\n)*?(?=^## |\Z)",
        "",
        content,
        flags=re.MULTILINE
    )
    return content


def add_table_of_contents(content: str) -> str:
    """
    添加目录（仅添加一次）
    提取所有二级标题（##）并生成目录
    """
    # 提取所有二级标题
    headings = re.findall(r"^##\s+(.+?)$", content, re.MULTILINE)
    # 过滤掉目录本身和 Tech Stack
    headings = [h for h in headings if TOC_TITLE not in h and TECH_STACK_TITLE not in h]
    
    if len(headings) < MIN_HEADINGS_FOR_TOC:
        logger.info(f"标题数量 ({len(headings)}) 少于最小值 ({MIN_HEADINGS_FOR_TOC})，跳过目录生成")
        return content
    
    # 移除已存在的目录
    content = _remove_existing_toc(content)
    
    # 生成新目录
    toc_lines = [f"## {TOC_TITLE}\n"]
    for title in headings:
        anchor = _generate_anchor(title)
        toc_lines.append(f"- [{title}](#{anchor})")
    toc = "\n".join(toc_lines) + "\n"
    
    # 在第一个二级标题之前插入目录
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("## ") and TOC_TITLE not in line:
            lines.insert(i, toc)
            logger.info(f"目录已添加，共 {len(headings)} 个标题")
            return "\n".join(lines)
    
    return content


def optimize_images(content: str) -> str:
    """
    优化图片标签：
    1. 移除多余的 {loading="lazy"} 标记
    2. 将 Markdown 图片转换为 HTML <img> 标签并添加懒加载
    3. 为现有的 HTML <img> 标签完善懒加载属性
    """
    # 移除多余的 {loading="lazy"} 标记
    content = re.sub(r'\s*\{:\s*loading="lazy"\s*\}\s*', "", content)
    
    # 将 Markdown 图片转换为 HTML <img> 标签
    content = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        r'<img src="\2" alt="\1" loading="lazy" />',
        content,
    )
    
    # 为现有的 HTML <img> 标签添加懒加载（如果还没有）
    def add_lazy_loading(match):
        img_tag = match.group(0)
        if 'loading=' not in img_tag:
            # 在 /> 或 > 之前插入 loading="lazy"
            if img_tag.endswith('/>'):
                img_tag = img_tag[:-2] + ' loading="lazy" />'
            elif img_tag.endswith('>'):
                img_tag = img_tag[:-1] + ' loading="lazy" >'
        return img_tag
    
    content = re.sub(r'<img\s+[^>]*/?>', add_lazy_loading, content)
    
    logger.info("图片优化完成")
    return content


def update_last_updated(content: str) -> str:
    """更新最后修改时间戳"""
    now = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    
    # 移除所有旧的时间戳行（在文件末尾）
    content = re.sub(
        r'\n\n最后更新于.*?(?=\n|$)',
        "",
        content,
    )
    
    # 查找并更新文件末尾的 "Last Updated" 行
    if re.search(r"Last Updated:.*?\*\*", content):
        content = re.sub(
            r"Last Updated:.*?\*\*",
            f"Last Updated: **{now}** | Optimized by AI Assistant**",
            content,
        )
        logger.info(f"时间戳已更新: {now}")
    else:
        # 添加新的时间戳到文件末尾（在最后的分隔线之前）
        content = content.rstrip("\n")
        if not content.endswith("---"):
            content += "\n\n---\n"
        content += f"\nLast Updated: **{now}** | Optimized by AI Assistant\n"
        logger.info(f"添加新时间戳: {now}")
    
    return content


def group_skill_badges(content: str) -> str:
    """
    按类别分组技能徽章（适配现有 README 格式）
    将技能部分重新整理为有组织的类别，每个徽章单独一行
    """
    # 查找技术栈部分（## 开头）
    match = re.search(
        rf"^## {re.escape(TECH_STACK_TITLE)}\n.*?(?=^## |\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    
    if not match:
        logger.warning("未找到技术栈部分，跳过徽章分组")
        return content
    
    # 定义技能徽章分类
    badges = {
        "💻 Programming Languages": [
            ("Java", "java", "ED8936"),
            ("Python", "python", "3776AB"),
            ("JavaScript", "javascript", "F7DF1E"),
            ("TypeScript", "typescript", "3178C6"),
            ("C", "c", "A8B9CC"),
            ("C%2B%2B", "cplusplus", "00599C"),
            ("SQL", "postgresql", "336791"),
            ("Swift", "swift", "FA7343"),
            ("Go", "go", "00ADD8"),
        ],
        "🎨 Frontend Technologies": [
            ("HTML5", "html5", "E34C26"),
            ("CSS3", "css3", "1572B6"),
            ("Vue.js", "vuedotjs", "4FC08D"),
            ("React", "react", "61DAFB"),
        ],
        "⚙️ Backend & Frameworks": [
            ("Spring", "spring", "6DB33F"),
            ("Django", "django", "092E20"),
            ("Node.js", "nodedotjs", "339933"),
            ("Express", "express", "000000"),
        ],
        "🔧 Tools & Platforms": [
            ("Git", "git", "F05032"),
            ("Docker", "docker", "2496ED"),
            ("GitHub", "github", "181717"),
            ("VS%20Code", "visualstudiocode", "007ACC"),
            ("Linux", "linux", "FCC624"),
        ],
    }
    
    # 构建新的技术栈部分，每个徽章换行
    new_section = f"## {TECH_STACK_TITLE}\n\n"
    for category, items in badges.items():
        new_section += f"### {category}\n\n"
        for name, logo, color in items:
            badge = (
                f'<img src="https://img.shields.io/badge/{name}-{color}'
                f'?style=flat-square&logo={logo}&logoColor=white" alt="{name}" loading="lazy" />\n'
            )
            new_section += badge
        new_section += "\n"
    
    old_section = match.group(0)
    updated_content = content.replace(old_section, new_section.rstrip() + "\n")
    logger.info("技能徽章分组完成")
    
    return updated_content


def validate_changes(original: str, modified: str) -> Tuple[bool, str]:
    """
    验证修改后的内容
    返回 (是否有效, 消息)
    """
    # 检查基本结构
    if not modified.strip():
        return False, "修改后的内容为空"
    
    # 检查是否删除了重要部分
    important_sections = ["About Me", "Statistics", "Tech Stack", "Featured Projects"]
    for section in important_sections:
        if section in original and section not in modified:
            return False, f"重要部分被删除: {section}"
    
    # 检查目录唯一性
    toc_count = len(re.findall(rf"^## {re.escape(TOC_TITLE)}", modified, re.MULTILINE))
    if toc_count > 1:
        return False, f"目录重复出现 {toc_count} 次"
    
    return True, "验证通过"


def main() -> None:
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始优化 README.md...")
    logger.info("=" * 50)
    
    try:
        # 读取原始文件
        content = read_readme()
        original_content = content
        original_length = len(content)
        
        # 执行优化操作
        logger.info("\n执行优化步骤...")
        content = add_table_of_contents(content)
        content = optimize_images(content)
        content = group_skill_badges(content)
        content = update_last_updated(content)
        
        # 验证修改
        logger.info("\n验证修改...")
        is_valid, validation_msg = validate_changes(original_content, content)
        if not is_valid:
            logger.error(f"验证失败: {validation_msg}")
            sys.exit(1)
        logger.info(f"✓ {validation_msg}")
        
        # 写入文件
        write_readme(content)
        
        # 输出统计信息
        optimized_length = len(content)
        diff = optimized_length - original_length
        
        logger.info("\n" + "=" * 50)
        logger.info("优化完成！✓")
        logger.info("=" * 50)
        logger.info(f"原始长度:  {original_length:,} 字符")
        logger.info(f"优化后长度: {optimized_length:,} 字符")
        logger.info(f"变化:     {diff:+,} 字符 ({(diff/original_length*100):+.2f}%)")
        logger.info("=" * 50)
        
    except FileNotFoundError as e:
        logger.error(f"文件错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"发生错误: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
