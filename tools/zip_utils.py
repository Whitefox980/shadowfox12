import os
import zipfile
from datetime import datetime

def create_zip(source_folder="reports/replay_ai", output_folder="reports"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{output_folder}/shadowfox_report_{timestamp}.zip"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, source_folder)
                zipf.write(filepath, arcname)
    
    print(f"[✓] ZIP fajl sačuvan: {zip_filename}")
    return zip_filename
