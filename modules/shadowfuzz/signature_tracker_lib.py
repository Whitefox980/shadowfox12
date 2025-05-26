import requests
import re

def test_reflection(url, payload):
    try:
        r = requests.get(url, timeout=10)
        reflected = payload in r.text

        # Exploit proveru: traži <script>, onerror, eval, alert, ili payload u <tag attr=...>
        potential_exec = (
            bool(re.search(r"<script.*?>.*?</script>", r.text, re.IGNORECASE)) or
            bool(re.search(r"on\w+=['\"].*?alert|eval|console|prompt", r.text, re.IGNORECASE)) or
            bool(payload in r.text and "<" in payload and ">" in payload) or
            bool(re.search(r"srcdoc=.*?<script>", r.text, re.IGNORECASE))
        )

        return {
            "url": url,
            "payload": payload,
            "reflected": reflected,
            "potential_exploit": potential_exec,
            "status_code": r.status_code,
            "response_size": len(r.content),
            "timestamp": r.elapsed.total_seconds(),
            "response": r.text[:3000]
        }
    except Exception as e:
        return {
            "url": url,
            "payload": payload,
            "reflected": False,
            "potential_exploit": False,
            "error": str(e),
            "response": ""
        }
