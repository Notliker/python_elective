"""
Шаблонный метод (Template method)
"""
import cv2
import numpy as np
class ObjectAnalysis(object):
    def template_method(self, image):
        image = self.noise_filtering(image)
        data = self.segmentation(image)
        data = self.object_parameters(data)
        return data

    def noise_filtering(self, image):
        raise NotImplementedError()

    def segmentation(self, data):
        raise NotImplementedError()

    def object_parameters(self, data):
        (image, output) = data
        (numLabels, labels, stats, centroids) = output
        
        x = []
        y = []
        w = []
        h = []
        area = []
        hu_moments = [] 

        for i in range(1, numLabels):
            x.append(stats[i, cv2.CC_STAT_LEFT])
            y.append(stats[i, cv2.CC_STAT_TOP])
            w.append(stats[i, cv2.CC_STAT_WIDTH])
            h.append(stats[i, cv2.CC_STAT_HEIGHT])
            area.append(stats[i, cv2.CC_STAT_AREA])
            hu_moments.append(None)

        return (x, y, w, h, area, hu_moments, labels)


class BinaryImage(ObjectAnalysis):
    def noise_filtering(self, image):
        return cv2.medianBlur(image, 5)

    def segmentation(self, image):
        output = cv2.connectedComponentsWithStats(image, 4, cv2.CV_32S)
        return (image, output)

class MonochromeImage(BinaryImage):
    def noise_filtering(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    def segmentation(self, image):
        edges = cv2.Canny(image, 50, 150)
        output = cv2.connectedComponentsWithStats(edges, 4, cv2.CV_32S)
        return (edges, output)

class ColorImage(MonochromeImage):
    def noise_filtering(self, image):
        mean = 0
        stddev = 180
        noise = np.zeros(image.shape, np.uint8)
        cv2.randn(noise, mean, stddev)
        noisy_img = cv2.add(image, noise)
        return noisy_img
    
    def segmentation(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
        
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        
        markers = cv2.watershed(image, markers)
        
        mask = np.zeros_like(gray, dtype=np.uint8)
        mask[markers > 1] = 255
        
        output = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
        return (mask, output)

"""
Декоратор - структурный паттерн
"""

class FilteredAnalysis(ObjectAnalysis):
    """
    Декоратор над ObjectAnalysis.
    - фильтрует объекты по площади
    - дополнительно считает Hu-моменты и сохраняет их в self.hu_moments
    """
    def __init__(self, obj):
        self._proc = obj
        self.hu_moments = None

    def template_method(self, image):
        (_x, _y, _w, _h, _area) = self._proc.template_method(image)

        x = []
        y = []
        w = []
        h = []
        area = []

        for i in range(len(_area)):
            if 10 < _area[i] < 2500:
                x.append(_x[i])
                y.append(_y[i])
                w.append(_w[i])
                h.append(_h[i])
                area.append(_area[i])

        try:
            processed = self._proc.noise_filtering(image)
            (seg_image, seg_data) = self._proc.segmentation(processed)
            (numLabels, labels, stats, centroids) = seg_data

            hu_list = []
            for i in range(1, numLabels):
                if 10 < stats[i, cv2.CC_STAT_AREA] < 2500:
                    mask = (labels == i).astype("uint8")
                    m = cv2.moments(mask)
                    hu = cv2.HuMoments(m)
                    hu_list.append(hu)
            self.hu_moments = hu_list
        except Exception:
            self.hu_moments = None

        return (x, y, w, h, area)


if __name__ == '__main__':
    print("Binary Image Processing")
    bin_segm = BinaryImage()
    (x, y, w, h, area) = bin_segm.template_method(
        cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE)
    )
    for i in range(len(area)):
        print([x[i], y[i], w[i], h[i], area[i]])

    print("Decorated Binary Image Processing")
    filt_bin = FilteredAnalysis(BinaryImage())
    (x, y, w, h, area) = filt_bin.template_method(
        cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE)
    )
    for i in range(len(area)):
        print([x[i], y[i], w[i], h[i], area[i]])
