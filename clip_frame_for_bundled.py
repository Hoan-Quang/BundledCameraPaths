import os
import cv2


def process_file(file_path, output_dir):
    capture = cv2.VideoCapture(file_path)
    fps = capture.get(cv2.CAP_PROP_FPS)
    print(fps)
    num_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if num_frames > 1000:
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    num_digits = len(str(num_frames))
    index = 1

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame is None or cv2.countNonZero(gray) == 0:
            continue

        file_name = f"{index:0{num_digits}d}.png"
        output_path = os.path.join(output_dir, file_name)

        print(f"Processing frame {index}/{num_frames}")
        cv2.imwrite(output_path, frame)
        index += 1

    capture.release()


def process_video_files(video_dir, output_base_dir):
    os.makedirs(output_base_dir, exist_ok=True)

    # List all .avi files in the directory
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.avi')]

    for video_file in video_files:
        file_path = os.path.join(video_dir, video_file)
        output_dir = os.path.join(output_base_dir, os.path.splitext(video_file)[0])
        process_file(file_path, output_dir)


def main():
    class_name = "Zooming"
    video_dir = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\{class_name}\\unstable"
    output_base_dir = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\Bundled\\images\\{class_name}"
    process_video_files(video_dir, output_base_dir)


if __name__ == "__main__":
    main()
