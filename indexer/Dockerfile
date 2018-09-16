FROM google/cloud-sdk:slim


COPY batch_snippifier.py batch_snippifier.py
COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh
RUN chmod u+x entrypoint.sh

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN yes | apt-get install ffmpeg
RUN rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
