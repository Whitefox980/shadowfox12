import os

DELETE_EXTENSIONS = [".log", ".tmp", ".db-journal", ".pyc"]
DELETE_FILENAMES = ["__pycache__", ".DS_Store"]
DELETE_PATTERNS = ["proof_0", "fuzz_results_0", "invalid_", "error_", "test_", "empty_"]

def is_trash(filename):
    for ext in DELETE_EXTENSIONS:
        if filename.endswith(ext):
            return True
    for pattern in DELETE_PATTERNS:
        if pattern in filename:
            return True
    for name in DELETE_FILENAMES:
        if filename == name:
            return True
    return False

def deep_clean(path="."):
    removed = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            full = os.path.join(root, file)
            if is_trash(file):
                try:
                    os.remove(full)
                    print(f"[✘] Uklonjeno: {full}")
                    removed += 1
                except Exception as e:
                    print(f"[!] Ne mogu da obrišem: {full} → {e}")
    print(f"\n[✓] Čišćenje završeno. Uklonjeno ukupno: {removed} fajlova.")

if __name__ == "__main__":
    print("=== ShadowFox DEEP CLEAN ===")
    deep_clean()
