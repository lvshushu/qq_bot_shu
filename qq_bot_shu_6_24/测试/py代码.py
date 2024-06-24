from PIL import Image
from PIL import ImageSequence
import os
import shutil

def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"文件 {file_path} 已被成功删除。")
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在。")
    except Exception as e:
        print(f"删除文件 {file_path} 时出错： {e}")
def gif_to_png_frames(gif_path, output_folder):
    # 确保输出文件夹存在

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    clear_directory(output_folder)
    #delete_file('111.png')
    # 读取GIF文件
    gif = Image.open(gif_path)

    # 遍历GIF的每一帧并将其保存为PNG
    frame_count = 0
    for frame in ImageSequence.Iterator(gif):
        # 将帧转换为RGBA模式
        frame = frame.convert("RGBA")
        # 保存帧为PNG
        frame.save(os.path.join(output_folder, f"frame_{frame_count:03d}.png"), "PNG")
        frame_count += 1
    # 使用示例
