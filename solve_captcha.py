import os
import cv2
import numpy as np
import pickle
from dotenv import load_dotenv

load_dotenv()

template_matching_methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED',
                             'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

method_index = int(os.getenv('TEMPLATE_MATCHING_METHOD_INDEX'))


class CaptchaSolver:
    def __init__(self):
        pass

    def read_templates_data(self, path):
        with open(path, 'rb') as f:
            templates_json = pickle.load(f)
            return templates_json

    def get_character_extents(self, captcha_gray, template_gray, threshold):
        w, h = template_gray.shape[::-1]

        # apply template matching
        res = cv2.matchTemplate(captcha_gray, template_gray, eval(template_matching_methods[method_index]))

        res[res < threshold] = 0
        x = res.flatten()
        loc = np.where(res >= threshold)

        mean = 0
        if len(loc[0]):
            print('mean: ', np.sum(x) / len(loc[0]))
            mean = np.sum(x) / len(loc[0])

        pts_top_left = list()
        pts = list()
        for pt in zip(*loc[::-1]):
            pts.append(pt)

        if pts:
            pts_sorted = sorted(pts, key=lambda x: x[0])
            pt_index = 0
            for i in range(len(pts_sorted)):
                if pts_sorted[i][0] >= pt_index:
                    pts_top_left.append(pts_sorted[i])
                    pt_index = pts_sorted[i][0] + w / 2
                    cv2.rectangle(captcha_gray, pts_sorted[i], (pts_sorted[i][0] + w, pts_sorted[i][1] + h), (0, 0, 255), 2)
        if pts_top_left:
            print(pts_top_left)

        return pts_top_left, mean

    def get_captcha_string(self, templates_json, captcha_image_path):
        captcha_img = cv2.imread(captcha_image_path, cv2.IMREAD_UNCHANGED)
        captcha_gray = 255 - captcha_img[:, :, 3]
        _, captcha_binary = cv2.threshold(captcha_gray, 127, 255, cv2.THRESH_BINARY)
        captcha_binary_inverse = cv2.bitwise_not(captcha_binary)
        result = list()
        n_found = 0
        threshold = float(os.getenv('THRESHOLD'))

        while n_found < 5:
            found_indices = list()
            temp_result = list()
            print('\n')
            for i in range(len(templates_json)):
                pts_top_left, mean = self.get_character_extents(captcha_binary_inverse, templates_json[i]['imageDataArray'], threshold)
                if pts_top_left:
                    print('value: ', templates_json[i]['value'])
                    found_indices.append(i)
                    for pt in pts_top_left:
                        temp_result.append(tuple((templates_json[i]['value'], pt[0], pt[1], mean)))

            temp_result = sorted(temp_result, key=lambda x: x[3], reverse=True)
            for res in temp_result:
                if len(result) < 5:
                    ignore = False
                    for pt in result:
                        if abs(res[1] - pt[1]) < int(os.getenv('AVERAGE_TEMPLATE_WIDTH')) / 2:
                            ignore = True
                    if ignore:
                        continue
                    n_found += 1
                    result.append(res)

            print(temp_result)

            threshold -= float(os.getenv('THRESHOLD_STEP'))
            print('result: ', result)

        result = sorted(result, key=lambda x: x[1])
        captcha_string = ''.join(str(res[0]) for res in result)
        return captcha_string
