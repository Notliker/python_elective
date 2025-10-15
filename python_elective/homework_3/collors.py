class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = None
    
    def get_type(self):
        pass
    
    def get_shape(self):
        return (self.height, self.width)
    
    def save_jpg(self, filename):
        """Save image in JPG format"""
        pass


class BinaryImage(Image):
    def __init__(self, width, height, data=None):
        super().__init__(width, height)
        if data is not None:
            self.data = [[bool(data[i][j]) for j in range(width)] for i in range(height)]
        else:
            self.data = [[False for _ in range(width)] for _ in range(height)]
    
    def get_type(self):
        return "Binary"
    
    def save_jpg(self, filename):
        """Save binary image as JPG"""
        try:
            from PIL import Image as PILImage
            
            pil_img = PILImage.new('L', (self.width, self.height))
            pixels = pil_img.load()
            
            for i in range(self.height):
                for j in range(self.width):
                    pixels[j, i] = 255 if self.data[i][j] else 0
            
            pil_img.save(filename, 'JPEG', quality=95)
            print(f"Binary image saved to {filename}")
        except ImportError:
            print("PIL/Pillow required for JPG. Install: pip install Pillow")
        except Exception as e:
            print(f"Error saving JPG: {e}")


class MonochromeImage(Image):
    def __init__(self, width, height, data=None):
        super().__init__(width, height)
        if data is not None:
            self.data = [[max(0, min(255, int(data[i][j]))) for j in range(width)] for i in range(height)]
        else:
            self.data = [[0 for _ in range(width)] for _ in range(height)]
    
    def get_type(self):
        return "Monochrome"
    
    def save_jpg(self, filename):
        """Save monochrome image as JPG"""
        try:
            from PIL import Image as PILImage
            
            pil_img = PILImage.new('L', (self.width, self.height))
            pixels = pil_img.load()
            
            for i in range(self.height):
                for j in range(self.width):
                    pixels[j, i] = self.data[i][j]
            
            pil_img.save(filename, 'JPEG', quality=95)
            print(f"Monochrome image saved to {filename}")
        except ImportError:
            print("PIL/Pillow required for JPG. Install: pip install Pillow")
        except Exception as e:
            print(f"Error saving JPG: {e}")


class ColorImage(Image):
    def __init__(self, width, height, data=None):
        super().__init__(width, height)
        if data is not None:
            self.data = [[[max(0, min(255, int(data[i][j][k]))) for k in range(3)] for j in range(width)] for i in range(height)]
        else:
            self.data = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
    
    def get_type(self):
        return "Color"
    
    def save_jpg(self, filename):
        """Save color image as JPG"""
        try:
            from PIL import Image as PILImage
            
            pil_img = PILImage.new('RGB', (self.width, self.height))
            pixels = pil_img.load()
            
            for i in range(self.height):
                for j in range(self.width):
                    r, g, b = self.data[i][j]
                    pixels[j, i] = (r, g, b)
            
            pil_img.save(filename, 'JPEG', quality=95)
            print(f"Color image saved to {filename}")
        except ImportError:
            print("PIL/Pillow required for JPG. Install: pip install Pillow")
        except Exception as e:
            print(f"Error saving JPG: {e}")


