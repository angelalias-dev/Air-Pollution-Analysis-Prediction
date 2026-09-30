FROM apache/spark:3.5.9-scala2.12-java11-python3-r-ubuntu

USER root

ENV PYTHONPATH=/opt/spark/python:/opt/spark/python/lib/py4j-0.10.9.7-src.zip

RUN pip install --no-cache-dir fastapi uvicorn

WORKDIR /app

COPY app.py /app/app.py

RUN chmod -R 755 /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]