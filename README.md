# wwlei-common-utils

这是一个通用Python工具库，提供了多个实用的工具包，用于处理日常开发中的常见任务。

## 安装

```bash
pip install git+https://github.com/wang14597/wwlei-common-utils.git
```

## 工具包说明

### 1. csv_tools
用于处理CSV文件的工具包。

#### 函数说明
- `write_to_csv(json_data: list, output_path: str) -> None`
  - 功能：将JSON数据写入CSV文件，支持UTF-8编码
  - 参数：
    - json_data: 包含字典的列表，每个字典代表一行数据
    - output_path: 输出CSV文件的路径
  
示例代码：
```python
from csv_tools.csv_tool import write_to_csv

# 准备数据
data = [
    {"name": "张三", "age": 25, "city": "北京"},
    {"name": "李四", "age": 30, "city": "上海"}
]

# 写入CSV文件
write_to_csv(data, "output.csv")
```

### 2. datetime_tools
日期时间处理工具包。

#### 函数说明
- `convert_time_to_seconds(time_str: str) -> int`
  - 功能：将时间字符串转换为秒数
  - 参数：
    - time_str: 格式为"MM:SS"的时间字符串
  - 返回：总秒数

- `seconds_to_time_str(seconds: int) -> str`
  - 功能：将秒数转换为时间字符串格式
  - 参数：
    - seconds: 秒数
  - 返回：格式为"MM:SS"的时间字符串

- `get_uid() -> str`
  - 功能：基于当前时间生成唯一标识符
  - 返回：格式为"MMDDHHMM"的字符串

示例代码：
```python
from datetime_tools.datetime_tools import convert_time_to_seconds, seconds_to_time_str, get_uid

# 时间转换示例
seconds = convert_time_to_seconds("05:30")  # 返回 330
time_str = seconds_to_time_str(330)  # 返回 "05:30"

# 生成唯一标识符
uid = get_uid()  # 返回类似 "03151425" (3月15日14点25分)
```

### 3. ffmpeg_tools
视频处理工具包，基于FFmpeg。

#### 函数说明
- `split_video(input_file: str, segment_time: int = 300, output_dir: str = "output") -> tuple`
  - 功能：将视频按指定时长分段
  - 参数：
    - input_file: 输入视频文件路径
    - segment_time: 每段时长（秒），默认300秒
    - output_dir: 输出目录，默认"output"
  - 返回：(输出目录路径, 各分段视频时长字典)

- `get_video_duration(file_path: str) -> float`
  - 功能：获取视频文件的时长
  - 参数：
    - file_path: 视频文件路径
  - 返回：视频时长（秒）

示例代码：
```python
from ffmpeg_tools.ffmpeg import split_video, get_video_duration

# 获取视频时长
duration = get_video_duration("input.mp4")  # 返回视频时长（秒）

# 分割视频
output_dir, durations = split_video(
    input_file="input.mp4",
    segment_time=300,  # 5分钟一段
    output_dir="split_videos"
)
print(f"视频分段保存在: {output_dir}")
print(f"各分段时长: {durations}")
```

### 4. gcp_tools
Google Cloud Platform (GCP) 相关工具包。

#### 类和方法说明

##### GCS类
```python
from gcp_tools.gcs import GCS

class GCS:
    def __init__(self, service_account: str | dict = None):
        """
        初始化GCS客户端
        :param service_account: 服务账号凭据文件路径或凭据字典
        """

    def upload_stream(self, bucket_name: str, destination_blob_name: str, iter) -> None:
        """流式上传数据到GCS"""

    def upload(self, bucket_name: str, destination_blob_name: str, file_obj) -> None:
        """上传文件对象到GCS"""

    def upload_from_filename(self, bucket_name: str, destination_blob_name: str, local_file_path: str) -> None:
        """上传本地文件到GCS"""

    def generate_signed_url(self, bucket_name: str, blob_name: str, expiration: int = 30, content_type: str = None) -> str:
        """生成签名URL"""

    def file_exists(self, bucket_name: str, destination_blob_name: str) -> bool:
        """检查文件是否存在"""

    def upload_folder(self, bucket_name: str, folder_path: str, file_prefix: str) -> list:
        """上传整个文件夹到GCS"""

    def download_file(self, bucket_name: str, source_blob_name: str, destination_file_name: str) -> str:
        """从GCS下载文件"""

    def list_files(self, bucket_name: str) -> list:
        """列出存储桶中的所有文件"""
```

示例代码：
```python
from gcp_tools.gcs import GCS

# 初始化GCS客户端
gcs = GCS("path/to/service-account.json")

# 上传文件
gcs.upload_from_filename(
    bucket_name="my-bucket",
    destination_blob_name="folder/file.txt",
    local_file_path="local/file.txt"
)

# 生成签名URL
signed_url = gcs.generate_signed_url(
    bucket_name="my-bucket",
    blob_name="folder/file.txt",
    expiration=60  # 60分钟有效期
)

# 上传文件夹
uploaded_files = gcs.upload_folder(
    bucket_name="my-bucket",
    folder_path="local/folder",
    file_prefix="remote/folder"
)
```

##### Veo2类
用于视频生成的工具类。