class ImageConverter:
    @staticmethod
    def convert(source_image, target_type, **kwargs):
        """Universal image converter"""
        source_type = source_image.get_type()
        
        if source_type == target_type:
            return ImageConverter._convert_same_type(source_image, **kwargs)
        
        conversion_map = {
            ("Color", "Monochrome"): ImageConverter._color_to_monochrome,
            ("Color", "Binary"): ImageConverter._color_to_binary,
            ("Monochrome", "Color"): ImageConverter._monochrome_to_color,
            ("Monochrome", "Binary"): ImageConverter._monochrome_to_binary,
            ("Binary", "Monochrome"): ImageConverter._binary_to_monochrome,
            ("Binary", "Color"): ImageConverter._binary_to_color,
        }
        
        converter_func = conversion_map.get((source_type, target_type))
        if converter_func:
            return converter_func(source_image, **kwargs)
        else:
            raise ValueError(f"Conversion from {source_type} to {target_type} not supported")
    
    @staticmethod
    def _convert_same_type(image, **kwargs):
        """Convert image of same type with corrections"""
        if image.get_type() == "Monochrome":
            return ImageConverter._monochrome_correction(image)
        elif image.get_type() == "Color":
            return ImageConverter._color_correction(image)
        elif image.get_type() == "Binary":
            new_data = [[image.data[i][j] for j in range(image.width)] for i in range(image.height)]
            return BinaryImage(image.width, image.height, new_data)
    
    @staticmethod
    def _monochrome_correction(image):
        """Statistical color correction for monochrome"""
        total = 0
        count = image.width * image.height
        for i in range(image.height):
            for j in range(image.width):
                total += image.data[i][j]
        mean = total / count
        
        variance_sum = 0
        for i in range(image.height):
            for j in range(image.width):
                variance_sum += (image.data[i][j] - mean) ** 2
        std = (variance_sum / count) ** 0.5
        
        new_data = [[0 for _ in range(image.width)] for _ in range(image.height)]
        min_val = float('inf')
        max_val = float('-inf')
        
        for i in range(image.height):
            for j in range(image.width):
                normalized = (image.data[i][j] - mean) / (std + 1e-8)
                new_data[i][j] = normalized
                if normalized < min_val:
                    min_val = normalized
                if normalized > max_val:
                    max_val = normalized
        
        for i in range(image.height):
            for j in range(image.width):
                new_data[i][j] = int((new_data[i][j] - min_val) / (max_val - min_val + 1e-8) * 255)
        
        return MonochromeImage(image.width, image.height, new_data)
    
    @staticmethod
    def _color_correction(image):
        """Per-channel statistical color correction"""
        corrected = [[[0 for _ in range(3)] for _ in range(image.width)] for _ in range(image.height)]
        
        for channel in range(3):
            total = 0
            count = image.width * image.height
            for i in range(image.height):
                for j in range(image.width):
                    total += image.data[i][j][channel]
            mean = total / count
            
            variance_sum = 0
            for i in range(image.height):
                for j in range(image.width):
                    variance_sum += (image.data[i][j][channel] - mean) ** 2
            std = (variance_sum / count) ** 0.5
            
            temp = [[0 for _ in range(image.width)] for _ in range(image.height)]
            min_val = float('inf')
            max_val = float('-inf')
            
            for i in range(image.height):
                for j in range(image.width):
                    normalized = (image.data[i][j][channel] - mean) / (std + 1e-8)
                    temp[i][j] = normalized
                    if normalized < min_val:
                        min_val = normalized
                    if normalized > max_val:
                        max_val = normalized
            
            for i in range(image.height):
                for j in range(image.width):
                    corrected[i][j][channel] = int((temp[i][j] - min_val) / (max_val - min_val + 1e-8) * 255)
        
        return ColorImage(image.width, image.height, corrected)
    
    @staticmethod
    def _color_to_monochrome(image, **kwargs):
        """Color to Monochrome"""
        gray = [[0 for _ in range(image.width)] for _ in range(image.height)]
        for i in range(image.height):
            for j in range(image.width):
                gray[i][j] = (image.data[i][j][0] + image.data[i][j][1] + image.data[i][j][2]) // 3
        return MonochromeImage(image.width, image.height, gray)
    
    @staticmethod
    def _monochrome_to_color(image, palette=None, **kwargs):
        """Monochrome to Color"""
        if palette is None:
            palette = [[i, i, i] for i in range(256)]
        
        color_data = [[[0, 0, 0] for _ in range(image.width)] for _ in range(image.height)]
        for i in range(image.height):
            for j in range(image.width):
                gray_value = image.data[i][j]
                color_data[i][j] = palette[gray_value]
        
        return ColorImage(image.width, image.height, color_data)
    
    @staticmethod
    def _monochrome_to_binary(image, threshold=None, **kwargs):
        """Monochrome to Binary"""
        if threshold is None:
            threshold = ImageConverter._otsu_threshold(image)
        
        binary = [[False for _ in range(image.width)] for _ in range(image.height)]
        for i in range(image.height):
            for j in range(image.width):
                binary[i][j] = image.data[i][j] > threshold
        
        return BinaryImage(image.width, image.height, binary)
    
    @staticmethod
    def _binary_to_monochrome(image, **kwargs):
        """Binary to Monochrome"""
        distances = ImageConverter._distance_transform(image)
        
        max_dist = 0
        for i in range(image.height):
            for j in range(image.width):
                if distances[i][j] > max_dist:
                    max_dist = distances[i][j]
        
        if max_dist > 0:
            normalized = [[int(distances[i][j] / max_dist * 255) for j in range(image.width)] for i in range(image.height)]
        else:
            normalized = [[0 for _ in range(image.width)] for _ in range(image.height)]
        
        return MonochromeImage(image.width, image.height, normalized)
    
    @staticmethod
    def _color_to_binary(image, threshold=None, **kwargs):
        """Color to Binary: via monochrome"""
        mono = ImageConverter._color_to_monochrome(image)
        return ImageConverter._monochrome_to_binary(mono, threshold)
    
    @staticmethod
    def _binary_to_color(image, palette=None, **kwargs):
        """Binary to Color: via monochrome"""
        mono = ImageConverter._binary_to_monochrome(image)
        return ImageConverter._monochrome_to_color(mono, palette)
    
    @staticmethod
    def _otsu_threshold(image):
        """Otsu's method for automatic threshold"""
        histogram = [0] * 256
        for i in range(image.height):
            for j in range(image.width):
                histogram[image.data[i][j]] += 1
        
        total_pixels = image.width * image.height
        
        total_sum = 0
        for i in range(256):
            total_sum += i * histogram[i]
        
        sum_background = 0
        weight_background = 0
        max_variance = 0
        threshold = 0
        
        for t in range(256):
            weight_background += histogram[t]
            if weight_background == 0:
                continue
            
            weight_foreground = total_pixels - weight_background
            if weight_foreground == 0:
                break
            
            sum_background += t * histogram[t]
            
            mean_background = sum_background / weight_background
            mean_foreground = (total_sum - sum_background) / weight_foreground
            
            variance = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
            
            if variance > max_variance:
                max_variance = variance
                threshold = t
        
        return threshold
    
    @staticmethod
    def _distance_transform(image):
        """Distance transform using two-pass algorithm"""
        INF = image.width * image.height
        distances = [[INF for _ in range(image.width)] for _ in range(image.height)]
        
        for i in range(image.height):
            for j in range(image.width):
                if image.data[i][j]:
                    distances[i][j] = 0
        
        for i in range(image.height):
            for j in range(image.width):
                if distances[i][j] > 0:
                    if i > 0:
                        distances[i][j] = min(distances[i][j], distances[i-1][j] + 1)
                    if j > 0:
                        distances[i][j] = min(distances[i][j], distances[i][j-1] + 1)
                    if i > 0 and j > 0:
                        distances[i][j] = min(distances[i][j], distances[i-1][j-1] + 1.414)
                    if i > 0 and j < image.width - 1:
                        distances[i][j] = min(distances[i][j], distances[i-1][j+1] + 1.414)
        
        for i in range(image.height - 1, -1, -1):
            for j in range(image.width - 1, -1, -1):
                if distances[i][j] > 0:
                    if i < image.height - 1:
                        distances[i][j] = min(distances[i][j], distances[i+1][j] + 1)
                    if j < image.width - 1:
                        distances[i][j] = min(distances[i][j], distances[i][j+1] + 1)
                    if i < image.height - 1 and j < image.width - 1:
                        distances[i][j] = min(distances[i][j], distances[i+1][j+1] + 1.414)
                    if i < image.height - 1 and j > 0:
                        distances[i][j] = min(distances[i][j], distances[i+1][j-1] + 1.414)
        
        return distances


