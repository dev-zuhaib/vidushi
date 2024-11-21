import cv2
import requests
import time
import numpy as np
from picamera2 import Picamera2


# Video capture from default camera
#cap = cv2.VideoCapture(0)

#if not cap.isOpened():
#    print("could not open camera")

def find_max_frequency_value(lst):
    # Create a dictionary to store the frequency of each element
    frequency = {}

    # Count the frequency of each element in the list
    for item in lst:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1

    # Find the value with the maximum frequency
    max_frequency_value = max(frequency, key=frequency.get)
    
    return max_frequency_value


def Identify():
	picam = Picamera2()
	picam.start()
	l = []
	for i in range(0,5):
		# Capture a single frame
		frame = picam.capture_array()
		#ret, frame = cap.read()
		ret = True
		if ret:
			# Resize the raw image into (224-height,224-width) pixels
			frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
			frame = cv2.flip(frame, 1) 
			# frame = np.asarray(frame, dtype=np.float32).reshape(1, 224, 224, 3)

			# Normalize the image array
			# frame = (frame / 127.5) - 1

			# Encode the frame as JPEG
			_, encoded_image = cv2.imencode('.jpg', frame)

			# Convert the encoded image to bytes
			image_data = encoded_image.tobytes()

			# Send the image data to the server
			url = 'http://192.168.29.89:3300/upload'  # Replace with your server endpoint
			files = {'image': ('captured_image.jpg', image_data, 'image/jpeg')}
			response = requests.post(url, files=files)

			if response.status_code == 200:
				print(f"Image sent successfully.{response.text}")
				l.append(eval(response.text)[0]['class'])
			else:
				print(f"Failed to send image. Status code: {response.status_code}")

			#time.sleep(1)
	result = find_max_frequency_value(l)
	return result

# Release the capture and close OpenCV windows
#Identify()
