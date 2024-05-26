import cv2
import numpy as np

# Open the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# File to save the HSV values
output_file = "hsv_values.txt"

# Flag to control writing to file
write_to_file = False

while True:
    # Read a frame from the camera
    _, frame = cap.read()
    
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Get the HSV values at the center pixel
    cx = int(width / 2)
    cy = int(height / 2)
    pixel_center = hsv_frame[cy, cx]
    
    # Convert HSV values from OpenCV scale to standard scale
    pixel_center[0] = pixel_center[0] * 2  # Hue
    pixel_center[1] = pixel_center[1] / 2.55  # Saturation
    pixel_center[2] = pixel_center[2] / 2.55  # Value

    # Get the RGB values at the center pixel
    pixel_center_rgb = frame[cy, cx]

    # Convert RGB to hex
    hex_color = "#{:02x}{:02x}{:02x}".format(pixel_center_rgb[2], pixel_center_rgb[1], pixel_center_rgb[0])

    # Display the frame with a circle at the center pixel
    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)
    cv2.imshow("Frame", frame)

    # Wait for key press
    key = cv2.waitKey(1)

    # Press 'ESC' to exit
    if key == 27:
        break

    # Press 'SPACE' to write HSV values to file
    elif key == 32:
        write_to_file = True

    # Write HSV values to file if the flag is set
    if write_to_file:
        with open(output_file, 'w') as file:
            # Write the HSV values with the required column names
            file.write("Name,Hex (24 bit),Red (8 bit),Green (8 bit),Blue (8 bit),Hue (degrees),HSL.S (%),HSL.L (%) HSV.S (%) HSV.V (%)\n")
            hsv_values = [
                "CenterPixel",    # Name
                hex_color,        # Hex (24 bit)
                pixel_center_rgb[2],  # Red (8 bit)
                pixel_center_rgb[1],  # Green (8 bit)
                pixel_center_rgb[0],  # Blue (8 bit)
                pixel_center[0],  # Hue (degrees)
                pixel_center[1],  # HSL.S (%)
                pixel_center[2]   # HSL.L (%) HSV.S (%) HSV.V (%)
            ]
            hsv_values_str = ','.join(map(str, hsv_values))
            file.write(hsv_values_str + '\n')
        write_to_file = False  # Reset the flag after writing to file

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()