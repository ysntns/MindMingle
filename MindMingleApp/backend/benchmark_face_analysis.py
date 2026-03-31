
import time
import threading
import requests
import os

# This script assumes the server is running at http://localhost:8000
BASE_URL = "http://localhost:8000"
IMAGE_PATH = "logo.png" # Using an existing image for testing

def send_request():
    try:
        with open(IMAGE_PATH, 'rb') as f:
            files = {'file': ('image.png', f, 'image/png')}
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/analyze-face", files=files)
            end_time = time.time()
            if response.status_code == 200:
                print(f"Request took {end_time - start_time:.4f} seconds")
            else:
                print(f"Request failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def run_benchmark(num_requests=5):
    print(f"Starting benchmark with {num_requests} concurrent requests...")
    threads = []
    for i in range(num_requests):
        t = threading.Thread(target=send_request)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    if not os.path.exists(IMAGE_PATH):
        # Create a dummy image if logo.png doesn't exist (though it should)
        import numpy as np
        import cv2
        dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(IMAGE_PATH, dummy_img)

    run_benchmark()
