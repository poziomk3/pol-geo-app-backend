import sys

from PowiatModel import scrape_images_to_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_voivo_imgs.py <output_file>")
        sys.exit(1)
    scrape_images_to_file(sys.argv[1])
