import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as compare_ssim
import numpy as np

class compareImage :
    def __init__(self) :
        pass

    def readImg(self, filepath) :
        img = cv2.imread(filepath)
        # scale_percent = 50  # percent of original size
        # width = int(img.shape[1] * scale_percent / 100)
        # height = int(img.shape[0] * scale_percent / 100)
        # dim = (width, height)
        dim = (900, 500)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return img


    def diffImg(self, src, dest, gridX, gridY) :
        if src.shape[0] != dest.shape[0] or src.shape[1] != dest.shape[1]:
            return

        srcGray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        destGray = cv2.cvtColor(dest, cv2.COLOR_BGR2GRAY)
        score, diff = compare_ssim(srcGray, destGray, full=True)
        diff = (diff * 255).astype('uint8')
        print(f'SSIM: {score:.6f}')

        # #_, thresh = cv2.threshold(diff, 0, 200, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        _, thresh = cv2.threshold(diff, 128, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 400:
                x, y, w, h = cv2.boundingRect(c)
                newSrc = srcGray[y:y+h, x:x+w]
                newDest = destGray[y:y+h, x:x+w]
                newScore, _ = compare_ssim(newSrc, newDest, full=True)
                print(f'new SSIM: {newScore:.6f}')
                print(x, y, w, h)
                cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.drawContours(dest, [c], -1, (0, 0, 255), 2)

        """
        gridXCount = src.shape[1]/gridX
        gridYCount = src.shape[0]/gridY

        for x in range(gridXCount):
            for y in range(gridYCount):
                startX = x * gridX
                startY = y * gridY
                EndX = startX + gridX
                EndY = startY + gridY

                srcGrid = src[startX:EndX, startY:EndY].copy()
                destGrid = src[startX:EndX, startY:EndY].copy()
        """
        cv2.imshow("Original", src)
        cv2.imshow("Modified", dest)
        cv2.imshow("newOriginal", newSrc)
        cv2.imshow("newModified", newDest)
        cv2.waitKey(0)

    def run(self) :
        # 이미지 파일 경로 설정
        filepath1 = "images\world1.PNG"
        filepath2 = "images\world2.PNG"
        
        # 이미지 객체 가져옴
        img1 = self.readImg(filepath1)
        img2 = self.readImg(filepath2)

        self.diffImg(img1, img2, 18, 10)

if __name__ == '__main__':
    cImg = compareImage()
    cImg.run()
