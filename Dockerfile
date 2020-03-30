FROM ubuntu:18.04

WORKDIR /covid-19

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT 8501

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        ca-certificates \
        curl \
        python3 \
        python3-distutils \
    && rm -rf /var/lib/apt/lists/*

RUN curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py

COPY ./ ./

RUN pip3 install --requirement requirements.txt

RUN streamlit version
EXPOSE 8501/tcp
CMD ["streamlit", "run", "simulator/hospital_queue/hospital_queue.py", "--bind 0.0.0.0:$PORT"]
