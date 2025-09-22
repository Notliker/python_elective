import sys
import argparse

from utils.reader import image_reader as imread
from utils.reader import csv_reader, bin_reader, txt_reader, json_reader
from utils.processor import histogram
from utils.image_toner import equalization, gamma_correction
from utils.writer import csv_writer, bin_writer, txt_writer, image_writer, json_writer
from utils.image_toner import stat_correction

img_type = {'jpg', 'jpeg', 'png'}

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-img', '--img_path', required=True, help='Path to image (base image)')
    parser.add_argument('-p', '--path', required=True, help='Input file path (template or second image)')
    parser.add_argument('-o', '--output', required=True, help='Save file path')

    parser.add_argument('--mode', choices=['hist', 'gamma', 'equalize', 'stat'], default='gamma', 
                        help='Operation mode: hist (compute histogram), gamma (alpha/beta), equalize (HE), stat (match stats)')
    parser.add_argument('--alpha', type=float, default=1.0, help='Contrast scale for gamma/linear correction')
    parser.add_argument('--beta', type=float, default=0.0, help='Brightness shift for gamma/linear correction')
    return parser

def write_by_ext(out_path, data):
    ext = out_path.split('.')[-1].lower()
    if ext in img_type:
        image_writer.write_data(out_path, data)
    elif ext == 'json':
        json_writer.write_data(out_path, data)
    elif ext == 'csv':
        csv_writer.write_data(out_path, data)
    elif ext == 'bin':
        bin_writer.write_data(out_path, data)
    elif ext == 'txt':
        txt_writer.write_data(out_path, data)
    else:
        raise ValueError(f'Unsupported output extension: .{ext}')

if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args(sys.argv[1:])

    image = imread.read_data(args.img_path)
    base_hist = histogram.image_processing(image)

    file_type = args.path.split('.')[-1].lower()
    input_kind = 'img' if file_type in img_type else file_type

    img2 = None
    hist_template = None
    if input_kind == 'img':
        img2 = imread.read_data(args.path)
    elif input_kind == 'csv':
        hist_template = csv_reader.read_data(args.path)
    elif input_kind == 'bin':
        hist_template = bin_reader.read_data(args.path)
    elif input_kind == 'txt':
        hist_template = txt_reader.read_data(args.path)
    elif input_kind == 'json':
        hist_template = json_reader.read_data(args.path)

    if args.mode == 'hist':
        write_by_ext(args.output, base_hist)
    elif args.mode == 'gamma':
        res_image = gamma_correction.gamma_correction(img2, alpha=args.alpha, beta=args.beta)
        image_writer.write_data(args.output, res_image)
    elif args.mode == 'equalize':
        eq = equalization.equalization(img2)
        image_writer.write_data(args.output, eq)
    elif args.mode == 'stat':
        if input_kind == 'img':
            hist_template = histogram.image_processing(img2)
        if hist_template is None:
            raise ValueError('For --mode stat provide --path with image or histogram file')
        res_image = stat_correction.processing(hist_template, image)
        image_writer.write_data(args.output, res_image)
