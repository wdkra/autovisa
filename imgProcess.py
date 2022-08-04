# This file is an unnecessary part of the program VisaHelper

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

import io
import os
import base64
# from PIL import Image
from OCR.ocr import autoCaptcha

# def analyzeForm(img_data64):
#     imgForm = Image.open(io.BytesIO(base64.b64decode(img_data64.encode())))
#     print(f'form is {data_f.format}')
#     return imgForm.format

def b2img(number, img_data64, imgForm, FriendlyName = 'DELETABLE_tempCaptchaImg_'):
    path_Img = f'C:\\{FriendlyName}{number}.{imgForm}'
    with open(path_Img,'wb') as imgdata:
        imgdata.write(base64.b64decode(img_data64))
        print(f'captcha img.jpeg has been saved. path: {path_Img}')
    ocr = autoCaptcha()
    with open(path_Img, 'rb') as f:
        image = f.read()
        res = ocr.classification(image)
        print(f'OCR prediction(imgProcess.py): {res}')
    return res
    