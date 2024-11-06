FROM python:3.12

WORKDIR /app
RUN pip install Flask scikit-learn SQLAlchemy tensorflow-cpu matplotlib pandas flask_sqlalchemy

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0



EXPOSE 5000
CMD ["python", "app.py"]