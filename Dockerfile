FROM fedora:latest

# before that, you need to use your proxy on docker by using -e argument setting env variable 
# 根据你的代理端口调整
# ENV HTTP_PROXY=http://
# ENV HTTPS_PROXY=https://
# ENV NO_PROXY=localhost,127.0.0.1

WORKDIR /start

RUN dnf update -y
RUN dnf install vim python3 git python3 python3-pip conda npm nodejs cargo rustup rustc sqlite3 -y


# 在（base）下安装依赖

RUN conda activate;pip install fastapi  uvicorn sqlalchemy pandas


# 假设你在Competition1下（即仓库）开发，那么可以移动到/start（docker 下的工作目录下）
COPY . .

# 进入仓库文件夹后需要创建第二个python环境, 3.10(mofa). 3.11(web)
RUN conda create -n mofa-env python=3.10
RUN conda install python3-setuptools python3.10-devel

 # 安装mofa
RUN git clone https://github.com/moxin-org/mofa.git;cd mofa/python
RUN pip3 install -r requirements.txt 
RUN pip install -e .
RUN python -c "import mofa"

 # 安装dora-rs
RUN pip install dora-rs
RUN cargo install dora-rs
