# encoding:utf-8
# !/usr/bin/env python
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import time
import os
import pymysql
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def upload_test():
    return render_template('index.html')

def insert_database(insert_image,length,id):
    # 连接数据库
    connect = pymysql.Connect(
        host='47.114.53.192',
        port=3306,
        user='xmc',
        passwd='294207',
        db='deeppupil',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    if length == 1:
        path = "C:/Users/Administrator/Desktop/Flask_Get_Image/upload/"
        sql = "insert into person_comments_image_temp(comments_id, image_path,status) VALUES ('%s','%s','%s');"
        data = (id, path + insert_image[0], '0')
        cursor.execute(sql % data)
        connect.commit()
    elif length == 2:
        path = "C:/Users/Administrator/Desktop/Flask_Get_Image/upload/"
        sql = "insert into person_comments_image_temp(comments_id, image_path,status) VALUES ('%s','%s','%s');"
        data = (id, path + insert_image[0], '0')
        cursor.execute(sql % data)
        connect.commit()

        sql = "insert into person_comments_image_temp(comments_id, image_path,status) VALUES ('%s','%s','%s');"
        data = (id, path + insert_image[1], '0')
        cursor.execute(sql % data)
        connect.commit()

    elif length == 3:
        path = "C:/Users/Administrator/Desktop/Flask_Get_Image/upload/"
        sql = "insert into person_comments_image_temp(comments_id, image_path,status) VALUES ('%s','%s','%s');"
        data = (id, path + insert_image[0], '0')
        cursor.execute(sql % data)
        connect.commit()

        sql = "insert into person_comments_image_temp(comments_id, image_path,status) VALUES ('%s','%s','%s');"
        data = (id, path + insert_image[1], '0')
        cursor.execute(sql % data)
        connect.commit()

        sql = "insert into person_comments_image_temp(comments_id, image_path,status) VALUES ('%s','%s','%s');"
        data = (id, path + insert_image[2], '0')
        cursor.execute(sql % data)
        connect.commit()


    cursor.close()
    connect.close()

# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    id = request.form.get('comments_id')
    num = request.form.get('image_num')
    print(id+" "+num)
    if num == "1":
        f = request.files['file1']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            ext = fname.rsplit('.', 1)[1]
            # 利用时间序列保证图片名称唯一性
            new_filename = time.strftime("%Y%m%d%H%M%S0", time.localtime()) + '.' + ext
            f.save(os.path.join(file_dir, new_filename))
            # 上传记录存储服务器
            insert_image = [new_filename]
            insert_database(insert_image,1,id)
            return jsonify({"success": 0, "msg": "上传成功"})
        else:
            return jsonify({"error": 1001, "msg": "上传失败"})
    elif num == "2":
        f = request.files['file1']
        f2 = request.files['file2']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            ext = fname.rsplit('.', 1)[1]
            # 利用时间序列保证图片名称唯一性
            new_filename = time.strftime("%Y%m%d%H%M%S0", time.localtime()) + '.' + ext
            f.save(os.path.join(file_dir, new_filename))
            new_filename2 = time.strftime("%Y%m%d%H%M%S1", time.localtime()) + '.' + ext
            f2.save(os.path.join(file_dir, new_filename2))
            # 上传记录存储服务器
            insert_image = [new_filename,new_filename2]
            insert_database(insert_image,2,id)
            return jsonify({"success": 0, "msg": "上传成功"})
        else:
            return jsonify({"error": 1001, "msg": "上传失败"})
    elif num == "3":
        f = request.files['file1']
        f2 = request.files['file2']
        f3 = request.files['file3']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            ext = fname.rsplit('.', 1)[1]
            # 利用时间序列保证图片名称唯一性
            new_filename = time.strftime("%Y%m%d%H%M%S0", time.localtime()) + '.' + ext
            f.save(os.path.join(file_dir, new_filename))
            new_filename2 = time.strftime("%Y%m%d%H%M%S1", time.localtime()) + '.' + ext
            f2.save(os.path.join(file_dir, new_filename2))
            new_filename3 = time.strftime("%Y%m%d%H%M%S2", time.localtime()) + '.' + ext
            f3.save(os.path.join(file_dir, new_filename3))

            # 上传记录存储服务器
            insert_image = [new_filename, new_filename2, new_filename2]
            insert_database(insert_image,3,id)

            return jsonify({"success": 0, "msg": "上传成功"})
        else:
            return jsonify({"error": 1001, "msg": "上传失败"})


@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True)
        pass


# show photo
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True)