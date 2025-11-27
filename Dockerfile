FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

# copy all files
RUN mkdir hello
COPY . /hello
WORKDIR /hello

# install required libraries
RUN pip install Flask
RUN pip install Flask_Script
RUN python -m pip install --upgrade pip

EXPOSE 5000

ENV TZ Asia/Shanghai

CMD ["python3", "run.py"]