class ImageLoader:
    @staticmethod
    def load_from_pil(filename):
        """Load image using PIL and convert to ColorImage"""
        from PIL import Image as PILImage
        
        pil_img = PILImage.open(filename)
        pil_img = pil_img.convert('RGB')
        
        width, height = pil_img.size
        data = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
        
        pixels = pil_img.load()
        for i in range(height):
            for j in range(width):
                r, g, b = pixels[j, i]
                data[i][j] = [r, g, b]
        
        return ColorImage(width, height, data)


print("\n" + "="*60)
print("LOADING IMAGE: image.jpg")
print("="*60)

img = ImageLoader.load_from_pil("homework_3/image.jpg")

if img is not None:
    print(f"Loaded: {img.width}x{img.height} pixels\n")
    
    # 1. Monochrome -> Monochrome 
    print("1. Monochrome -> Monochrome (statistical correction)")
    mono = ImageConverter.convert(img, "Monochrome")
    mono_corrected = ImageConverter.convert(mono, "Monochrome")
    mono_corrected.save_jpg("homework_3/1_mono_corrected.jpg")
    
    # 2. Color -> Color 
    print("2. Color -> Color (per-channel correction)")
    color_corrected = ImageConverter.convert(img, "Color")
    color_corrected.save_jpg("homework_3/2_color_corrected.jpg")
    
    # 3. Binary -> Binary 
    print("3. Binary -> Binary (no changes)")
    binary = ImageConverter.convert(mono, "Binary")
    binary_same = ImageConverter.convert(binary, "Binary")
    binary_same.save_jpg("homework_3/3_binary_same.jpg")
    
    # 4. Color -> Monochrome 
    print("4. Color -> Monochrome")
    mono_from_color = ImageConverter.convert(img, "Monochrome")
    mono_from_color.save_jpg("homework_3/4_color_to_mono.jpg")
    
    # 5. Monochrome -> Color 
    print("5. Monochrome -> Color (with palette)")
    palette = [[i, i, i] for i in range(256)]
    color_from_mono = ImageConverter.convert(mono, "Color", palette=palette)
    color_from_mono.save_jpg("homework_3/5_mono_to_color.jpg")
    
    # 6. Monochrome -> Binary 
    print("6. Monochrome -> Binary (Otsu threshold)")
    binary_otsu = ImageConverter.convert(mono, "Binary")
    binary_otsu.save_jpg("homework_3/6_mono_to_binary.jpg")
    
    # 7. Binary -> Monochrome 
    print("7. Binary -> Monochrome (distance transform)")
    mono_from_binary = ImageConverter.convert(binary, "Monochrome")
    mono_from_binary.save_jpg("homework_3/7_binary_to_mono.jpg")
    
    # 8. Color -> monochrome -> Binary 
    print("8. Color -> Binary")
    binary_from_color = ImageConverter.convert(img, "Binary")
    binary_from_color.save_jpg("homework_3/8_color_to_binary.jpg")
    
    # 9. Binary -> monochrome -> Color 
    print("9. Binary -> Color")
    color_from_binary = ImageConverter.convert(binary, "Color")
    color_from_binary.save_jpg("homework_3/9_binary_to_color.jpg")

