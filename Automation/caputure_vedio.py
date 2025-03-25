import cv2 # type: ignore
import os

# Define the output directory and filename
def video_recording(input):
    output_dir = r"D:\Files\videos"
    output_filename = "recorded video.avi"
    output_path = os.path.join(output_dir, output_filename)

    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the camera (0 for default camera, change if multiple cameras are available)
    capture = cv2.VideoCapture(0)

    # Get the default frame width and height
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        
        # Write the frame to the output file
        out.write(frame)
        
        # Display the recording frame
        cv2.imshow('Recording', frame)
        
        # Press 'q' to exit the recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    capture.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Video saved at: {output_path}")
