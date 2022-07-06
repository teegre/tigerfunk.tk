FROM python:alpine3.16

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]

# RUN apk update && \
#     addgroup -S tigerfunk && \
#     adduser -S tigerfunk -G tigerfunk && \
#     mkdir -p /home/tigerfunk/tigerfunk.tk
# 
# WORKDIR /home/tigerfunk/tigerfunk.tk
# 
# COPY . .
# 
# RUN chown -R tigerfunk:tigerfunk .
# 
# RUN pip install --upgrade pip && \
#     pip install -r requirements.txt
# 
# USER tigerfunk
# WORKDIR /home/tigerfunk/tigerfunk.tk
# 
# ENTRYPOINT ["./entrypoint.sh"]
