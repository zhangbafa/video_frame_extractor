# AGENTS.md - Video Frame Extractor

This document provides guidance for AI coding agents working in this repository.

## Project Overview

Video Frame Extractor is a Python CLI tool for extracting frames from videos. It supports multiple extraction modes (time interval, fixed count, keyframe detection), batch processing, and various output formats.

## Build/Install Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Build distribution packages
python -m build
```

## Test Commands

```bash
# Run the interactive test script (requires user input)
python test_extractor.py

# Run a specific test manually with a video file
python -c "from video_frame_extractor.extractor import VideoFrameExtractor; e = VideoFrameExtractor(verbose=True); e.extract_frames('path/to/video.mp4', 'output/', mode='time', interval=1)"
```

Note: This project uses an interactive test script rather than a formal testing framework (pytest/unittest). The `test_extractor.py` file provides manual testing functionality.

## Linting/Type Checking

No linting or type checking configuration exists in this project. If adding validation:

```bash
# Suggested linting (if ruff is installed)
ruff check .

# Suggested type checking (if mypy is installed)
mypy .
```

## Code Style Guidelines

### Imports

Order imports as follows:
1. Standard library imports (os, sys, logging, etc.)
2. Third-party imports (cv2, numpy, PIL, tqdm, etc.)
3. Local imports (from .extractor import ...)

Example:
```python
import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

from .extractor import VideoFrameExtractor
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `VideoFrameExtractor`)
- **Functions/Methods**: snake_case (e.g., `extract_frames`, `_detect_keyframes`)
- **Private Methods**: Prefix with underscore (e.g., `_calculate_histogram`)
- **Constants**: UPPER_SNAKE_CASE at module level (e.g., `SUPPORTED_VIDEO_FORMATS`)
- **Variables**: snake_case (e.g., `video_path`, `output_dir`)

### Documentation

- Use docstrings for all public modules, classes, and functions
- Chinese comments are used throughout this codebase - maintain consistency
- Include Args, Returns sections in docstrings

Example:
```python
def extract_frames(self, video_path, output_dir, mode='time'):
    """
    从视频中提取帧
    
    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        mode: 抽帧模式 ('time', 'count', 'keyframe')
        
    Returns:
        提取的帧数
    """
```

### Error Handling

- Use the logging module for errors, warnings, and info messages
- Return appropriate values (e.g., 0 for extraction count on error) rather than raising exceptions for expected failures
- Log errors before returning:

```python
if not os.path.exists(video_path):
    logger.error(f"视频文件不存在: {video_path}")
    return 0
```

- Use try/except for operations that may fail (file I/O, video processing)
- Catch specific exceptions when possible, use Exception as fallback

### Logging

- Module-level logger: `logger = logging.getLogger(__name__)`
- Log levels: DEBUG (verbose), INFO (normal), WARNING (issues), ERROR (failures)
- Use f-strings for log messages: `logger.info(f"处理完成: {count} 帧")`

### Code Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: ~100 characters
- Use f-strings for string formatting (not .format() or %)
- Add blank lines between logical sections
- Group related statements together

### Type Hints

The existing codebase does not use type hints. When adding new code:
- Match the existing style (no type hints) for consistency
- Document types in docstrings instead

### CLI Module (cli.py)

- Use argparse for command-line argument parsing
- Use colorama for colored terminal output
- Follow the existing pattern of helper functions: `print_success()`, `print_error()`, `print_warning()`, `print_info()`

### Core Module (extractor.py)

- The `VideoFrameExtractor` class is the main extraction engine
- Support three modes: 'time', 'count', 'keyframe'
- Always release OpenCV VideoCapture objects (`cap.release()`)
- Use `os.makedirs(output_dir, exist_ok=True)` for directory creation

## Project Structure

```
video_frame_extractor/
├── .github/
│   └── workflows/
│       └── release.yml       # GitHub Actions release workflow
├── video_frame_extractor/    # Main package
│   ├── __init__.py           # Package init, version info
│   ├── cli.py                # Command-line interface
│   ├── extractor.py          # Core extraction logic
│   └── main.py               # Entry point
├── test_extractor.py         # Interactive test script
├── setup.py                  # Package setup
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
└── AGENTS.md                 # AI agent guidelines
```

## Key Dependencies

- **opencv-python (cv2)**: Video reading and frame extraction
- **Pillow (PIL)**: Image saving
- **tqdm**: Progress bars
- **colorama**: Terminal colors
- **numpy**: Array operations

## Video Format Support

Supported formats defined in cli.py:
- .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm

## Common Tasks

### Adding a new extraction mode

1. Add mode choice to argparse in `cli.py`
2. Add mode handling logic in `extractor.py:extract_frames()`
3. Update documentation in README.md

### Adding new CLI options

1. Add argument to `parse_arguments()` in `cli.py`
2. Pass the option to `VideoFrameExtractor` methods
3. Update interactive_mode() if applicable

### Modifying output format

The output format is handled in `extractor.py:extract_frames()`:
- JPG uses quality parameter (1-100)
- PNG is saved without compression options
