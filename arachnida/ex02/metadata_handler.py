from PIL import Image
from PIL.ExifTags import TAGS


def get_image_metadata(image_path):
    try:
        with Image.open(image_path) as image:
            metadata = {}
            metadata['File'] = image.filename
            metadata['Format'] = image.format
            metadata['Size'] = image.size
            metadata['Mode'] = image.mode

            exif_data = image.getexif()
            if exif_data:
                for code, value in exif_data.items():
                    tag_name = TAGS.get(code, code)
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except (UnicodeDecodeError, AttributeError):
                            pass
                    metadata[tag_name] = value
            return metadata

    except Exception:
        return None
