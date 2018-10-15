FROM python:3.7

# copy all files
RUN mkdir hello
COPY . /hello
WORKDIR /hello

# install required libraries
RUN pip install Flask
RUN pip install Flask_Script

RUN pip list

ENTRYPOINT ["python"]
CMD ["run.py"]
EXPOSE 5000