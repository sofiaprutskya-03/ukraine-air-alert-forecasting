import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import urlretrieve

from src.config import RAW_DATA_URL


def _file_size(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def _write_source_metadata(
    metadata_path: Path,
    raw_path: Path,
    source_type: str,
    downloaded: bool,
) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "source_url": RAW_DATA_URL,
        "source_type": source_type,
        "downloaded": downloaded,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_csv_path": str(raw_path),
        "file_size_bytes": _file_size(raw_path),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def get_raw_csv(local_path: Path | None, destination: Path, metadata_path: Path) -> Path:
    """Return a raw CSV path, downloading it when no local file is supplied."""
    if local_path is not None:
        if not local_path.exists():
            raise FileNotFoundError(f"Local raw CSV not found: {local_path}")
        _write_source_metadata(
            metadata_path=metadata_path,
            raw_path=local_path,
            source_type="local_path",
            downloaded=False,
        )
        return local_path

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        print(f"Using existing raw CSV: {destination}")
        _write_source_metadata(
            metadata_path=metadata_path,
            raw_path=destination,
            source_type="existing_download",
            downloaded=False,
        )
        return destination

    print(f"Downloading raw data from {RAW_DATA_URL}")
    print("If this fails, download the CSV manually and rerun with --raw-path.")
    urlretrieve(RAW_DATA_URL, destination)
    _write_source_metadata(
        metadata_path=metadata_path,
        raw_path=destination,
        source_type="github_raw_url",
        downloaded=True,
    )
    return destination
