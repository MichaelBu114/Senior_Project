FROM python
WORKDIR /code
ENV FLASK_APP=app.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]