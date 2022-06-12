import cv2
import numpy as np
from matplotlib import pyplot as plt

class compareImg :
    def __init__(self) :
        pass

    def readImg(self, filepath) :
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

        scale_percent = 50  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        # cv2.namedWindow("root", cv2.WINDOW_NORMAL) # window 생성
        # cv2.imshow("root", img) # window에 이미지 띄우기
        # cv2.waitKey(5000) # 5초 기다림. 아무키나 입력되면 대기 종료
        # cv2.destroyAllWindows() # window 제거
        return img


    def diffImg(self, img1, img2) :
        # Initiate SIFT detector
        #feature_match = cv2.ORB_create()
        feature_match = cv2.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = feature_match.detectAndCompute(img1, None)
        kp2, des2 = feature_match.detectAndCompute(img2, None)

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1,des2)

        # Sort them in the order of their distance.
        matches = sorted(matches, key = lambda x:x.distance)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        # Draw first 10 matches.
        knn_image = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
        plt.title("match count:" + str(len(good)))
        plt.imshow(knn_image)
        plt.axis("off")
        plt.show()

    def run(self) :
        # 이미지 파일 경로 설정
        filepath1 = r"images\LM-world1.PNG"
        filepath2 = r"images\LM-world4.PNG"
        
        # 이미지 객체 가져옴
        img1 = self.readImg(filepath1)
        img2 = self.readImg(filepath2)

        self.diffImg(img1, img2)

if __name__ == '__main__':
    cImg = compareImg()
    cImg.run()
