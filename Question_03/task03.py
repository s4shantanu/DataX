import requests, csv, os, base64, json
from PIL import Image
from io import BytesIO
import sys

def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)), len(response.content)
    except Exception as e:
        return None, f"error - {str(e)}"

def resize_image(img, size=(320, 568)):
    img_copy = img.copy()
    img_copy.thumbnail(size)
    return img_copy

def encode_image_to_base64(image):
    try:
        buffered = BytesIO()
        image = image.convert("RGB") if image.mode in ("RGBA", "P") else image
        image.save(buffered, format='PNG')  
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        return None

def process_image(url):
    img, result = download_image(url)
    if img is None:
        return {"image_url": url, "status": result}

    try:
        width, height = img.size
        size_bytes = result
        resized_img = resize_image(img)
        return {
            "image_url": url,
            "status": "success",
            "original_image64": encode_image_to_base64(img),
            "resized_image64": encode_image_to_base64(resized_img),
            "size": size_bytes,
            "resolution": f"{width}x{height}"
        }
    except Exception as e:
        return {"image_url": url, "status": f"error - {str(e)}"}

def main(input_arg):
    output = []
    if input_arg.lower().endswith(".csv"):
        with open(input_arg, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                url = row[0]
                output.append(process_image(url))
    else:
        output.append(process_image(input_arg))

    with open("output.json", "w") as f:
        json.dump(output, f, indent=2)
    print("Process completed! Check output.json")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python image_processor.py <image_url_or_csv_path>")
    else:
        main(sys.argv[1])


# png link url - https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png