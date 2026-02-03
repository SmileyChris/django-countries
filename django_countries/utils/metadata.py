import os
import threading

import yaml

_metadata = None
_lock = threading.Lock()


def get_metadata():
    global _metadata
    if _metadata is None:
        with _lock:
            if _metadata is None:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                file_path = os.path.join(base_dir, "data", "country_metadata.yaml")
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        _metadata = yaml.safe_load(f) or {}
                else:
                    _metadata = {}
    return _metadata


def get_country_metadata(code):
    metadata = get_metadata()
    if code not in metadata:
        raise KeyError(f"Country code '{code}' not found in metadata.")
    return metadata[code]
