# wwlei-common-utils

这是一个通用Python工具库，提供了多个实用的工具包，用于处理日常开发中的常见任务。

## 安装

```bash
pip install git+https://github.com/wang14597/wwlei-common-utils.git
```

## 工具包说明

### 1. csv_tools
用于处理CSV文件的工具包。

主要功能：
- `write_to_csv(json_data, output_path)`: 将JSON数据写入CSV文件，支持UTF-8编码。

### 2. datetime_tools
日期时间处理工具包。

主要功能：
- `convert_time_to_seconds(time_str)`: 将时间字符串(如'00:48')转换为秒数
- `seconds_to_time_str(seconds)`: 将秒数转换为时间字符串格式(如'00:48')
- `get_uid()`: 基于当前时间生成唯一标识符

### 3. ffmpeg_tools
视频处理工具包，基于FFmpeg。

主要功能：
- `split_video(input_file, segment_time=300, output_dir="output")`: 将视频按指定时长分段
- `get_video_duration(file_path)`: 获取视频文件的时长

### 4. gcp_tools
Google Cloud Platform (GCP) 相关工具包。

主要功能：
- GCS类：用于Google Cloud Storage操作
  - 文件上传（支持流式上传、字符串上传、本地文件上传）
  - 生成签名URL
  - 文件存在性检查
  - 文件夹上传
  - 文件下载
  - 文件列表获取
- Veo2类：用于视频生成相关操作
- Credentials工具：处理GCP认证凭据

### 5. https_tools
HTTP和媒体类型处理工具。

主要功能：
- `get_mime_type(images_path)`: 根据文件扩展名获取MIME类型

### 6. log_tools
日志处理工具包。

主要功能：
- `get_logger(name, to_file=False)`: 创建自定义logger，支持控制台和文件输出
  - 支持日志轮转
  - 支持自定义日志格式
  - 默认INFO级别日志

## 依赖要求

- Python >= 3.9
- 详细依赖列表请参见 requirements.txt

## 许可证

MIT License

## 作者

Lei Wang (greatbestlei@gmail.com) 