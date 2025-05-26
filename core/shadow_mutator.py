def mutate_payload(payload):
    # Osnovne mutacije, možeš proširiti
    return [
        payload,
        payload.replace("<", "&lt;").replace(">", "&gt;"),
        payload.replace("alert", "al<!-- -->ert"),
        payload.replace("script", "scr<script>ipt")
    ]
