import numpy as np
import cv2
import copy
"""
不做padding,将对应五张操作直接改成opencv 智能补帧的方式
"""

pred_last_index = 84 #推理最后一批次的最后一帧
def frame_filler(num_interpolated_frames: int,src_frame:np.ndarray, dst_frame:np.ndarray, debug:bool=False):
    """补帧函数，使用线性插值生成中间帧
    Args:
        num_interpolated_frames: need filed frame nums 
        src_frame: shape like: h,w,3
        dst_frame: shape like: h,w,3
    Return:
        filled frames
    """
    # 用来调整过渡帧的曲线类型
    t = np.linspace(0,1, num_interpolated_frames+1)
    curve = 1-np.exp(-3.5*t) # 指数 数字越大,变换越缓慢, 目前这个数值下效果较好,sota


    def interpolate_frames(src_frame, dst_frame, alpha):
        interpolated_frame = cv2.addWeighted(src_frame, 1-alpha, dst_frame, alpha, 0)
        return interpolated_frame
    # 生成中间帧
    interpolated_frames = []
    for i in range(1, num_interpolated_frames+1):
        alpha = curve[i]
        print(f'alpha: {alpha}')
        interpolated_frame = interpolate_frames(src_frame, dst_frame, alpha)
        interpolated_frames.append(interpolated_frame)

    # # 显示结果
    if debug:
        count=pred_last_index+1 #推理的下一张
        for i, interpolated_frame in enumerate(interpolated_frames):
            cv2.imwrite(f"tmp/infer_image_{count+i}.jpg", interpolated_frame)

def test_frame():
    # 读取输入的两帧图像
    src_frame = cv2.imread(f'infer_image_{pred_last_index}.jpg') # 推理(最后一批)
    dst_frame = cv2.imread('video_pk/UDpdyce0p9LC2NgD/image/img00069.jpg') # 沉默第一批最后一张 循环帧(读取的原图)
    num_interpolated_frames = 5  # 个别情况下可以考虑增大个数,缓解过渡,一般5或者10能达到较好效果
    frame_filler(num_interpolated_frames, src_frame, dst_frame, debug=True)
