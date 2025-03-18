from setuptools import setup, find_packages

setup(
    name="wwlei-common-utils",  # 包的名称
    version="0.1.0",  # 版本号
    author="Lei Wang",
    author_email="greatbestlei@gmail.com",
    description="common utils",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_package",  # GitHub 仓库地址
    packages=find_packages(),  # 自动发现包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Python 版本要求
    install_requires=[
        # 列出依赖项，例如：
        # "requests>=2.25.1",
    ],
)
