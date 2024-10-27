import os
import cv2

def create_video_from_bmp(input_dir, output_file, fps):
    """
    Creates a video from BMP files in the input directory and displays each frame.
    """
    # Get list of all .bmp files in the directory
    bmp_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    bmp_files.sort(key=lambda f: int(os.path.splitext(f)[0]))  # Sort files numerically

    if not bmp_files:
        print("No .bmp files found in the directory.")
        return

    # Read the first image to get dimensions
    first_frame = cv2.imread(os.path.join(input_dir, bmp_files[0]))
    height, width, layers = first_frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for idx, file in enumerate(bmp_files):
        frame = cv2.imread(os.path.join(input_dir, file))
        video_writer.write(frame)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break
        print(f"Processing Frame {idx + 1}/{len(bmp_files)}: {file}")

    video_writer.release()
    cv2.destroyAllWindows()
    print(f"Video saved to {output_file}")

def main():
    class_name = "Parallax"
    video_name = "3"
    input_dir = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\Bundled\\images\\{class_name}\\{video_name}"
    output_file = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\{class_name}\\unstable\\{video_name}_noSound.avi"

    sharky_dir = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\{class_name}\\unstable\\{video_name}.avi"

    capture = cv2.VideoCapture(sharky_dir)
    fps = capture.get(cv2.CAP_PROP_FPS)
    print(fps)

    create_video_from_bmp(input_dir, output_file, fps)

if __name__ == "__main__":
    main()
