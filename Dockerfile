# Use Python slim image
FROM python:3.11-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`wget -qO- chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY bot.py .

# Run the bot
CMD ["python", "bot.py"]