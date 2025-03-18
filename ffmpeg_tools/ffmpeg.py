import subprocess
import os
import ffmpeg


def split_video(input_file, segment_time=300, output_dir="output"):
    """
    使用 FFmpeg 将视频按指定时长分段
    :param input_file: 输入视频文件路径
    :param segment_time: 每段时长（秒），默认 300 秒（5 分钟）
    :param output_dir: 输出目录，默认为 "output"
    :return: None
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 构建 FFmpeg 命令
    output_template = os.path.join(output_dir, f"{os.path.basename(input_file).split('.')[0]}_%03d.mp4")
    command = [
        "ffmpeg",
        "-i", input_file,  # 输入文件
        "-f", "segment",  # 使用分段模式
        "-segment_time", str(segment_time),  # 每段时长
        "-reset_timestamps", "1",  # 重置时间戳
        "-c", "copy",  # 直接复制流，避免重新编码
        output_template  # 输出文件名模板
    ]

    try:
        subprocess.run(command, check=True)
        # 获取所有分片视频文件
        video_files = [f for f in os.listdir(output_dir) if f.endswith(".mp4")]
        video_files.sort()  # 按文件名排序

        # 获取每个分片视频的时长
        durations = {}
        for video_file in video_files:
            video_path = os.path.join(output_dir, video_file)
            durations[video_file] = int(get_video_duration(video_path))

        # 返回输出目录和时长信息
        return output_dir, durations
    except subprocess.CalledProcessError as e:
        raise Exception(f"视频分割失败：{e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到 FFmpeg，请确保已安装 FFmpeg 并添加到系统环境变量中。")


def get_video_duration(file_path):
    """
    使用 ffmpeg-python 获取视频的时长
    :param file_path: 视频文件路径
    :return: 视频时长（秒）
    """
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe["format"]["duration"])
        return duration
    except Exception as e:
        raise Exception(f"获取视频时长失败：{e}")
