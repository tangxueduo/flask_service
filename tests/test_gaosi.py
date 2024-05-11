import cv2
import numpy as np

input_dir = "data/input"
output_dir = "data/output"
def test_gaosi_img():
    """
    测试高斯平滑原理，不同高斯核的表现
    高斯平滑原理：
        原理: 
            模糊一张图像，可以对每个像素点，以它为中心，取其3x3区域内所有像素灰度值的平均作为中心点的灰度值。
            可是，如果仅使用简单平均，显然不是很合理，因为图像都是连续的，越靠近的点关系越密切，越远离的点关系越疏远。
            因此， ，加权平均更合理，距离越近的点权重越大，距离越远的点权重越小。
            而正态分布显然是一种可取的权重分配模式。由于图像是二维的，所以需要使用二维的高斯函数。


        高斯核选择: 高斯核必须是奇数整数， 如果是0, 会自动由sigma计算出，高斯核越大，锯齿越不明显，但是
        borderType: 图像像素外推方式: 
        参数意思：refer to: https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#gaussianblur

    """
    mask_path = f"{input_dir}/mask33.jpg"
    mask = cv2.imread(mask_path)

    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    cv2.imwrite(f"{output_dir}/erode.jpg", mask)
    print(cv2.BORDER_DEFAULT) # 4
    # TODO:高斯核按照图片尺寸进行调整， 但是具体比例关系不清楚，后面更新
    gaosi_kernel = int(0.1 * mask.shape[0] // 2 * 2) + 1 
    # borderType 表示外充像素方法
    mask = cv2.GaussianBlur(mask, (gaosi_kernel, gaosi_kernel), 0, 0, borderType=cv2.BORDER_DEFAULT)
    cv2.imwrite(f"{output_dir}/15_gaosi.jpg", mask)
