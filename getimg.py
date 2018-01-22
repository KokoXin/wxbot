# -*- coding: utf-8 -*-

import os
import requests

base_dir = os.path.dirname(os.path.abspath(__file__))

with open('tmp/images', 'r') as f:
    for line in f:
        _img_url = line.strip()
        print(_img_url)
        img_content = requests.get(_img_url)
        img_name = _img_url.split('/')[-1].strip()

        with open(base_dir + '/' + 'logos' + '/' + img_name, 'wb') as f:
            f.write(img_content.content)
