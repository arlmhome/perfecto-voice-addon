ARG BUILD_FROM
FROM $BUILD_FROM
RUN apk add --no-cache python3
WORKDIR /app
COPY run.sh server.py index.html ./
RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]
