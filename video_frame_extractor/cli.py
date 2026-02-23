"""
命令行界面模块
"""

import os
import sys
import argparse
import glob
import logging
from colorama import init, Fore, Style, Back

from .extractor import VideoFrameExtractor

# 初始化colorama
init(autoreset=True)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# 支持的视频格式
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    """打印彩色文本"""
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def print_success(text):
    """打印成功信息"""
    print_colored(f"✓ {text}", Fore.GREEN)

def print_warning(text):
    """打印警告信息"""
    print_colored(f"⚠ {text}", Fore.YELLOW)

def print_error(text):
    """打印错误信息"""
    print_colored(f"✗ {text}", Fore.RED)

def print_info(text):
    """打印信息"""
    print_colored(f"ℹ {text}", Fore.BLUE)

def print_header():
    """打印程序头部信息"""
    header = """
    ╔══════════════════════════════════════════════╗
    ║            Video Frame Extractor             ║
    ║              视频抽帧工具                    ║
    ╚══════════════════════════════════════════════╝
    """
    print_colored(header, Fore.CYAN, Style.BRIGHT)

def is_video_file(file_path):
    """检查文件是否为支持的视频格式"""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in SUPPORTED_VIDEO_FORMATS

def find_video_files(directory, recursive=False):
    """查找目录中的视频文件"""
    video_files = []
    
    if recursive:
        pattern = os.path.join(directory, '**', '*')
    else:
        pattern = os.path.join(directory, '*')
    
    for file_path in glob.glob(pattern, recursive=recursive):
        if os.path.isfile(file_path) and is_video_file(file_path):
            video_files.append(file_path)
    
    return video_files

