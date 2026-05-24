#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""โหมดออฟไลน์: จำลอง MongoDB collection ด้วยไฟล์ JSON"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

LAB_ROOT = Path(__file__).resolve().parents[1]
STORE = LAB_ROOT / "output" / "mongo_collections"


class JsonCollection:
    def __init__(self, name: str) -> None:
        self.path = STORE / f"{name}.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict[str, Any]]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, docs: list[dict[str, Any]]) -> None:
        self.path.write_text(
            json.dumps(docs, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def insert_one(self, doc: dict[str, Any]) -> str:
        docs = self._load()
        if "_id" not in doc:
            doc["_id"] = f"local_{len(docs) + 1}"
        docs.append(doc)
        self._save(docs)
        return str(doc["_id"])

    def find(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        docs = self._load()
        if not query:
            return docs
        return [d for d in docs if all(d.get(k) == v for k, v in query.items())]

    def update_one(self, query: dict[str, Any], update: dict[str, Any]) -> int:
        docs = self._load()
        count = 0
        for d in docs:
            if all(d.get(k) == v for k, v in query.items()):
                d.update(update)
                count += 1
                break
        self._save(docs)
        return count

    def delete_one(self, query: dict[str, Any]) -> int:
        docs = self._load()
        before = len(docs)
        docs = [d for d in docs if not all(d.get(k) == v for k, v in query.items())]
        self._save(docs)
        return before - len(docs)
