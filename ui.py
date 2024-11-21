import cv2
from pydub import AudioSegment
import simpleaudio as sa

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    audio = AudioSegment.from_file(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video.")
        return

    # Get screen resolution
    screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a full screen window
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.resizeWindow('Video', 1350, 738)

    # Play audio
    audio_player = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width,
                                   sample_rate=audio.frame_rate)
    
    # Read and discard the first frame
    ret, _ = cap.read()
    if not ret:
        print("Error: Unable to read the first frame.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        cv2.imshow('Video', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    audio_player.stop()


if __name__ == "__main__":
    video_path = '/home/vidushi/Desktop/.Vidushi/vidushi-backdrop.mp4'
    play_video(video_path)

