from flask import Flask, jsonify, abort, send_file, send_from_directory, request
from ise_lib import utils
import cv2
import json

app = Flask(__name__, static_folder='html')

images = [
    {
        'id': 1,
        'name': u'2015-04-029_20X_C57Bl6_E16.5_LMM.14.24.4.46_SOX9_SFTPC_ACTA2_001'
    },
    {
        'id': 2,
        'name': u'2015-04-029_20X_C57Bl6_E16.5_LMM.14.24.4.46_SOX9_SFTPC_ACTA2_002'
    },
    {
        'id': 3,
        'name': u'2015-04-029_20X_C57Bl6_E16.5_LMM.14.24.4.46_SOX9_SFTPC_ACTA2_003'
    },
    {
        'id': 4,
        'name': u'2015-04-029_20X_C57Bl6_E16.5_LMM.14.24.4.46_SOX9_SFTPC_ACTA2_004'
    }
]


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/ng-app/<path:path>')
def send_ng(path):
    return send_from_directory('ng-app', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/api/images/', methods=['GET'])
def get_image_list():
    return jsonify(images)


@app.route('/api/images/<int:img_id>', methods=['GET'])
def get_image(img_id):
    img_format = request.args.get('type')

    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    else:
        img = img[0]

    if img_format == 'tif':
        img_file = '.'.join([img['name'], 'tif'])
        img_path = '/'.join(['data', 'orig-imgs', img_file])
        mime_type = 'image/tiff'
    elif img_format == 'jpg':
        img_file = '.'.join([img['name'], 'jpg'])
        img_path = '/'.join(['data', 'jpeg-imgs', img_file])
        mime_type = 'image/jpeg'
    else:
        abort(404)

    return send_file(img_path, mimetype=mime_type)


@app.route('/api/images/<int:img_id>/train/region', methods=['POST'])
def post_training_sub_region(img_id):
    points = json.loads(request.data)

    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    else:
        img = img[0]

    img_file = '.'.join([img['name'], 'tif'])
    img_path = '/'.join(['data', 'orig-imgs', img_file])

    cv_img = cv2.imread(img_path)

    success = utils.extract_regions(cv_img, img_file, points['points'])

    return jsonify({'response': success})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
