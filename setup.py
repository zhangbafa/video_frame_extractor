"""
Video Frame Extractor 安装配置
"""

import re
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("video_frame_extractor/__init__.py", "r", encoding="utf-8") as f:
    version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]+)[\'"]', f.read(), re.M)
    version = version_match.group(1) if version_match else "1.0.0"

setup(
    name="video-frame-extractor",
    version=version,
    description="一个高效的命令行视频抽帧工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Video Frame Extractor Team",
    author_email="",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "Pillow>=8.0.0",
        "tqdm>=4.50.0",
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "video-extract=video_frame_extractor.cli:main",
        ],
    },
    keywords="video, frame, extract, opencv, cli",
    project_urls={
        "Bug Reports": "",
        "Source": "",
    },
)