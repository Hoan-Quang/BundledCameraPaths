import os
import cv2
import numpy as np

def calculate_padding(frame):
    """
    Calculate padding to crop the frame such that the number of black pixels in the respective row/column equals outpadding * 2.
    """
    outpadding = 200
    # threshold <<<, cropping >>> && threshold >>>, cropping <<<
    threshold = 50
    height, width = frame.shape[:2]
    padding_top, padding_bottom, padding_left, padding_right = 0, 0, 0, 0

    # Calculate padding top
    for i in range(height):
        black_pixel_count = np.sum(np.all(frame[i, :] == [0, 0, 0], axis=1))
        if black_pixel_count <= outpadding * 2 + threshold:
            padding_top = i
            break

    # Calculate padding bottom
    for i in range(height-1, -1, -1):
        black_pixel_count = np.sum(np.all(frame[i, :] == [0, 0, 0], axis=1))
        if black_pixel_count <= outpadding * 2 + threshold:
            padding_bottom = height - i - 1
            break

    # Calculate padding left
    for j in range(width):
        black_pixel_count = np.sum(np.all(frame[:, j] == [0, 0, 0], axis=1))
        if black_pixel_count <= outpadding * 2 + threshold:
            padding_left = j
            break

    # Calculate padding right
    for j in range(width-1, -1, -1):
        black_pixel_count = np.sum(np.all(frame[:, j] == [0, 0, 0], axis=1))
        if black_pixel_count <= outpadding * 2 + threshold:
            padding_right = width - j - 1
            break

    return padding_top, padding_bottom, padding_left, padding_right

def calculate_padding1(frame):
    """
    Calculate padding to remove black pixels from the edges of the frame.
    """
    height, width = frame.shape[:2]
    padding_top, padding_bottom, padding_left, padding_right = 0, 0, 0, 0

    # Check top
    for i in range(height):
        if np.any(frame[i, :] != 0):
            padding_top = i
            break

    # Check bottom
    for i in range(height-1, -1, -1):
        if np.any(frame[i, :] != 0):
            padding_bottom = height - i - 1
            break

    # Check left
    for j in range(width):
        if np.any(frame[:, j] != 0):
            padding_left = j
            break

    # Check right
    for j in range(width-1, -1, -1):
        if np.any(frame[:, j] != 0):
            padding_right = width - j - 1
            break

    return padding_top, padding_bottom, padding_left, padding_right

def calculate_max_padding(input_dir):
    """
    Calculate the maximum padding for all frames in the directory to remove black pixels from the edges.
    """
    max_padding_top, max_padding_bottom, max_padding_left, max_padding_right = 0, 0, 0, 0

    # Get list of all .bmp files in the directory
    bmp_files = [f for f in os.listdir(input_dir) if f.endswith('.bmp')]
    bmp_files.sort(key=lambda f: int(os.path.splitext(f)[0]))  # Sort files numerically

    for file in bmp_files:
        frame = cv2.imread(os.path.join(input_dir, file))
        if frame is not None:
            height, width = frame.shape[:2]
            padding_top, padding_bottom, padding_left, padding_right = calculate_padding(frame)
            max_padding_top = max(max_padding_top, padding_top)
            max_padding_bottom = max(max_padding_bottom, padding_bottom)
            max_padding_left = max(max_padding_left, padding_left)
            max_padding_right = max(max_padding_right, padding_right)

    return max_padding_top, max_padding_bottom, max_padding_left, max_padding_right


def create_video_from_bmp(input_dir, output_file, fps, max_padding):
    """
    Creates a video from BMP files in the input directory, crops each frame, and displays each frame.
    """
    # Get list of all .bmp files in the directory
    bmp_files = [f for f in os.listdir(input_dir) if f.endswith('.bmp')]
    bmp_files.sort(key=lambda f: int(os.path.splitext(f)[0]))  # Sort files numerically

    if not bmp_files:
        print("No .bmp files found in the directory.")
        return

    # Read the first image to get dimensions
    first_frame = cv2.imread(os.path.join(input_dir, bmp_files[0]))
    height, width, layers = first_frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps,
                                   (width - max_padding[2] - max_padding[3], height - max_padding[0] - max_padding[1]))

    for idx, file in enumerate(bmp_files):
        frame = cv2.imread(os.path.join(input_dir, file))
        # Crop the frame
        frame_crop = frame[max_padding[0]:height - max_padding[1], max_padding[2]:width - max_padding[3]]
        video_writer.write(frame_crop)
        # cv2.imshow('Frame', frame_crop)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break
        print(f"Processing Frame {idx + 1}/{len(bmp_files)}: {file}")

    video_writer.release()
    cv2.destroyAllWindows()
    print(f"Video saved to {output_file}")


def main():
    class_name = "Zooming"
    class_path = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\Bundled\\results\\{class_name}"
    # List all directories in class_path
    directories = [d for d in os.listdir(class_path) if os.path.isdir(os.path.join(class_path, d))]
    for dir_name in directories:
        video_name = dir_name
        input_dir = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\Bundled\\results\\{class_name}\\{video_name}"
        output_file = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\Bundled\\{class_name}\\{video_name}.avi"

        sharky_dir = f"D:\\Dai_hoc\\Nam5_Ky1\\STP\\VidStab\\dataset\\{class_name}\\unstable\\{video_name}.avi"

        capture = cv2.VideoCapture(sharky_dir)
        fps = capture.get(cv2.CAP_PROP_FPS)
        print(fps)

        # Calculate maximum padding for all frames
        max_padding = calculate_max_padding(input_dir)
        print(
            f"Calculated max padding: Top={max_padding[0]}, Bottom={max_padding[1]}, Left={max_padding[2]}, Right={max_padding[3]}")

        create_video_from_bmp(input_dir, output_file, fps, max_padding)

        print(f'End {video_name}!\n')
    print(f'End {class_name}!\n')

if __name__ == "__main__":
    main()
