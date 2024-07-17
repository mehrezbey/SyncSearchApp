FROM python:3.10
EXPOSE 5000
RUN mkdir /home/app
WORKDIR /home/app
COPY requirements.txt /home/app/
RUN pip install  -r requirements.txt
COPY . /home/app/
CMD ["python", "run.py"]
