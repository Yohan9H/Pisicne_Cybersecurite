from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import logging

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
    except Exception as e:
        logging.error(f"Pillow could not read {image_path}: {e}")
        return None

IFD_NAME_MAP = {
    "Image": "0th",
    "Exif": "Exif",
    "GPS": "GPS",
    "Interop": "Interop",
    "1st": "1st",
}

def find_tag_info(tag_name):
    for ifd_group, tags in piexif.TAGS.items():
        for tag_code, tag_details in tags.items():
            if tag_details['name'] == tag_name:
                ifd_name = IFD_NAME_MAP.get(ifd_group)
                if ifd_name:
                    return ifd_name, tag_code
    return None, None

def set_image_tag(filepath, tag_name, value):
    ifd_name, tag_code = find_tag_info(tag_name)

    if not ifd_name:
        print(f"Error: Tag '{tag_name}' is not a known or supported EXIF tag.")
        return False

    try:
        exif_dict = piexif.load(filepath)
        try:
            final_value = int(value)
        except ValueError:
            final_value = str(value).encode("utf-8")

        ifd_dict = exif_dict.setdefault(ifd_name, {})
        ifd_dict[tag_code] = final_value

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, filepath)
        return True
    except Exception as e:
        logging.error(f"Error writing tag '{tag_name}' to {filepath}: {e}")
        return False

def remove_image_tag(filepath, tag_name):
    ifd_name, tag_code = find_tag_info(tag_name)

    if not ifd_name:
        print(f"Error: Tag '{tag_name}' is not a known EXIF tag.")
        return False

    try:
        exif_dict = piexif.load(filepath)
        if ifd_name in exif_dict and tag_code in exif_dict[ifd_name]:
            del exif_dict[ifd_name][tag_code]
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, filepath)
        else:
            print(f"Info: Tag '{tag_name}' not found in the file, nothing to remove.")
        return True
    except Exception as e:
        logging.error(f"Error removing tag '{tag_name}' from {filepath}: {e}")
        return False

def remove_all_metadata(filepath):
    try:
        piexif.remove(filepath)
        return True
    except Exception as e:
        logging.error(f"Error removing all EXIF data from {filepath}: {e}")
        return False
