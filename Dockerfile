# Tool: Copilot Fusion
#
# Prompt summary: create a Dockerfile for a FastAPI app using Python with a virtual env 
#
# AI Contribution: 100%
#
# Human Modifications: I did not have to change anything

FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /functional-codebase/build
COPY functional-codebase/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /opt/venv /opt/venv
WORKDIR /functional-codebase/app
COPY functional-codebase/app ./app

WORKDIR /functional-codebase
COPY functional-codebase/app ./app
RUN groupadd --system app \
    && useradd --system --gid app --home-dir /home/app app \
    && chown -R app:app /functional-codebase

USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
