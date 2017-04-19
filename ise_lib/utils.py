import os
import re
import numpy as np
import cv2

image_dir = 'some_dir'
region_class = 'test'


def extract_regions(image, image_name, points):

    output_dir = "/".join(
        [
            image_dir,
            region_class
        ]
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for point_list in points:

        if len(point_list) < 3:
            continue

        real_point_list = []
        for p in point_list:
            real_point_list.append([p[2], p[3]])

        contour = np.array(real_point_list, dtype='int')
        b_rect = cv2.boundingRect(contour)

        poly_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(poly_mask, [contour], 0, 255, cv2.FILLED)

        x1 = b_rect[0]
        x2 = b_rect[0] + b_rect[2]
        y1 = b_rect[1]
        y2 = b_rect[1] + b_rect[3]

        region = image[y1:y2, x1:x2]
        poly_mask = poly_mask[y1:y2, x1:x2]

        match = re.search('(.+)\.(.+)$', image_name)
        output_filename = "".join(
            [
                match.groups()[0],
                '_',
                str(x1),
                ',',
                str(y1)
            ]
        )
        mask_filename = "_".join(
            [
                output_filename,
                'mask'
            ]
        )
        output_filename = ".".join([output_filename, match.groups()[1]])
        mask_filename = ".".join([mask_filename, match.groups()[1]])

        output_file_path = "/".join([output_dir, output_filename])
        mask_file_path = "/".join([output_dir, mask_filename])

        cv2.imwrite(output_file_path, region)
        cv2.imwrite(mask_file_path, poly_mask)
