# Extend the offical Rasa Core SDK image
FROM rasa/rasa_core_sdk:latest

# Add a custom python library (pony orm)
RUN pip install --no-cache-dir \
    pony && \
    mkdir /actions

COPY . .

CMD ["start", "--actions", "actions"]