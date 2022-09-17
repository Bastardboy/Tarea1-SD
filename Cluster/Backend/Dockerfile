FROM python:3.8.10

WORKDIR /Backend

COPY requirements.txt /Backend

RUN pip3 install -r requirements.txt

COPY . .

#CMD tail -f /dev/null
RUN python3 -m grpc_tools.protoc -I config --python_out=. --grpc_python_out=. config/proto_message.proto

EXPOSE 3000

CMD ["python3", "-u", "back.py"]