import json
import httpx

async def parse_streaming_response(response: httpx.Response) -> list:
    """
    Parses a streamed OpenAI-compatible chat completion response and extracts the full message content.
    Note - data: [DONE] is a special marker used in Server-Sent Events (SSE)—the streaming format used by OpenAI-compatible chat endpoints—to indicate that the stream has finished.
    Args:
        response (httpx.Response): The streaming response object.
    Returns:
        list: List of parsed chunks with metadata.
    """
    response_chunks = []
    async for line in response.aiter_lines():
        if line.startswith("data:"):
            chunk = line.replace("data:", "").strip()
            if chunk == "[DONE]":
                break
            try:
                data = json.loads(chunk)
                response_chunks.append(data)
            except json.JSONDecodeError:
                continue
    return response_chunks

def extract_text_from_chunks(chunks: list) -> str:
    """
    Extracts and concatenates text content from streamed LLM chunks.
    Args:
        chunks (list): Parsed streamed response chunks.
    Returns:
        str: Combined message content from all chunks.
    """
    text = ""
    for chunk in chunks:
        try:
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content", "")
            text += content
        except (KeyError, IndexError):
            continue
    return text
