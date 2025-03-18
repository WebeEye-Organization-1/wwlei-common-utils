from datetime import datetime


def convert_time_to_seconds(time_str):
    """将时间字符串(如'00:48')转换为秒数"""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


def seconds_to_time_str(seconds):
    """将秒数转换为时间字符串格式(如'00:48')"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def get_uid():
    return datetime.now().strftime("%m%d%H%M")