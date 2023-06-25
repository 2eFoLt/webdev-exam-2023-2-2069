import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import Cover
from app import db, app


def drop_by_name(filename):
    print(filename)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))


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
