
import os
import urllib.request
from pathlib import Path

TARGET_DIR_NAME = "infection"

TEXT_FILES = {
    ".txt": "This is a simple text file for testing the Stockholm project.",
    ".html": "<!DOCTYPE html><html><head><title>Test Page</title></head><body><h1>Hello, Stockholm!</h1></body></html>",
    ".py": "# Simple Python script\nprint(\"Hello from a Python file!\")",
    ".js": "// Simple JavaScript file\nconsole.log(\"Hello from a JavaScript file!\");",
    ".css": "/* Simple CSS file */\nbody { font-family: sans-serif; }",
    ".sql": "-- Simple SQL file\nSELECT * FROM users;",
    ".rtf": "{\\rtf1\\ansi This is some RTF content.}",
    ".c": "// Simple C file\n#include <stdio.h>\nint main() { printf(\"Hello, World!\\n\"); return 0; }",
    ".cpp": "// Simple C++ file\n#include <iostream>\nint main() { std::cout << \"Hello, World!\"; return 0; }",
    ".java": "// Simple Java file\nclass HelloWorld { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }",
}

BINARY_FILES = {
    ".jpg": "https://filesamples.com/samples/image/jpg/sample_640%C3%97426.jpg",
    ".png": "https://filesamples.com/samples/image/png/sample_640%C3%97426.png",
    ".gif": "https://filesamples.com/samples/image/gif/sample_640%C3%97426.gif",
    ".pdf": "https://filesamples.com/samples/document/pdf/sample1.pdf",
    ".docx": "https://filesamples.com/samples/document/docx/sample1.docx",
    ".xlsx": "https://filesamples.com/samples/document/xlsx/sample1.xlsx",
    ".pptx": "https://filesamples.com/samples/document/pptx/sample1.pptx",
    ".zip": "https://filesamples.com/samples/archived/zip/sample1.zip",
}

ALL_EXTENSIONS = [
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".psd",
    ".zip", ".rar", ".tar", ".gz",
    ".sql", ".mdb", ".db", ".dbf", ".py", ".c", ".cpp", ".h", ".java", ".html", ".css", ".js",
    ".pdf", ".txt", ".rtf", ".key", ".pem"
]

def main():
    infection_dir = Path.home() / TARGET_DIR_NAME
    print(f"Preparing test files in: {infection_dir}\n")
    
    infection_dir.mkdir(exist_ok=True)

    created_extensions = set()

    print("--- Creating text-based files ---")
    for ext, content in TEXT_FILES.items():
        try:
            file_path = infection_dir / f"sample{ext}"
            file_path.write_text(content)
            print(f"[OK] Created {file_path.name}")
            created_extensions.add(ext)
        except Exception as e:
            print(f"[FAIL] Could not create sample{ext}. Reason: {e}")

    print("\n--- Downloading binary files ---")
    for ext, url in BINARY_FILES.items():
        try:
            file_path = infection_dir / f"sample{ext}"
            urllib.request.urlretrieve(url, file_path)
            print(f"[OK] Downloaded {file_path.name}")
            created_extensions.add(ext)
        except Exception as e:
            print(f"[FAIL] Could not download sample{ext}. Reason: {e}")

    print("\n--- Creating empty placeholder files ---")
    for ext in ALL_EXTENSIONS:
        if ext not in created_extensions:
            try:
                file_path = infection_dir / f"sample{ext}"
                file_path.touch()
                print(f"[OK] Touched {file_path.name}")
            except Exception as e:
                print(f"[FAIL] Could not touch sample{ext}. Reason: {e}")

    print("\nSetup complete!")

if __name__ == "__main__":
    main()