def get_input_videos(input_paths, recursive=False):
    """获取输入的视频文件列表"""
    video_files = []
    
    for path in input_paths:
        if os.path.isfile(path):
            if is_video_file(path):
                video_files.append(path)
            else:
                print_warning(f"跳过非视频文件: {path}")
        elif os.path.isdir(path):
            dir_videos = find_video_files(path, recursive)
            if dir_videos:
                video_files.extend(dir_videos)
                print_info(f"从目录 '{path}' 中找到 {len(dir_videos)} 个视频文件")
            else:
                print_warning(f"目录 '{path}' 中没有找到视频文件")
        else:
            print_error(f"路径不存在: {path}")
    
    return video_files

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog='video-extract',
        description='视频抽帧工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 每5秒提取一帧，保存为jpg格式
  video-extract -i video.mp4 -o frames -m time -t 5 -f jpg
  
  # 提取10帧，均匀分布在视频中
  video-extract -i video.mp4 -o frames -m count -n 10
  
  # 自动检测关键帧，灵敏度为70
  video-extract -i video.mp4 -o frames -m keyframe -s 70
  
  # 处理目录下所有视频
  video-extract -i videos/ -o frames/ -m time -t 10 -r
        """
    )
    
    # 基本参数
    parser.add_argument('-i', '--input', nargs='+', help='输入视频文件路径或目录')
    parser.add_argument('-o', '--output', help='输出目录路径')
    parser.add_argument('-m', '--mode', choices=['time', 'count', 'keyframe'], default='time',
                      help='抽帧模式')
    parser.add_argument('-f', '--format', choices=['jpg', 'png'], default='jpg',
                      help='输出图像格式')
    parser.add_argument('-q', '--quality', type=int, default=90,
                      help='输出图像质量(1-100，仅jpg有效)')
    
    # 模式特定参数
    parser.add_argument('-t', '--interval', type=float, default=1.0,
                      help='时间间隔(秒)，用于time模式')
    parser.add_argument('-n', '--number', type=int, default=10,
                      help='提取帧数，用于count模式')
    parser.add_argument('-s', '--sensitivity', type=int, default=50,
                      help='关键帧检测灵敏度(1-100)，用于keyframe模式')
    
    # 其他参数
    parser.add_argument('-r', '--recursive', action='store_true',
                      help='递归处理目录下所有视频文件')
    parser.add_argument('-v', '--verbose', action='store_true',
                      help='显示详细信息')
    parser.add_argument('-y', '--yes', action='store_true',
                      help='自动确认覆盖已存在文件')
    
    return parser.parse_args()

def interactive_mode():
    """交互式模式"""
    print_header()
    print_info("进入交互式模式，请按照提示输入信息")
    print()
    
    # 获取输入路径
    input_paths = []
    while True:
        path = input("请输入视频文件路径或目录 (多个路径用空格分隔，直接回车结束): ").strip()
        if not path:
            break
        input_paths.extend(path.split())
    
    if not input_paths:
        print_error("未提供输入路径，程序退出")
        return False
    
    # 获取输出目录
    output_dir = input("请输入输出目录路径 [默认为 'frames']: ").strip()
    if not output_dir:
        output_dir = 'frames'
    
    # 获取抽帧模式
    mode = input("请选择抽帧模式 [time/count/keyframe，默认为time]: ").strip().lower()
    if not mode or mode not in ['time', 'count', 'keyframe']:
        mode = 'time'
    
    # 获取输出格式
    output_format = input("请选择输出图像格式 [jpg/png，默认为jpg]: ").strip().lower()
    if not output_format or output_format not in ['jpg', 'png']:
        output_format = 'jpg'
    
    # 获取图像质量
    quality = 90
    if output_format == 'jpg':
        quality_input = input("请输入图像质量 (1-100，默认为90): ").strip()
        if quality_input:
            try:
                quality = int(quality_input)
                quality = max(1, min(100, quality))
            except ValueError:
                print_warning("无效的质量值，使用默认值90")
    
    # 获取模式特定参数
    interval = 1.0
    number = 10
    sensitivity = 50
    
    if mode == 'time':
        interval_input = input("请输入时间间隔(秒) [默认为1.0]: ").strip()
        if interval_input:
            try:
                interval = float(interval_input)
                if interval <= 0:
                    print_warning("时间间隔必须大于0，使用默认值1.0")
                    interval = 1.0
            except ValueError:
                print_warning("无效的时间间隔，使用默认值1.0")
    
    elif mode == 'count':
        number_input = input("请输入要提取的帧数 [默认为10]: ").strip()
        if number_input:
            try:
                number = int(number_input)
                if number <= 0:
                    print_warning("帧数必须大于0，使用默认值10")
                    number = 10
            except ValueError:
                print_warning("无效的帧数，使用默认值10")
    
    elif mode == 'keyframe':
        sensitivity_input = input("请输入关键帧检测灵敏度(1-100) [默认为50]: ").strip()
        if sensitivity_input:
            try:
                sensitivity = int(sensitivity_input)
                sensitivity = max(1, min(100, sensitivity))
            except ValueError:
                print_warning("无效的灵敏度值，使用默认值50")
    
    # 获取递归选项
    recursive_input = input("是否递归处理目录下所有视频文件? [y/N]: ").strip().lower()
    recursive = recursive_input == 'y'
    
    # 获取详细信息选项
    verbose_input = input("是否显示详细信息? [y/N]: ").strip().lower()
    verbose = verbose_input == 'y'
    
    # 显示配置摘要
    print()
    print_colored("配置摘要:", Fore.CYAN, Style.BRIGHT)
    print(f"  输入路径: {', '.join(input_paths)}")
    print(f"  输出目录: {output_dir}")
    print(f"  抽帧模式: {mode}")
    print(f"  输出格式: {output_format}")
    if output_format == 'jpg':
        print(f"  图像质量: {quality}")
    
    if mode == 'time':
        print(f"  时间间隔: {interval}秒")
    elif mode == 'count':
        print(f"  提取帧数: {number}")
    elif mode == 'keyframe':
        print(f"  检测灵敏度: {sensitivity}")
    
    print(f"  递归处理: {'是' if recursive else '否'}")
    print(f"  详细信息: {'是' if verbose else '否'}")
    
    # 确认开始
    confirm = input("\n确认开始处理? [Y/n]: ").strip().lower()
    if confirm and confirm != 'y':
        print_info("操作已取消")
        return False
    
    # 返回配置
    return {
        'input_paths': input_paths,
        'output_dir': output_dir,
        'mode': mode,
        'output_format': output_format,
        'quality': quality,
        'interval': interval,
        'number': number,
        'sensitivity': sensitivity,
        'recursive': recursive,
        'verbose': verbose,
        'yes': True
    }

def main():
    """主函数"""
    args = parse_arguments()
    
    # 检查是否提供了足够的参数，否则进入交互式模式
    if not args.input:
        config = interactive_mode()
        if not config:
            return 1
        
        # 使用交互式模式的配置
        input_paths = config['input_paths']
        output_dir = config['output_dir']
        mode = config['mode']
        output_format = config['output_format']
        quality = config['quality']
        interval = config['interval']
        number = config['number']
        sensitivity = config['sensitivity']
        recursive = config['recursive']
        verbose = config['verbose']
        yes = config['yes']
    else:
        # 使用命令行参数
        input_paths = args.input
        output_dir = args.output or 'frames'
        mode = args.mode
        output_format = args.format
        quality = args.quality
        interval = args.interval
        number = args.number
        sensitivity = args.sensitivity
        recursive = args.recursive
        verbose = args.verbose
        yes = args.yes
    
    # 验证参数
    if quality < 1 or quality > 100:
        print_error("图像质量必须在1-100之间")
        return 1
    
    if interval <= 0:
        print_error("时间间隔必须大于0")
        return 1
    
    if number <= 0:
        print_error("提取帧数必须大于0")
        return 1
    
    if sensitivity < 1 or sensitivity > 100:
        print_error("关键帧检测灵敏度必须在1-100之间")
        return 1
    
    # 获取视频文件列表
    video_files = get_input_videos(input_paths, recursive)
    
    if not video_files:
        print_error("没有找到有效的视频文件")
        return 1
    
    print_success(f"找到 {len(video_files)} 个视频文件")
    
    # 检查输出目录是否已存在
    if os.path.exists(output_dir):
        if not yes:
            confirm = input(f"输出目录 '{output_dir}' 已存在，是否继续? [Y/n]: ").strip().lower()
            if confirm and confirm != 'y':
                print_info("操作已取消")
                return 0
    else:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        print_success(f"创建输出目录: {output_dir}")
    
    # 创建提取器实例
    extractor = VideoFrameExtractor(verbose=verbose)
    
    # 显示开始信息
    print()
    print_colored("开始处理视频:", Fore.CYAN, Style.BRIGHT)
    print(f"  抽帧模式: {mode}")
    print(f"  输出格式: {output_format}")
    if output_format == 'jpg':
        print(f"  图像质量: {quality}")
    
    if mode == 'time':
        print(f"  时间间隔: {interval}秒")
    elif mode == 'count':
        print(f"  提取帧数: {number}")
    elif mode == 'keyframe':
        print(f"  检测灵敏度: {sensitivity}")
    
    print()
    
    try:
        # 批量提取帧
        total_extracted = extractor.batch_extract(
            video_files,
            output_dir,
            mode=mode,
            interval=interval,
            number=number,
            sensitivity=sensitivity,
            output_format=output_format,
            quality=quality
        )
        
        print()
        print_success(f"处理完成! 总共提取了 {total_extracted} 帧")
        print_success(f"输出目录: {os.path.abspath(output_dir)}")
        
    except KeyboardInterrupt:
        print()
        print_warning("操作被用户中断")
        return 1
    except Exception as e:
        print_error(f"处理过程中出错: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())