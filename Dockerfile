FROM amancevice/pandas

WORKDIR /app
# RUN apk add --no-cache gcc musl-dev linux-headers
# RUN apk add make automake gcc g++ subversion python3-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "./main.py"]