import argparse
from metadata_handler import (
    get_image_metadata,
    set_image_tag,
    remove_image_tag,
    remove_all_metadata
)

def print_metadata(filepath, metadata):
    print("\n" + "-" * 40)
    print(f"Metadata for: {filepath}")
    print("-" * 40)
    if not metadata:
        print("Could not read or no metadata found.")
        return

    for key, value in metadata.items():
        if isinstance(value, str) and len(value) > 70:
            value = value[:70] + "..."
        print(f"{str(key):<20}: {str(value)}")

def main():
    parser = argparse.ArgumentParser(
        description="A program to read or modify metadata from image files.",
        epilog="Example for setting: python3 scorpion.py img.jpg --set Artist \"Yohan\""
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="One or more image files to process."
    )

    modification_group = parser.add_mutually_exclusive_group()
    modification_group.add_argument(
        "--set",
        nargs=2,
        metavar=("TAG", "VALUE"),
        help="Set a specific EXIF tag. e.g., --set Artist \"Yohan\""
    )
    modification_group.add_argument(
        "--delete",
        metavar="TAG",
        help="Delete a specific EXIF tag."
    )
    modification_group.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all EXIF data from the image."
    )

    args = parser.parse_args()

    if args.set or args.delete or args.delete_all:
        for target_file in args.files:
            success = False
            if args.set:
                tag, value = args.set
                success = set_image_tag(target_file, tag, value)
            elif args.delete:
                success = remove_image_tag(target_file, args.delete)
            elif args.delete_all:
                success = remove_all_metadata(target_file)

            if success:
                print("Operation successful. Verifying changes:")
                metadata = get_image_metadata(target_file)
                print_metadata(target_file, metadata)
            else:
                print("Operation failed.")
    else:
        for filepath in args.files:
            metadata = get_image_metadata(filepath)
            print_metadata(filepath, metadata)


if __name__ == "__main__":
    main()
