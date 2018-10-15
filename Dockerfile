FROM python:3.7

# copy all files
RUN mkdir hello
COPY . /hello
WORKDIR /hello

RUN python --version
RUN python3 --version

# install required libraries
RUN pip install Flask
RUN pip install Flask_Script

ENTRYPOINT ["python"]
CMD ["/hello/run.py"]