```python
from gcp_tools.veo2 import Veo2

class Veo2:
    class AspectRatio(Enum):
        RATIO_16_9 = "16:9"
        RATIO_9_16 = "9:16"
        RATIO_1_1 = "1:1"
        # ... 其他比例

    def generate_video_from_text(self, prompt: str, aspect_ratio: AspectRatio = AspectRatio.RATIO_16_9, ...) -> list:
        """从文本生成视频"""

    def generate_video_from_image(self, prompt: str = None, image_path: str = None, ...) -> list:
        """从图片生成视频"""
```

##### Credentials工具
```python
from gcp_tools.credentials import get_credentials

def get_credentials(service_account: str | dict, scopes=None) -> Credentials:
    """获取GCP认证凭据"""
```

##### VertexAIGemini类
用于与Google Vertex AI Gemini模型交互的工具类。

```python
from gcp_tools.vertex_ai import VertexAIGemini

class VertexAIGemini:
    def __init__(self,
                 project: str,
                 location: str,
                 model_name: str,
                 service_account: str | dict = None,
                 response_schema=None):
        """
        初始化VertexAI Gemini客户端
        :param project: GCP项目ID
        :param location: 地理位置
        :param model_name: 模型名称
        :param service_account: 服务账号凭据
        :param response_schema: 响应模式
        """

    def generate_content(self,
                        prompt: str,
                        images_path: List = None,
                        video_path: str = None
                        ) -> dict[str, str]:
        """
        生成内容
        :param prompt: 提示文本
        :param images_path: 图片路径列表
        :param video_path: 视频路径
        :return: JSON格式的响应内容
        """
```

示例代码：
```python
from gcp_tools.vertex_ai import VertexAIGemini

# 初始化Gemini客户端
gemini = VertexAIGemini(
    project="your-project-id",
    location="us-central1",
    model_name="gemini-pro",
    service_account="path/to/service-account.json"
)

# 生成内容
response = gemini.generate_content(
    prompt="描述这张图片",
    images_path=["image1.jpg", "image2.jpg"]
)
print(response)

# 处理视频内容
video_response = gemini.generate_content(
    prompt="分析这个视频",
    video_path="video.mp4"
)
print(video_response)
```

### 5. https_tools
HTTP和媒体类型处理工具。

#### 函数说明
- `get_mime_type(images_path: str) -> str`
  - 功能：根据文件扩展名获取MIME类型
  - 参数：
    - images_path: 文件路径
  - 返回：MIME类型字符串
  - 支持类型：jpg/jpeg, png

示例代码：
```python
from https_tools.media_tools import get_mime_type

mime_type = get_mime_type("image.jpg")  # 返回 "image/jpeg"
mime_type = get_mime_type("image.png")  # 返回 "image/png"
```

#### 函数说明

##### HTTP下载工具
```python
from https_tools.http_download import download_file, download_file_stream, iter_content_func

def download_file(url: str) -> bytes | None:
    """
    下载文件并返回文件内容
    :param url: 文件URL
    :return: 文件内容的字节数据
    """

def download_file_stream(url: str) -> requests.Response | None:
    """
    以流式方式下载文件
    :param url: 文件URL
    :return: requests.Response对象
    """

def iter_content_func(response: requests.Response, chunk_size: int = 1024 * 1024 * 10):
    """
    迭代获取下载内容
    :param response: Response对象
    :param chunk_size: 每块大小（默认10MB）
    :yield: 文件内容块
    """
```

示例代码：
```python
from https_tools.http_download import download_file, download_file_stream, iter_content_func

# 直接下载文件
content = download_file("https://example.com/file.pdf")
with open("file.pdf", "wb") as f:
    f.write(content)

# 流式下载大文件
response = download_file_stream("https://example.com/large-file.zip")
for chunk in iter_content_func(response):
    # 处理每个数据块
    process_chunk(chunk)
```

### 6. log_tools
日志处理工具包。

#### 函数说明
- `get_logger(name: str, to_file: bool = False) -> logging.Logger`
  - 功能：创建自定义logger
  - 参数：
    - name: logger名称
    - to_file: 是否输出到文件
  - 特性：
    - 支持控制台和文件输出
    - 文件输出支持自动轮转（2MB大小，保留5个备份）
    - 自定义日志格式：时间 - 日志级别 - 名称 - 消息
    - 默认INFO级别

示例代码：
```python
from log_tools.log import get_logger

# 创建只输出到控制台的logger
console_logger = get_logger("my-app")
console_logger.info("这是一条信息")
console_logger.error("这是一条错误")

# 创建同时输出到文件的logger
file_logger = get_logger("my-app-with-file", to_file=True)
file_logger.info("这条信息会同时输出到控制台和文件")
# 日志文件将保存在 logs/my-app-with-file/my-app-with-file.log
```

## 依赖要求

- Python >= 3.9
- 主要依赖包：
  - ffmpeg-python==0.2.0
  - google-cloud-storage==2.19.0
  - google-cloud-aiplatform==1.71.1
  - google-genai==1.5.0
  - 其他依赖详见 requirements.txt

## 许可证

MIT License

## 作者

Lei Wang (greatbestlei@gmail.com) 