FROM google/cloud-sdk:slim


COPY entrypoint.sh entrypoint.sh
COPY gunicorn.config gunicorn.config
COPY requirements.txt requirements.txt
COPY bumblebee_backend bumblebee_backend
COPY api api
COPY manage.py manage.py
RUN chmod u+x entrypoint.sh

RUN apt-get update && \
    apt-get --no-install-recommends -y install vim gettext && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

RUN python manage.py collectstatic

EXPOSE 5432

ENTRYPOINT ["./entrypoint.sh"]
