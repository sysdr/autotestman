# UQAP Lesson 76 — Dockerized Selenium Test Environment
# Bookworm: stable Debian package names (default slim may track trixie and break apt pins).
FROM python:3.11-slim-bookworm

LABEL maintainer="uqap-course" \
      lesson="76" \
      description="Python 3.11 + Chrome + pytest"

# System deps for headless Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg unzip curl ca-certificates \
    fonts-liberation libxss1 libnss3 \
    libgdk-pixbuf2.0-0 libgtk-3-0 \
    libxcomposite1 libxdamage1 libxrandr2 \
    libasound2 libatk-bridge2.0-0 libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome (signed-by keyring; apt-key is deprecated)
RUN wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /usr/share/keyrings/google-linux.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Chromedriver: Selenium 4.6+ Selenium Manager resolves a matching driver for installed Chrome.

WORKDIR /app

# Layer order: requirements first (cached), code second (volatile)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure report dir exists at runtime
RUN mkdir -p /app/reports

CMD ["pytest", "tests/", "-v", \
     "--html=reports/report.html", \
     "--self-contained-html", \
     "--tb=short"]
