"""
创建测试视频的脚本
"""

import cv2
import numpy as np
import os

# 创建测试视频目录
os.makedirs('test_video', exist_ok=True)

# 创建一个简单的测试视频
width, height = 640, 480
fps = 20.0
duration = 5  # 5秒
total_frames = int(fps * duration)

# 创建视频写入器
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test_video/sample.mp4', fourcc, fps, (width, height))

print(f"正在创建测试视频，共 {total_frames} 帧...")

# 生成视频帧
for i in range(total_frames):
    # 创建渐变背景
    frame = np.ones((height, width, 3), dtype=np.uint8)
    
    # 根据帧索引设置背景颜色（从黑到白渐变）
    color_value = int(255 * (i / total_frames))
    frame[:, :, :] = color_value
    
    # 添加帧号文本
    text = f'Frame {i}'
    cv2.putText(frame, text, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    
    # 添加一些简单的动画效果
    if i % 30 < 15:  # 每30帧闪烁一次
        cv2.circle(frame, (width//2, height//2), 50, (0, 0, 255), -1)
    
    # 写入帧
    out.write(frame)

# 释放视频写入器
out.release()

print(f"测试视频创建成功: test_video/sample.mp4")
print(f"视频信息: {width}x{height}, {fps}fps, {duration}秒")