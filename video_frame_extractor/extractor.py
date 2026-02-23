"""
视频抽帧核心功能模块
"""

import os
import cv2
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoFrameExtractor:
    """视频帧提取器类"""
    
    def __init__(self, verbose=False):
        """
        初始化视频帧提取器
        
        Args:
            verbose: 是否显示详细信息
        """
        self.verbose = verbose
        if verbose:
            logger.setLevel(logging.DEBUG)
    
    def extract_frames(self, video_path, output_dir, mode='time', interval=1, 
                      number=10, sensitivity=50, output_format='jpg', quality=90):
        """
        从视频中提取帧
        
        Args:
            video_path: 视频文件路径
            output_dir: 输出目录
            mode: 抽帧模式 ('time', 'count', 'keyframe')
            interval: 时间间隔(秒)，用于time模式
            number: 提取帧数，用于count模式
            sensitivity: 关键帧检测灵敏度(1-100)，用于keyframe模式
            output_format: 输出图像格式 ('jpg', 'png')
            quality: 输出图像质量(1-100)，仅jpg有效
            
        Returns:
            提取的帧数
        """
        if not os.path.exists(video_path):
            logger.error(f"视频文件不存在: {video_path}")
            return 0
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取视频文件名（不含扩展名）
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"无法打开视频文件: {video_path}")
            return 0
        
        # 获取视频信息
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        if self.verbose:
            logger.debug(f"视频信息:")
            logger.debug(f"  路径: {video_path}")
            logger.debug(f"  帧率: {fps:.2f} fps")
            logger.debug(f"  总帧数: {total_frames}")
            logger.debug(f"  时长: {duration:.2f} 秒")
            logger.debug(f"  分辨率: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
        
        # 根据模式确定要提取的帧索引
        frame_indices = []
        
        if mode == 'time':
            # 时间间隔模式
            interval_frames = int(interval * fps)
            if interval_frames < 1:
                interval_frames = 1
            frame_indices = list(range(0, total_frames, interval_frames))
            
        elif mode == 'count':
            # 固定帧数模式
            if number <= 0:
                logger.error("提取帧数必须大于0")
                return 0
            
            if number > total_frames:
                logger.warning(f"请求的帧数({number})大于视频总帧数({total_frames})，将提取所有帧")
                frame_indices = list(range(total_frames))
            else:
                # 均匀分布帧索引
                step = total_frames / number
                frame_indices = [int(i * step) for i in range(number)]
                
        elif mode == 'keyframe':
            # 关键帧检测模式
            frame_indices = self._detect_keyframes(cap, sensitivity, total_frames)
            
        else:
            logger.error(f"不支持的抽帧模式: {mode}")
            cap.release()
            return 0
        
        # 提取帧
        extracted_count = 0
        progress_bar = tqdm(frame_indices, desc=f"处理 {video_name}", unit="帧") if self.verbose else frame_indices
        
        for frame_idx in progress_bar:
            # 设置当前帧位置
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            
            # 读取帧
            ret, frame = cap.read()
            if not ret:
                logger.warning(f"无法读取帧 {frame_idx}")
                continue
            
            # 转换BGR为RGB（OpenCV读取的是BGR格式）
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 创建PIL图像
            image = Image.fromarray(frame_rgb)
            
            # 保存图像
            output_filename = f"{video_name}_frame_{frame_idx:06d}.{output_format}"
            output_path = os.path.join(output_dir, output_filename)
            
            if output_format.lower() == 'jpg':
                image.save(output_path, 'JPEG', quality=quality)
            else:  # png
                image.save(output_path, 'PNG')
            
            extracted_count += 1
        
        # 释放视频捕获对象
        cap.release()
        
        logger.info(f"从视频 '{video_name}' 中成功提取 {extracted_count} 帧")
        return extracted_count
    
    def _detect_keyframes(self, cap, sensitivity, total_frames):
        """
        检测视频中的关键帧
        
        Args:
            cap: 视频捕获对象
            sensitivity: 灵敏度(1-100)，值越高检测越敏感
            total_frames: 视频总帧数
            
        Returns:
            关键帧索引列表
        """
        # 将灵敏度转换为阈值（灵敏度越高，阈值越低）
        threshold = 100 - sensitivity
        threshold = max(5, min(95, threshold))  # 限制在5-95范围内
        threshold = threshold / 100.0  # 转换为0-1范围
        
        keyframes = []
        prev_hist = None
        frame_interval = max(1, int(total_frames / 1000))  # 最多检查1000帧
        
        # 读取第一帧作为基准
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, prev_frame = cap.read()
        if not ret:
            return keyframes
        
        # 添加第一帧作为关键帧
        keyframes.append(0)
        
        # 计算第一帧的直方图
        prev_hist = self._calculate_histogram(prev_frame)
        
        # 遍历视频帧
        for i in range(frame_interval, total_frames, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                continue
            
            # 计算当前帧的直方图
            curr_hist = self._calculate_histogram(frame)
            
            # 计算直方图差异
            hist_diff = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_CHISQR)
            
            # 归一化差异值
            hist_diff_norm = hist_diff / (10000 * 256)
            
            # 如果差异超过阈值，认为是关键帧
            if hist_diff_norm > threshold:
                keyframes.append(i)
                prev_hist = curr_hist
                
                if self.verbose:
                    logger.debug(f"检测到关键帧: {i}, 差异值: {hist_diff_norm:.4f}")
        
        # 确保最后一帧也被添加
        if total_frames > 0 and keyframes[-1] != total_frames - 1:
            keyframes.append(total_frames - 1)
        
        return keyframes
    
    def _calculate_histogram(self, frame):
        """
        计算帧的颜色直方图
        
        Args:
            frame: 视频帧
            
        Returns:
            直方图
        """
        # 将帧转换为HSV颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 计算H通道的直方图
        hist = cv2.calcHist([hsv], [0], None, [256], [0, 256])
        
        # 归一化直方图
        cv2.normalize(hist, hist)
        
        return hist
    
    def batch_extract(self, video_paths, output_dir, mode='time', interval=1, 
                     number=10, sensitivity=50, output_format='jpg', quality=90, 
                     max_workers=None):
        """
        批量提取多个视频的帧
        
        Args:
            video_paths: 视频文件路径列表
            output_dir: 输出目录
            mode: 抽帧模式 ('time', 'count', 'keyframe')
            interval: 时间间隔(秒)，用于time模式
            number: 提取帧数，用于count模式
            sensitivity: 关键帧检测灵敏度(1-100)，用于keyframe模式
            output_format: 输出图像格式 ('jpg', 'png')
            quality: 输出图像质量(1-100)，仅jpg有效
            max_workers: 最大工作线程数
            
        Returns:
            总提取帧数
        """
        total_extracted = 0
        
        # 使用线程池并行处理
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            futures = []
            for video_path in video_paths:
                future = executor.submit(
                    self.extract_frames,
                    video_path, output_dir, mode, interval,
                    number, sensitivity, output_format, quality
                )
                futures.append(future)
            
            # 收集结果
            for future in tqdm(futures, desc="处理视频", unit="个") if self.verbose else futures:
                try:
                    extracted = future.result()
                    total_extracted += extracted
                except Exception as e:
                    logger.error(f"处理视频时出错: {e}")
        
        return total_extracted