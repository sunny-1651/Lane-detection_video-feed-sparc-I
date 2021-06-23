import os
import cv2
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
x11 = x12 = x21 = x22 = None
def drow_the_lines(img, lines):
    img = np.copy(img)
    blank_image1 = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    blank_image2 = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    s1 = s2 = n1 = n2 = c1 = c2 = 0
    for line in lines:
        for x1, y1, x2, y2 in line:
            z = (y2 - y1) / (x2 - x1)
            c = y1 - (x1 * z)
            if z>0.4:
                s1 = s1 + z
                n1 = n1 + 1
                c1 = c + c1
            elif z<0:
                s2 = s2 + z
                n2 = n2 + 1
                c2 = c + c2
    # print(s1, n1, s2, n2)

    if s1 != 0:
        s1 = s1 / n1
        c1 = c1 / n1
        x11 = int((540 - c1) / s1)
        x21 = int((324 - c1) / s1)
    if s2 != 0:
        s2 = s2 / n2
        c2 = c2 / n2
        x12 = int((540 - c2) / s2)
        x22 = int((324 - c2) / s2)

    cv2.line(blank_image1, (x11, 540), (x21, 324), (255, 0, 0), thickness=10)
    cv2.line(blank_image2, (x12, 540), (x22, 324), (255, 0, 0), thickness=10)

    blank_image = cv2.addWeighted(blank_image2, 1, blank_image1, 1, 0)
    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0)
    return img

def process(image):
    x = image.shape[1]
    y = image.shape[0]
    region_of_interest_vertices = [(0.04 * x, y), (0.46875 * x, 0.62 * y), (0.55 * x, 0.62 * y),
                                   (0.96 * x, y)]
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    canny_image = cv2.Canny(gray_image, 100, 120)
    cropped_image = region_of_interest(canny_image,
                                       np.array([region_of_interest_vertices], np.int32), )
    lines = cv2.HoughLinesP(cropped_image,
                            rho=2, theta=np.pi / 90,
                            threshold=50,
                            lines=np.array([]),
                            minLineLength=1, maxLineGap=100)
    image_with_lines = drow_the_lines(image, lines)
    return image_with_lines

# image = mpimg.imread('test_images/solidWhiteRight.jpg')
# plt.imshow(process(image))
# plt.show()

white_output = "test_videos_output/solidWhiteRight.mp4"
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
white_clip = clip1.fl_image(process)
white_clip.write_videofile(white_output, audio=False)

pics = os.listdir("test_images/")
for x in range(6):
    imr = "test_images/" + pics[x]
    imrs = "test_images_output2/" + pics[x]
    image = mpimg.imread(imr)
    plt.imsave(imrs, process(image))
