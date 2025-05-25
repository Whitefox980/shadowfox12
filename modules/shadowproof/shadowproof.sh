#!/bin/bash

mkdir -p proofs

echo "==== SHADOWPROOF v0.4 ===="
read -p "Unesi metu (npr. https://target.com): " URL
read -p "Unesi payload (npr. ?q=<script>alert(1)</script>): " PAYLOAD

# Auto dodaj https ako nije unet
if [[ "$URL" != http* ]]; then
  URL="https://$URL"
fi

FULL_URL="${URL}${PAYLOAD}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTFILE_TXT="proofs/proof_${TIMESTAMP}.txt"
OUTFILE_HTML="proofs/proof_${TIMESTAMP}.html"

# TXT export
echo "[+] Target: $FULL_URL" | tee $OUTFILE_TXT
echo -e "\n[+] Curl HEAD output:" | tee -a $OUTFILE_TXT
curl -s -I "$FULL_URL" | tee -a $OUTFILE_TXT
echo -e "\n[+] HTTPX output:" | tee -a $OUTFILE_TXT
httpx "$FULL_URL" | tee -a $OUTFILE_TXT
echo -e "\n[+] Korišćeni payload:" | tee -a $OUTFILE_TXT
echo "$PAYLOAD" | tee -a $OUTFILE_TXT

# HTML export
echo "<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'>" > $OUTFILE_HTML
echo "<h1>ShadowProof v0.4 by Whitefox980</h1>" >> $OUTFILE_HTML
echo "<h2>Meta: $FULL_URL</h2><pre>" >> $OUTFILE_HTML
curl -s -I "$FULL_URL" >> $OUTFILE_HTML
echo -e "\n------------------------\n" >> $OUTFILE_HTML
httpx "$FULL_URL" >> $OUTFILE_HTML
echo -e "\nPayload:\n$PAYLOAD" >> $OUTFILE_HTML
echo "</pre><br><hr><p>Operater: Čupko AI – mission complete.</p>" >> $OUTFILE_HTML
echo "</body></html>" >> $OUTFILE_HTML

# Info
echo -e "\n[✓] Dokazi sačuvani:"
echo "- $OUTFILE_TXT"
echo "- $OUTFILE_HTML"
echo "[!] Otvori HTML i slikaj ga kao dokaz!"
