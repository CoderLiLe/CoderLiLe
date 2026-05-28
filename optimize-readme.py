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

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

README_PATH = Path("README.md")

CST = timezone(timedelta(hours=8))


def read_readme(path: Path = README_PATH) -> str:
    if not path.exists():
        raise FileNotFoundError(f"{path} 不存在")
    return path.read_text(encoding="utf-8")


def write_readme(content: str, path: Path = README_PATH) -> None:
    path.write_text(content, encoding="utf-8")


def _generate_anchor(title: str) -> str:
    """生成 GitHub 兼容的锚点（保留中文）"""
    # GitHub 锚点规则：转小写，非字母数字中文连字符替换为 -
    anchor = title.lower().strip()
    anchor = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", anchor)
    anchor = re.sub(r"[\s]+", "-", anchor)
    return anchor


def add_table_of_contents(content: str) -> str:
    headings = re.findall(r"^(#{2,3})\s+(.+)$", content, re.MULTILINE)
    top_headings = [t for level, t in headings if level == "##"]

    if len(top_headings) < 2:
        return content

    toc_parts = ["## 📑 目录\n"]
    for title in top_headings:
        anchor = _generate_anchor(title)
        toc_parts.append(f"- [{title}](#{anchor})\n")
    toc = "".join(toc_parts)

    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("## ") and "目录" not in line:
            lines.insert(i + 1, "\n" + toc)
            return "\n".join(lines)

    return content


def optimize_images(content: str) -> str:
    # 为 Markdown 图片添加懒加载（kramdown 语法）
    content = re.sub(
        r'!\[(.*?)\]\((.*?)\)',
        r'![\1](\2){:loading="lazy"}',
        content,
    )
    # 为 HTML <img> 标签添加懒加载和响应式
    content = re.sub(
        r'<img\s',
        '<img loading="lazy" ',
        content,
    )
    return content


def update_last_updated(content: str) -> str:
    now = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")

    if "最后更新" in content:
        content = re.sub(
            r"最后更新于\s*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}(:\d{2})?",
            f"最后更新于 {now}",
            content,
        )
    else:
        content = content.rstrip("\n") + f'\n\n---\n\n最后更新于 {now} | 由 AI 助手优化\n'

    return content


def group_skill_badges(content: str) -> str:
    """按类别分组技能徽章（适配现有 README 格式）"""
    match = re.search(
        r"### 🛠️ 技术栈\n.*?(?=\n### |\n---|\Z)",
        content,
        re.DOTALL,
    )
    if not match:
        return content

    old_section = match.group(0)

    badges = {
        "编程语言": [
            ("Java", "java", "3776AB"),
            ("Python", "python", "3776AB"),
            ("JavaScript", "javascript", "3776AB"),
            ("TypeScript", "typescript", "3178C6"),
            ("C", "c", "3776AB"),
            ("C++", "cplusplus", "3776AB"),
            ("MySQL", "mysql", "3776AB"),
            ("Swift", "swift", "3776AB"),
            ("Go", "go", "3776AB"),
        ],
        "前端技术": [
            ("HTML5", "html5", "E34F26"),
            ("CSS3", "css3", "1572B6"),
            ("Vue.js", "vuedotjs", "4FC08D"),
        ],
        "后端技术": [
            ("Spring", "spring", "6DB33F"),
            ("Node.js", "nodedotjs", "339933"),
        ],
        "开发工具": [
            ("Git", "git", "F05032"),
            ("Docker", "docker", "2496ED"),
            ("Linux", "linux", "FCC624"),
            ("VS Code", "visualstudiocode", "007ACC"),
        ],
    }

    new_section = "### 🛠️ 技术栈\n\n"
    for category, items in badges.items():
        new_section += f"#### {category}\n"
        for name, logo, color in items:
            color_logo = logo if logo or color else ""
            new_section += (
                f'![](https://img.shields.io/badge/{name}-{color}'
                f'?style=flat-square&logo={logo}&logoColor=white) '
            )
        new_section += "\n\n"

    return content.replace(old_section, new_section.strip())


def main() -> None:
    logger.info("开始优化 README.md...")

    try:
        content = read_readme()
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)

    original_length = len(content)

    content = add_table_of_contents(content)
    content = optimize_images(content)
    content = group_skill_badges(content)
    content = update_last_updated(content)

    write_readme(content)

    optimized_length = len(content)
    diff = optimized_length - original_length
    logger.info(f"优化完成！")
    logger.info(f"原始长度: {original_length} 字符")
    logger.info(f"优化后长度: {optimized_length} 字符")
    logger.info(f"变化: {diff:+d} 字符")


if __name__ == "__main__":
    main()
