from PIL import Image
from PIL.ExifTags import TAGS
from PIL.PngImagePlugin import PngInfo
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

            if image.format == 'JPEG':
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
            elif image.format in ['PNG', 'GIF']:
                for key, value in image.info.items():
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore').strip('\x00')
                        except (UnicodeDecodeError, AttributeError):
                             pass
                    metadata[key] = value
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
    try:
        with Image.open(filepath) as img:
            image_format = img.format

        if image_format == 'JPEG':
            ifd_name, tag_code = find_tag_info(tag_name)
            if not ifd_name:
                print(f"Error: Tag '{tag_name}' is not supported EXIF tag.")
                return False

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

        elif image_format == 'PNG':
            with Image.open(filepath) as img:
                png_info = PngInfo()
                if img.info:
                    for key, val in img.info.items():
                        if key.lower() != tag_name.lower():
                            png_info.add_text(key, str(val))
                png_info.add_text(tag_name, str(value))
                img.save(filepath, pnginfo=png_info)
            return True

        elif image_format == 'GIF':
            if not tag_name == 'comment':
                logging.error(f"Error: '{tag_name}' is not supported, only comment for GIF")
                return False
            with Image.open(filepath) as img:
                img.save(filepath, comment=str(value).encode('utf-8'))
            return True

        elif image_format == "BMP":
            logging.error("Error: The BMP format does not support metadata modification.")
            return False

        else:
            logging.error(f"Error: Metadata modification for {image_format} is not supported.")
    except Exception as e:
        logging.error(f"Error writing tag '{tag_name}' to {filepath}: {e}")
        return False

def remove_image_tag(filepath, tag_name):
    try:
        with Image.open(filepath) as img:
            image_format = img.format

        if image_format == 'JPEG':
            ifd_name, tag_code = find_tag_info(tag_name)
            if not ifd_name:
                print(f"Error: Tag '{tag_name}' is not a known EXIF tag for JPEG.")
                return False

            exif_dict = piexif.load(filepath)
            if ifd_name in exif_dict and tag_code in exif_dict[ifd_name]:
                del exif_dict[ifd_name][tag_code]
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, filepath)
            else:
                print(f"Info: Tag '{tag_name}' not found in the file, nothing to remove.")
            return True

        elif image_format == 'PNG':
            with Image.open(filepath) as img:
                png_info = PngInfo()
                if img.info:
                    for key, val in img.info.items():
                        if key.lower() != tag_name.lower():
                            png_info.add_text(key, str(val))
                img.save(filepath, pnginfo=png_info)
            return True

        elif image_format == 'GIF':
            if not tag_name == 'comment':
                logging.error(f"Error: '{tag_name}' is not supported, only comment for GIF")
                return False
            with Image.open(filepath) as img:
                img.save(filepath, comment=b'')
            return True

        elif image_format == "BMP":
            logging.info("BMP format does not support metadata modification.")
            return True

        else:
            logging.error(f"Error: Metadata removal for {image_format} is not supported.")
            return False
    except Exception as e:
        logging.error(f"Error removing tag '{tag_name}' from {filepath}: {e}")
        return False

def remove_all_metadata(filepath):
    try:
        with Image.open(filepath) as img:
            image_format = img.format

        if image_format == 'JPEG':
            piexif.remove(filepath)
            return True

        elif image_format == 'PNG':
            with Image.open(filepath) as img:
                img.save(filepath)
            return True

        elif image_format == 'GIF':
            with Image.open(filepath) as img:
                img.save(filepath, comment=b'')
            return True

        elif image_format == "BMP":
            logging.info("BMP format does not support metadata.")
            return True
            
        else:
            with Image.open(filepath) as img:
                img.save(filepath)
            return True

    except Exception as e:
        logging.error(f"Error removing all metadata from {filepath}: {e}")
        return False
