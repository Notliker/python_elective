import cv2

"""
Абстрактная фабрика 
"""


class AbstractFactoryImageReader:
    def read_image(self, file_path):
        raise NotImplementedError()


class BinImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise RuntimeError(f"Не удалось открыть файл {file_path}")
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary


class MonochromeImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise RuntimeError(f"Не удалось открыть файл {file_path}")
        return image


class ColorImageReader(AbstractFactoryImageReader):
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError(f"Не удалось открыть файл {file_path}")
        return image


def get_image_reader(num):
    if num:
        return BinImageReader()
    elif num == 1:
        return MonochromeImageReader()
    elif num == 2:
        return ColorImageReader()
    else:
        raise ValueError("Неизвестный идентификатор: %s" % num)


if __name__ == "__main__":
    try:
        for i in range(3):
            print(get_image_reader(i))
    except Exception as e:
        print(e)