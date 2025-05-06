FROM python:3.9

# Installa wkhtmltopdf e dipendenze
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Configura xvfb-wrapper per wkhtmltopdf (ambiente headless)
RUN echo '#!/bin/bash\nxvfb-run -a --server-args="-screen 0 1024x768x24" /usr/bin/wkhtmltopdf "$@"' > /usr/local/bin/wkhtmltopdf.sh \
    && chmod +x /usr/local/bin/wkhtmltopdf.sh \
    && ln -s /usr/local/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file di progetto
COPY . /app/

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta
EXPOSE $PORT

# Comando di avvio
CMD gunicorn --bind 0.0.0.0:$PORT --config gunicorn_config.py main:app