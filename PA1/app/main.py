# Tool: Copilot Fusion
#
# Prompt summary: create a barebone FastAPI app
#
# AI Contribution: 
#
# Human Modifications: No changes needed
#

from fastapi import FastAPI

app = FastAPI(
    title="Domain 3: Peer Review and Evaluation Gateway",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
