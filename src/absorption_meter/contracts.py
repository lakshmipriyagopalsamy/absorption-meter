"""Contract drift: breaking changes to an API or event schema without a version bump.

Supports OpenAPI 3.x, Swagger 2.0 and JSON Schema files. The checks are a
deliberately small, conservative subset of what dedicated tools (oasdiff, buf,
graphql-inspector) do; use those in CI for full coverage. The point here is to
*count* drift over history, so a repository's trend can be read.

What counts as breaking:

* removed path, operation, or success response;
* new required request parameter or request property;
* removed response property, or a response property that is no longer required;
* a changed type;
* an enum value removed from a request.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml

from .gitlog import Change, show_file

HTTP_METHODS = ("get", "put", "post", "delete", "patch", "head", "options", "trace")

_NAME_HINT = re.compile(r"(openapi|swagger|asyncapi)[^/]*\.(ya?ml|json)$|\.schema\.json$", re.IGNORECASE)
_MAX_DEPTH = 8


@dataclass
class Breaking:
    kind: str
    location: str

    def __str__(self) -> str:
        return f"{self.kind} at {self.location}"


@dataclass
class DriftEvent:
    sha: str
    timestamp: int
    path: str
    old_version: Optional[str]
    new_version: Optional[str]
    breaking: List[Breaking] = field(default_factory=list)

    @property
    def kind(self) -> str:
        """``drift``: breaking with no version change. ``minor-bump``: breaking
        with a version change that keeps the same major version."""
        if self.old_version == self.new_version:
            return "drift"
        return "minor-bump" if _same_major(self.old_version, self.new_version) else "signalled"

    @property
    def is_drift(self) -> bool:
        return self.kind in ("drift", "minor-bump")


def _same_major(old: Optional[str], new: Optional[str]) -> bool:
    def major(v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        m = re.match(r"v?(\d+)", str(v).strip())
        return m.group(1) if m else None

    mo, mn = major(old), major(new)
    return mo is not None and mo == mn


def parse_document(text: Optional[str], path: str) -> Optional[Dict[str, Any]]:
    if text is None:
        return None
    try:
        doc = json.loads(text) if path.lower().endswith(".json") else yaml.safe_load(text)
    except (ValueError, yaml.YAMLError):
        return None
    return doc if isinstance(doc, dict) else None


def contract_type(doc: Optional[Dict[str, Any]]) -> Optional[str]:
    if not doc:
        return None
    if "openapi" in doc or "swagger" in doc:
        return "openapi"
    if "$schema" in doc or ("properties" in doc and doc.get("type") == "object"):
        return "jsonschema"
    return None


def is_candidate_path(path: str) -> bool:
    return bool(_NAME_HINT.search(path))


def document_version(doc: Optional[Dict[str, Any]]) -> Optional[str]:
    if not doc:
        return None
    info = doc.get("info")
    if isinstance(info, dict) and info.get("version") is not None:
        return str(info["version"])
    for key in ("version", "$id"):
        if doc.get(key) is not None:
            return str(doc[key])
    return None


# --------------------------------------------------------------------------- schema diff


def _resolve(schema: Any, root: Dict[str, Any], seen: Optional[set] = None) -> Any:
    seen = seen or set()
    while isinstance(schema, dict) and isinstance(schema.get("$ref"), str):
        ref = schema["$ref"]
        if not ref.startswith("#/") or ref in seen:
            return {}
        seen.add(ref)
        node: Any = root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            node = node.get(part) if isinstance(node, dict) else None
            if node is None:
                return {}
        schema = node
    return schema if isinstance(schema, dict) else {}


def compare_schema(
    old: Any,
    new: Any,
    old_root: Dict[str, Any],
    new_root: Dict[str, Any],
    direction: str,
    location: str,
    out: List[Breaking],
    depth: int = 0,
) -> None:
    """Append breaking differences between two schemas.

    ``direction`` is ``request`` (the client writes it) or ``response`` (the client
    reads it). The same edit can be safe in one direction and breaking in the other.
    """
    if depth > _MAX_DEPTH:
        return
    o = _resolve(old, old_root)
    n = _resolve(new, new_root)
    if not o or not n:
        return

    ot, nt = o.get("type"), n.get("type")
    if ot is not None and nt is not None and ot != nt:
        out.append(Breaking("type-changed", location))
        return

    o_props = o.get("properties") or {}
    n_props = n.get("properties") or {}
    o_req = set(o.get("required") or [])
    n_req = set(n.get("required") or [])

    if direction == "response":
        for name in sorted(set(o_props) - set(n_props)):
            out.append(Breaking("removed-property", f"{location}.{name}"))
        for name in sorted((o_req - n_req) & set(n_props)):
            out.append(Breaking("property-no-longer-required", f"{location}.{name}"))
    else:
        for name in sorted(n_req - o_req):
            out.append(Breaking("newly-required-property", f"{location}.{name}"))
        o_enum, n_enum = o.get("enum"), n.get("enum")
        if isinstance(o_enum, list) and isinstance(n_enum, list):
            for value in o_enum:
                if value not in n_enum:
                    out.append(Breaking("enum-value-removed", f"{location}={value!r}"))

    for name in sorted(set(o_props) & set(n_props)):
        compare_schema(o_props[name], n_props[name], old_root, new_root, direction, f"{location}.{name}", out, depth + 1)

    if "items" in o and "items" in n:
        compare_schema(o["items"], n["items"], old_root, new_root, direction, f"{location}[]", out, depth + 1)


def _request_schema(op: Dict[str, Any]) -> Any:
    body = op.get("requestBody")
    if isinstance(body, dict):
        for media in (body.get("content") or {}).values():
            if isinstance(media, dict) and "schema" in media:
                return media["schema"]
    for param in op.get("parameters") or []:
        if isinstance(param, dict) and param.get("in") == "body":
            return param.get("schema")
    return None


def _response_schema(resp: Any) -> Any:
    if not isinstance(resp, dict):
        return None
    if "schema" in resp:
        return resp["schema"]
    for media in (resp.get("content") or {}).values():
        if isinstance(media, dict) and "schema" in media:
            return media["schema"]
    return None


def _params(op: Dict[str, Any], path_item: Dict[str, Any], root: Dict[str, Any]) -> Dict[tuple, Dict[str, Any]]:
    result = {}
    for raw in list(path_item.get("parameters") or []) + list(op.get("parameters") or []):
        param = _resolve(raw, root)
        if param.get("in") == "body" or "name" not in param:
            continue
        result[(param.get("name"), param.get("in"))] = param
    return result


def diff_openapi(old: Dict[str, Any], new: Dict[str, Any]) -> List[Breaking]:
    out: List[Breaking] = []
    old_paths = old.get("paths") or {}
    new_paths = new.get("paths") or {}
    for path in sorted(old_paths):
        if path not in new_paths:
            out.append(Breaking("removed-path", path))
            continue
        o_item, n_item = old_paths[path] or {}, new_paths[path] or {}
        for method in HTTP_METHODS:
            if method not in o_item:
                continue
            loc = f"{method.upper()} {path}"
            if method not in n_item:
                out.append(Breaking("removed-operation", loc))
                continue
            o_op, n_op = o_item[method] or {}, n_item[method] or {}

            o_params = _params(o_op, o_item, old)
            n_params = _params(n_op, n_item, new)
            for key, param in sorted(n_params.items(), key=lambda kv: str(kv[0])):
                was = o_params.get(key)
                if param.get("required") and not (was and was.get("required")):
                    out.append(Breaking("newly-required-parameter", f"{loc} {key[1]}:{key[0]}"))

            o_body, n_body = _request_schema(o_op), _request_schema(n_op)
            if o_body is not None and n_body is not None:
                compare_schema(o_body, n_body, old, new, "request", f"{loc} request", out)

            o_resp = o_op.get("responses") or {}
            n_resp = n_op.get("responses") or {}
            for code in sorted(o_resp, key=str):
                if not str(code).startswith("2"):
                    continue
                if code not in n_resp:
                    out.append(Breaking("removed-response", f"{loc} {code}"))
                    continue
                o_s = _response_schema(_resolve(o_resp[code], old) or o_resp[code])
                n_s = _response_schema(_resolve(n_resp[code], new) or n_resp[code])
                if o_s is not None and n_s is not None:
                    compare_schema(o_s, n_s, old, new, "response", f"{loc} {code}", out)
    return out


def diff_documents(old: Dict[str, Any], new: Dict[str, Any]) -> List[Breaking]:
    kind = contract_type(old)
    if kind == "openapi":
        return diff_openapi(old, new)
    if kind == "jsonschema":
        out: List[Breaking] = []
        # An event or message schema is read by consumers: treat it as a response.
        compare_schema(old, new, old, new, "response", "$", out)
        return out
    return []


# --------------------------------------------------------------------------- history scan


def scan_drift(repo: str, changes: List[Change]) -> List[DriftEvent]:
    """Check every change that touches a contract file; return breaking events."""
    events: List[DriftEvent] = []
    for change in changes:
        if not change.parents:
            continue
        parent = change.parents[0]
        for path in change.paths:
            if not is_candidate_path(path):
                continue
            old = parse_document(show_file(repo, parent, path), path)
            if contract_type(old) is None:
                continue
            new = parse_document(show_file(repo, change.sha, path), path)
            if new is None:
                # Deleted or moved. History is read without rename detection, so a
                # move looks like a deletion: don't count it as drift.
                continue
            breaking = diff_documents(old, new)
            if breaking:
                events.append(
                    DriftEvent(change.sha, change.timestamp, path, document_version(old), document_version(new), breaking)
                )
    return events
