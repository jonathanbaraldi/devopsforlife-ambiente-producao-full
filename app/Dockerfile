# FROM python:3.8-slim
FROM python:3.8-slim


# Create a non-root user
RUN useradd --create-home devopsforlife
WORKDIR /home/devopsforlife

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and change the ownership to the non-root user
COPY . .
RUN chown -R devopsforlife:devopsforlife .

# Switch to the non-root user
USER devopsforlife

CMD ["python", "app.py"]
