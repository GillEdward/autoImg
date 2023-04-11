import cv2
import os
import numpy as np

imgPerLine = 5
linePerPage = 4
BasicWidth = 6000
BasicHeight = 1000
transparentThreshold = 120	# 如果出现透明底图片被全部变成白色, 可以调高该阈值

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
	try:
		depth = img.shape[2]	# 图像通道数
	except IndexError:	# 灰度图没有.shpae[2], 直接将depth赋值为3
		depth = 3

	if depth == 4:
		print('Processing Transparent Background...')
		img = borderSlicer(img, width, height)	# 消除透明底图片的多余边界
		height = img.shape[0]
		width = img.shape[1]
		for x in range(width):	# 手动白底
			for y in range(height):
				if img[y][x][3] <= transparentThreshold:
					img[y][x][3] = 255
					for i in range(3):
						img[y][x][i] = 255
	#print(height, width)

	width = int((width / height) * BasicHeight)
	height = BasicHeight

	img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA) 	# 将图片高度标准化到BasicHeightpx
	
	cv2.imwrite('./input/' + file, img)

'''
1、基准高度BasicHeight, 将5张图片转为n*BasicHeight, 然后拼接在一起
2、基准宽度范围BasicWidth, 若n大于BasicWidth, 则回到1, 尝试减少1张
3、若n小于BasicWidth, 将连接在一起的图片宽度等比放大到BasicWidth
4、linePerPage列为一张，生成组合图
'''

def stitchingOnX(prepareImg):
	imgList = []
	widthSum = 0
	for file in prepareImg:
		imgList.append(cv2.imread('./input/' + file, 3))
		widthSum += imgList[-1].shape[1]
	print('widthSum: ' + str(widthSum))
	
	img = np.concatenate(imgList, axis=1)	# 将图片横向拼接并保存到数组
	width = img.shape[1]

	if width > BasicWidth:	# 若超出最大宽度, 则减少一张
		print('Bigger than BasicWidth!')
		return stitchingOnX(prepareImg[:-1])
	return img, len(prepareImg)	# 返回合成图和使用图片数

pageCounter = 0
while len(files) > linePerPage * imgPerLine:
	lineImg = []	# 横向拼接
	
	for i in range(linePerPage):
		img, imgUsed = stitchingOnX(files[:imgPerLine])
	
		height = img.shape[0]
		width = img.shape[1]
		height = int((height / width) * BasicWidth)
		width = BasicWidth
	
		img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA) 	# 将图片宽度标准化到BasicWidth
		lineImg.append(img)
		del files[:imgUsed]	# 删除拼接过的图
	
	output = np.concatenate(lineImg, axis = 0)
	cv2.imwrite('./output/' + str(pageCounter) + '.png', output)
	print('imgOutput_' + str(pageCounter) + '\n\n')
	pageCounter += 1
