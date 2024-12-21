# Watermark Application

This project is a Python script that recursively processes all images in the `input` folder, adds a watermark to the bottom-center of each image, and saves the watermarked images in the `output` folder while maintaining the original directory structure.

## Requirements

- Python 3.10 or higher
- Pillow library

## Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:computerclubkec/watermarker.git
    cd watermark
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Place the images you want to process in the [input](input/) folder.
2. Place or replace your watermark image (must be PNG with transparency) in the project root directory and name it [watermark.png](watermark.png).
3. Run the script:
    ```sh
    python apply_watermark.py
    ```

The script will process all images in the [input](input/) folder and its subfolders, add the watermark to the bottom-center of each image, and save the watermarked images in the [output](output/) folder, preserving the original directory structure.

## Configuration

You can configure the watermark size and padding by modifying the following variables in the [apply_watermark.py](http://_vscodecontentref_/5) script:

- [scale_factor](apply_watermark.py): Size of the watermark relative to the main image (default: `0.18`)
- [padding](apply_watermark.py): Padding from the bottom-center in pixels (default: `300`)

## Example

```sh
python apply_watermark.py
```