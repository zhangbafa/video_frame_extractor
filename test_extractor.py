"""
测试脚本 - 用于快速测试视频抽帧功能
可以直接运行此脚本而无需安装包
"""

import os
import sys
from video_frame_extractor.extractor import VideoFrameExtractor
from video_frame_extractor.cli import print_header, print_success, print_error, print_info, print_warning

def test_extraction():
    """测试视频帧提取功能"""
    print_header()
    print_info("欢迎使用 Video Frame Extractor 测试脚本")
    print_info("此脚本用于快速测试视频抽帧功能")
    print()
    
    # 获取测试视频路径
    video_path = input("请输入测试视频路径: ").strip()
    
    if not os.path.exists(video_path):
        print_error(f"视频文件不存在: {video_path}")
        return False
    
    # 创建输出目录
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    print_info(f"输出目录: {os.path.abspath(output_dir)}")
    
    # 创建提取器实例
    extractor = VideoFrameExtractor(verbose=True)
    
    print()
    print_info("测试不同的抽帧模式...")
    
    # 测试时间间隔模式
    print()
    print_info("1. 测试时间间隔模式 (每2秒一帧)")
    try:
        extracted = extractor.extract_frames(
            video_path, 
            os.path.join(output_dir, "time_mode"), 
            mode='time', 
            interval=2,
            output_format='jpg',
            quality=90
        )
        print_success(f"时间间隔模式测试完成，提取了 {extracted} 帧")
    except Exception as e:
        print_error(f"时间间隔模式测试失败: {e}")
    
    # 测试固定帧数模式
    print()
    print_info("2. 测试固定帧数模式 (提取10帧)")
    try:
        extracted = extractor.extract_frames(
            video_path, 
            os.path.join(output_dir, "count_mode"), 
            mode='count', 
            number=10,
            output_format='jpg',
            quality=90
        )
        print_success(f"固定帧数模式测试完成，提取了 {extracted} 帧")
    except Exception as e:
        print_error(f"固定帧数模式测试失败: {e}")
    
    # 测试关键帧检测模式
    print()
    print_info("3. 测试关键帧检测模式 (灵敏度50)")
    try:
        extracted = extractor.extract_frames(
            video_path, 
            os.path.join(output_dir, "keyframe_mode"), 
            mode='keyframe', 
            sensitivity=50,
            output_format='jpg',
            quality=90
        )
        print_success(f"关键帧检测模式测试完成，提取了 {extracted} 帧")
    except Exception as e:
        print_error(f"关键帧检测模式测试失败: {e}")
    
    print()
    print_success("测试完成!")
    print_info(f"提取的帧保存在: {os.path.abspath(output_dir)}")
    print_info("您可以比较不同模式下提取的帧的差异")
    
    return True

if __name__ == "__main__":
    try:
        test_extraction()
    except KeyboardInterrupt:
        print()
        print_warning("测试被用户中断")
    except Exception as e:
        print_error(f"测试过程中发生错误: {e}")
    finally:
        input("\n按回车键退出...")