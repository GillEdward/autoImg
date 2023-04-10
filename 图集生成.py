import cv2
import os
import numpy as np

def borderSlicer(img, width, height):
	minX = width
	minY = height
	maxX = 0
	maxY = 0

	gap = 10

	for x in range(0, width, gap):
		for y in range(0, height, gap):
			if img[y][x][3] != 0:
				if x < minX:
					minX = x
				if y < minY:
					minY = y
				if x > maxX:
					maxX = x
				if y > maxY:
					maxY = y

	minX -= gap
	minY -= gap
	maxX += gap
	maxY += gap
	img_ = img[minY:maxY, minX:maxX]
	#print(minX, minY, maxX, maxY)

	return img_

files = os.listdir('./input')

for file in files:	# 预处理
	img = cv2.imread('./input/' + file, -1)
	height = img.shape[0]
	width = img.shape[1]
	depth = img.shape[2]	# 图像通道数

	if depth == 4 and (img[0][0][3] == 0 or img[height - 1][width - 1][3] == 0):
		img = borderSlicer(img, width, height)	# 消除透明底图片的多余边界

	height = img.shape[0]	# 去除透明边界后的长宽
	width = img.shape[1]
	#print(height, width)

	width = int((width / height) * 1000)
	height = 1000

	img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA) 	# 将图片高度标准化到1000px
	
	cv2.imwrite('./input/' + file, img)

'''
1、基准高度1000px, 将5张图片转为n*1000px, 然后拼接在一起
2、基准宽度范围7000, 若n大于7000px, 则回到1, 尝试减少1张
3、若n小于7000px, 将连接在一起的图片宽度等比放大到6000px
4、6列为一张，生成6000*6000px的组合图
'''

# 横向拼接
prepareImg = files[:5]	# 取五张图准备

imgList = []
widthSum = 0
for file in prepareImg:
	imgList.append(cv2.imread('./input/' + file, -1))
	widthSum += imgList[-1].shape[1]
print('widthSum: ' + str(widthSum))

line = np.concatenate(imgList, axis=1)
cv2.imwrite('./output/' + '1.png', line)