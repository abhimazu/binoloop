FROM nvcr.io/nvidia/tritonserver:23.06-py3

RUN pip install torch==1.10.0 transformers==4.12.0

RUN mkdir /models

COPY ./phi-2 /models/phi-2
COPY ./gemma /models/gemma

CMD ["tritonserver", "--model-repository=/models"]
