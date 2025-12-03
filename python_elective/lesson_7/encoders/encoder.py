import json
import csv
import struct

class HistEncoder:
    def encode(self, filepath, data):
        raise NotImplementedError()

class TxtHistEncoder(HistEncoder):
    def encode(self, filepath, data):
        with open(filepath, 'w') as f:
            f.write(str(data))

class BinHistEncoder(HistEncoder):
    def encode(self, file_path, data):
        values = [float(data.get(i, 0.0)) for i in range(256)]
        with open(file_path, "wb") as file:
            packed = struct.pack("f" * len(values), *values)
            file.write(packed)

class JsonHistEncoder(HistEncoder):
    def encode(self, filepath, data):
        with open(filepath, 'w') as f:
            if hasattr(data, 'tolist'):
                data = data.tolist()
            json.dump(data, f)

class CsvHistEncoder(HistEncoder):
    def encode(self, filepath, data):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data if isinstance(data, list) else list(data))
