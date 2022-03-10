import argparse
import sys
from pathlib import Path
import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import time
from models.experimental import attempt_load
from utils.augmentations import Albumentations, augment_hsv, copy_paste, letterbox
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_imshow, check_requirements, check_suffix, colorstr, is_ascii, \
    non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
    # save_one_box
from utils.plots import Annotator, colors
# from utils.torch_utils import select_device, load_classifier, time_sync
from utils.torch_utils import select_device, time_sync

def detect(weights, imgsz, image):
  device,half = '', False
  device = select_device(device)
  half &= device.type != 'cpu'
  model = attempt_load(weights, map_location=device)  # load FP32 model
  stride = int(model.stride.max())  # model stride
  names = model.module.names if hasattr(model, 'module') else model.names  # get class names
  if half:
    model.half()  # to FP16
  imgsz = check_img_size(imgsz, s=stride)
  image_orig=image.copy()
  # Padded resize
  im0 = image
  img = letterbox(image, imgsz, stride=stride, auto=True)[0]
  names = model.module.names if hasattr(model, 'module') else model.names
  ascii = is_ascii(names)
  # Convert
  img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
  img = np.ascontiguousarray(img)
  # bs = 1  # batch_size  
  dt, seen = [0.0, 0.0, 0.0], 0
  t1 = time_sync()
  img = torch.from_numpy(img).to(device)
  img = img.half() if half else img.float()  # uint8 to fp16/32
  img = img / 255.0  # 0 - 255 to 0.0 - 1.0
  if len(img.shape) == 3:
      img = img[None]  # expand for batch dim
  t2 = time_sync()
  dt[0] += t2 - t1
  pred = model(img, augment=False, visualize=False)[0]
  t3 = time_sync()
  dt[1] += t3 - t2

  # NMS
  pred = non_max_suppression(pred, 0.20, 0.10, None, False, max_det=1000)
  # print(pred)
  dt[2] += time_sync() - t3
  for i, det in enumerate(pred):
    seen += 1
    gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # norma
    display_str_list = []
    display_str_dict={}
    annotator = Annotator(im0, line_width=2, pil=not ascii)
    if len(det):
    #   # Rescale boxes from img_size to im0 size
      det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
      for *xyxy, conf, cls in reversed(det):
        c = int(cls)  # integer class
        label = None if False else (names[c] if True else f'{names[c]} {conf:.2f}') #Label
        annotator.box_label(xyxy, None, color=colors(c, True))
        label = f'{names[int(cls)]} {conf:.2f}'
        x1=int(xyxy[0].item())
        y1=int(xyxy[1].item())
        x2=int(xyxy[2].item())
        y2=int(xyxy[3].item())

        display_str_dict = {
            'name': names[int(cls)],
            'score': f'{conf:.2f}',
            'ymin': y1,
            'xmin': x1,
            'ymax': y2,
            'xmax': x2,
            'image': image_orig[y1-10:y2+10,x1-10:x2+10]}
        display_str_list.append(display_str_dict)
    
    return im0 , display_str_list



