import argparse
import csv
import io
import os
import base64
import requests
import json
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")  # Optional

def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        return f"error - {str(e)}"

def process_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        resolution = f"{img.width}x{img.height}"

        
        original_buffer = io.BytesIO()
        img.save(original_buffer, format="JPEG")
        original_b64 = base64.b64encode(original_buffer.getvalue()).decode()

        
        img.thumbnail((320, 568))
        resized_buffer = io.BytesIO()
        img.save(resized_buffer, format="JPEG")
        resized_b64 = base64.b64encode(resized_buffer.getvalue()).decode()

        size = len(image_bytes)
        return {
            "status": "success",
            "original_image64": original_b64,
            "resized_image64": resized_b64,
            "size": size,
            "resolution": resolution
        }
    except Exception as e:
        return {"status": f"error - unable to process image: {str(e)}"}

def upload_to_imgur(image_b64):
    if not IMGUR_CLIENT_ID:
        return None
    try:
        headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
        data = {"image": image_b64, "type": "base64"}
        response = requests.post("https://api.imgur.com/3/image", headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["data"]["link"]
    except Exception as e:
        return None
    return None

def handle_url(url):
    result = {"image_url": url}
    image_data = download_image(url)

    if isinstance(image_data, str):  # error message
        result["status"] = image_data
    else:
        img_result = process_image(image_data)
        result.update(img_result)
        if img_result.get("status") == "success":
            imgur_link = upload_to_imgur(img_result["resized_image64"])
            if imgur_link:
                result["imgur_link"] = imgur_link
    return result

def read_csv(csv_path):
    urls = []
    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            urls.append(row[0])
    return urls

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Image URL or path to CSV file")
    args = parser.parse_args()

    input_path = args.input
    results = []

    if input_path.endswith(".csv"):
        urls = read_csv(input_path)
        for url in urls:
            print(f"Processing {url}")
            results.append(handle_url(url))
    else:
        results.append(handle_url(input_path))

    with open("output.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Processing complete. Output saved to output.json")

if __name__ == "__main__":
    main()
