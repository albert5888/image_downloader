import requests
import os
import argparse

def download_image(url, folder, cookies=None):
    try:
        headers = {}
        if cookies:
            headers['Cookie'] = cookies

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        image_name = os.path.basename(url)
        image_path = os.path.join(folder, image_name)

        with open(image_path, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded: {image_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def download_images_from_file(file_path, output_folder, cookies=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(file_path, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            download_image(url, output_folder, cookies)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from a list of URLs in a file and save them to a specified folder")
    parser.add_argument('-f', '--file', required=True, help='Path to the file containing image URLs')
    parser.add_argument('-o', '--output', required=True, help='Path to the output folder')
    parser.add_argument('--cookie', help='Cookie to include in the requests [ex: --cookie name=value; name2=value2]', default=None)

    args = parser.parse_args()

    download_images_from_file(args.file, args.output, args.cookie)
