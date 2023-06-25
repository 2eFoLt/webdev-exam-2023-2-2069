import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import Cover
from app import db, app
from bleach import clean


def drop_by_name(filename):
    print(filename)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))


def log(item):
    print(f'\n\n\n{item}\n\n\n')


def to_type(iterable, t_type):
    if t_type == 'int':
        return [int(item) for item in iterable]
    elif t_type == 'str':
        return [str(item) for item in iterable]
    else:
        return iterable


def whiteclear(iterable_object):
    if type(iterable_object) == dict:
        for key in iterable_object.keys():
            print(key, iterable_object[key])
            iterable_object[key] = clean(iterable_object[key])
    return iterable_object


class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        image = self.__find_by_md5_hash()
        if image is not None:
            return image
        filename = secure_filename(self.file.filename)
        mime_type = self.file.mimetype
        img_obj = Cover(
            file_name=filename,
            mime_type=mime_type,
            md5_hash=self.md5_hash,
            id=str(uuid.uuid4())
        )
        db.session.add(img_obj)
        db.session.commit()
        self.file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_obj.storage_filename))
        return img_obj

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Cover.query.filter(Cover.md5_hash == self.md5_hash).first()
