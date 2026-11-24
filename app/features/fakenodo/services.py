"""Fakenodo — a lightweight fake Zenodo API for development.

Stores depositions in memory.  Implements the versioning rule the issue
requires:

* **Metadata-only edit** on a published deposition ⟶ the DOI stays the same.
* **File change** (upload / replace) + publish ⟶ a *new version* is created
  with a **new DOI** that shares the same *concept DOI*.
"""

import copy
import threading

from splent_framework.services.BaseService import BaseService

from app.features.fakenodo.repositories import FakenodoRepository


class FakenodoService(BaseService):
    """In-memory Zenodo stand-in.

    Thread-safety is handled by a simple lock — good enough for a
    single-process development server.
    """

    _lock = threading.Lock()
    _depositions: dict[int, dict] = {}
    _files: dict[int, list[dict]] = {}  # deposition_id → list of file dicts
    _next_id: int = 1
    _next_doi: int = 1

    def __init__(self):
        super().__init__(FakenodoRepository())

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @classmethod
    def _generate_id(cls) -> int:
        dep_id = cls._next_id
        cls._next_id += 1
        return dep_id

    @classmethod
    def _generate_doi(cls) -> str:
        doi = f"10.5072/fakenodo.{cls._next_doi}"
        cls._next_doi += 1
        return doi

    @classmethod
    def _concept_doi_for(cls, deposition: dict) -> str:
        return deposition.get("conceptdoi", deposition.get("doi", ""))

    # ------------------------------------------------------------------
    # Public API (called by the routes)
    # ------------------------------------------------------------------

    @classmethod
    def create_deposition(cls, metadata: dict | None = None) -> dict:
        with cls._lock:
            dep_id = cls._generate_id()
            concept_doi = f"10.5072/fakenodo.concept.{dep_id}"
            deposition = {
                "id": dep_id,
                "conceptrecid": str(dep_id),
                "metadata": metadata or {},
                "state": "unsubmitted",
                "submitted": False,
                "doi": None,
                "conceptdoi": concept_doi,
                "links": {},
            }
            cls._depositions[dep_id] = deposition
            cls._files[dep_id] = []
            return copy.deepcopy(deposition)

    @classmethod
    def get_deposition(cls, dep_id: int) -> dict | None:
        with cls._lock:
            dep = cls._depositions.get(dep_id)
            return copy.deepcopy(dep) if dep else None

    @classmethod
    def list_depositions(cls) -> list[dict]:
        with cls._lock:
            return [copy.deepcopy(d) for d in cls._depositions.values()]

    @classmethod
    def delete_deposition(cls, dep_id: int) -> bool:
        with cls._lock:
            if dep_id not in cls._depositions:
                return False
            del cls._depositions[dep_id]
            cls._files.pop(dep_id, None)
            return True

    @classmethod
    def upload_file(cls, dep_id: int, filename: str, content: bytes) -> dict | None:
        with cls._lock:
            if dep_id not in cls._depositions:
                return None
            file_entry = {
                "id": f"file-{dep_id}-{len(cls._files[dep_id]) + 1}",
                "filename": filename,
                "filesize": len(content),
                "checksum": f"md5:fake{dep_id}{len(cls._files[dep_id])}",
            }
            cls._files[dep_id].append(file_entry)
            # Mark that files were touched since last publish (for versioning).
            cls._depositions[dep_id]["_files_changed"] = True
            return copy.deepcopy(file_entry)

    @classmethod
    def publish_deposition(cls, dep_id: int) -> dict | None:
        with cls._lock:
            dep = cls._depositions.get(dep_id)
            if dep is None:
                return None

            if dep["state"] == "done" and not dep.get("_files_changed"):
                # Re-publish after a metadata-only edit → keep the same DOI.
                return copy.deepcopy(dep)

            # First publish **or** files changed → assign a (new) DOI.
            dep["doi"] = cls._generate_doi()
            dep["state"] = "done"
            dep["submitted"] = True
            dep.pop("_files_changed", None)
            return copy.deepcopy(dep)

    @classmethod
    def update_metadata(cls, dep_id: int, metadata: dict) -> dict | None:
        with cls._lock:
            dep = cls._depositions.get(dep_id)
            if dep is None:
                return None
            dep["metadata"] = metadata
            # Metadata-only: do NOT set ``_files_changed``.
            return copy.deepcopy(dep)

    @classmethod
    def new_version(cls, dep_id: int) -> dict | None:
        """Create a new draft version linked to the same concept DOI.

        The new draft starts with no files (Zenodo's real behaviour requires
        uploading fresh files to the new version).
        """
        with cls._lock:
            original = cls._depositions.get(dep_id)
            if original is None:
                return None

            new_id = cls._generate_id()
            draft = {
                "id": new_id,
                "conceptrecid": str(original.get("conceptrecid", original["id"])),
                "metadata": copy.deepcopy(original["metadata"]),
                "state": "unsubmitted",
                "submitted": False,
                "doi": None,
                "conceptdoi": original["conceptdoi"],
                "links": {},
                "_files_changed": True,
            }
            cls._depositions[new_id] = draft
            cls._files[new_id] = []
            return copy.deepcopy(draft)

    @classmethod
    def clear_all(cls) -> None:
        """Reset the in-memory store — useful in tests."""
        with cls._lock:
            cls._depositions.clear()
            cls._files.clear()
            cls._next_id = 1
            cls._next_doi = 1
