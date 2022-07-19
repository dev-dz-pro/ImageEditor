import cv2
import numpy as np
from scipy.ndimage import interpolation as inter


def correct_skew(image, delta=1, limit=15):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
            borderMode=cv2.BORDER_REPLICATE)

    return best_angle, corrected


def skew_im(file_in=''):
    file_out = file_in.replace('.', '_out.')
    image = cv2.imread(file_in)
    angle, corrected = correct_skew(image)
    # print('Skew angle:', angle)
    cv2.imwrite(file_out, corrected)
    return file_out
    # cv2.imshow('corrected', corrected)
    # cv2.waitKey()


# if __name__ == '__main__':
#     skew_im(file_in=r'data/lea_169.png')
