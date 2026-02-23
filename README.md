# Video Frame Extractor

一个高效的命令行视频抽帧工具，支持多种抽帧模式和批量处理。

## 功能特点

- 支持多种抽帧模式：
  - 时间间隔抽帧（每隔指定秒数抽取一帧）
  - 固定帧数抽帧（均匀抽取指定数量的帧）
  - 智能关键帧检测（自动识别场景变化明显的帧）
- 支持多种输出格式（JPG、PNG）和质量设置
- 批量处理多个视频文件
- 简洁直观的命令行界面
- 交互式模式支持

## 安装

### 依赖项

- Python 3.8+
- opencv-python
- pillow
- tqdm

### 安装方法

使用pip安装：

```bash
pip install video-frame-extractor
```

或从源码安装：

```bash
git clone https://github.com/yourusername/video-frame-extractor.git
cd video-frame-extractor
pip install .
```

## 使用方法

### 命令行参数

```
usage: video-extract [-h] [-i INPUT [INPUT ...]] [-o OUTPUT] [-m {time,count,keyframe}]
                     [-f {jpg,png}] [-q QUALITY] [-t INTERVAL] [-n NUMBER]
                     [-s SENSITIVITY] [-r] [-v] [-y]

视频抽帧工具

options:
  -h, --help            show this help message and exit
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        输入视频文件路径或目录
  -o OUTPUT, --output OUTPUT
                        输出目录路径
  -m {time,count,keyframe}, --mode {time,count,keyframe}
                        抽帧模式
  -f {jpg,png}, --format {jpg,png}
                        输出图像格式
  -q QUALITY, --quality QUALITY
                        输出图像质量(1-100，仅jpg有效)
  -t INTERVAL, --interval INTERVAL
                        时间间隔(秒)，用于time模式
  -n NUMBER, --number NUMBER
                        提取帧数，用于count模式
  -s SENSITIVITY, --sensitivity SENSITIVITY
                        关键帧检测灵敏度(1-100)，用于keyframe模式
  -r, --recursive       递归处理目录下所有视频文件
  -v, --verbose         显示详细信息
  -y, --yes             自动确认覆盖已存在文件
```

### 使用示例

#### 基本用法

```bash
# 每5秒提取一帧，保存为jpg格式
video-extract -i video.mp4 -o frames -m time -t 5 -f jpg

# 提取10帧，均匀分布在视频中
video-extract -i video.mp4 -o frames -m count -n 10

# 自动检测关键帧，灵敏度为70
video-extract -i video.mp4 -o frames -m keyframe -s 70
```

#### 批量处理

```bash
# 处理目录下所有视频
video-extract -i videos/ -o frames/ -m time -t 10 -r

# 处理多个指定视频
video-extract -i video1.mp4 video2.mp4 -o frames/ -m count -n 20
```

#### 高级选项

```bash
# PNG格式输出，无损质量
video-extract -i video.mp4 -o frames -m time -t 1 -f png

# JPG格式输出，高质量
video-extract -i video.mp4 -o frames -m count -n 50 -f jpg -q 95

# 详细输出模式
video-extract -i video.mp4 -o frames -m keyframe -s 60 -v
```

## 交互式模式

如果未提供足够的参数，工具会自动进入交互式模式，引导您完成设置：

```bash
video-extract
```

## 许可证

本项目采用MIT许可证 - 详见LICENSE文件