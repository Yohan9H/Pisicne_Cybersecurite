import argparse
from metadata_handler import get_image_metadata

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
        description="A program to extract metadata from image files."
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="One or more image files to process."
    )

    args = parser.parse_args()

    for filepath in args.files:
        metadata = get_image_metadata(filepath)
        print_metadata(filepath, metadata)


if __name__ == "__main__":
    main()
