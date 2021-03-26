FROM python:3.7.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
#    curl -fsSL https://deb.nodesource.com/setup_15.x | bash -; \
#    apt-get install -y nodejs; \
#    npm install -g @ionic/cli;
COPY . /code/