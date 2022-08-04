# This file is an INTEGRAL part of the program VisaHelper

#     Copyright (C) 2022  Tom Zhang

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published by
#     the Free Software Foundation, AGPL-3.0-only.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import onnxruntime
import cv2
import numpy as np
import math

class Predictonnx:
    def __init__(self,path_onnx,path_label):
        with open(path_label, 'r',encoding='utf-8') as r:
            self.character = r.read().splitlines()
        self.character.insert(0, 'blank')
        self.session = onnxruntime.InferenceSession(path_onnx)
        self.input_name = self.session.get_inputs()[0].name
        inputs = self.session.get_inputs()
        self.rec_image_shape = inputs[0].shape[1:]
    def decode(self,text_index, text_prob=None, is_remove_duplicate=False):
        """ convert text-index into text-label. """
        result_list = []
        ignored_tokens = [0]
        batch_size = len(text_index)
        for batch_idx in range(batch_size):
            char_list = []
            conf_list = []
            for idx in range(len(text_index[batch_idx])):
                if text_index[batch_idx][idx] in ignored_tokens:
                    continue
                if is_remove_duplicate:
                    # only for predict
                    if idx > 0 and text_index[batch_idx][idx - 1] == text_index[
                        batch_idx][idx]:
                        continue
                char_list.append(self.character[int(text_index[batch_idx][
                                                   idx])])
                if text_prob is not None:
                    conf_list.append(text_prob[batch_idx][idx])
                else:
                    conf_list.append(1)
            text = ''.join(char_list)
            result_list.append((text, np.mean(conf_list)))
        return result_list

    def detect(self,preds):
        preds_idx = preds.argmax(axis=2)
        preds_prob = preds.max(axis=2)
        text = self.decode(preds_idx, preds_prob, is_remove_duplicate=True)
        return text
    def resize_norm_img(self,img, max_wh_ratio):
        imgC, imgH, imgW = self.rec_image_shape
        assert imgC == img.shape[2]
        # max_wh_ratio = max(max_wh_ratio, imgW / imgH)
        # imgW = int((32 * max_wh_ratio))
        imgW = 128
        h, w = img.shape[:2]
        ratio = w / float(h)
        if math.ceil(imgH * ratio) > imgW:
            resized_w = imgW
        else:
            resized_w = int(math.ceil(imgH * ratio))
        resized_image = cv2.resize(img, (resized_w, imgH))

        resized_image = resized_image.astype('float32')
        resized_image = resized_image.transpose((2, 0, 1)) / 255
        resized_image -= 0.5
        resized_image /= 0.5
        padding_im = np.zeros((imgC, imgH, imgW), dtype=np.float32)
        padding_im[:, :, 0:resized_w] = resized_image
        return padding_im

    def __call__(self,img):
        img = self.resize_norm_img(img, 10.0)

        ort_inputs = {self.input_name: img[None, :, :, :]}
        output = self.session.run(None, ort_inputs)[0]
        text = self.detect(output)
        return text

if __name__ == '__main__':
    onnx = Predictonnx('ocr.onnx','train_data/labels.txt')
