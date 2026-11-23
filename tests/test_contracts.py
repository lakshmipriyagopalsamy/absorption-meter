import copy

import yaml
from conftest import day

from absorption_meter.contracts import diff_openapi, diff_documents, scan_drift
from absorption_meter.gitlog import read_changes

SPEC = {
    "openapi": "3.0.3",
    "info": {"title": "Orders", "version": "1.0.0"},
    "paths": {
        "/orders/{id}": {
            "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "get": {
                "responses": {"200": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/Order"}}}}},
            },
            "put": {
                "requestBody": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/OrderInput"}}}},
                "responses": {"204": {"description": "ok"}},
            },
        },
        "/health": {"get": {"responses": {"200": {"description": "ok"}}}},
    },
    "components": {
        "schemas": {
            "Order": {
                "type": "object",
                "required": ["id", "status"],
                "properties": {
                    "id": {"type": "string"},
                    "status": {"type": "string"},
                    "total": {"type": "number"},
                    "items": {"type": "array", "items": {"type": "object", "properties": {"sku": {"type": "string"}}}},
                },
            },
            "OrderInput": {
                "type": "object",
                "required": ["status"],
                "properties": {"status": {"type": "string", "enum": ["open", "closed"]}, "note": {"type": "string"}},
            },
        }
    },
}


def kinds(changes):
    return sorted(b.kind for b in changes)


def test_no_change_and_additive_change_are_safe():
    new = copy.deepcopy(SPEC)
    assert diff_openapi(SPEC, new) == []
    new["components"]["schemas"]["Order"]["properties"]["currency"] = {"type": "string"}
    new["paths"]["/new"] = {"get": {"responses": {"200": {"description": "ok"}}}}
    assert diff_openapi(SPEC, new) == []


def test_response_property_removed_through_ref():
    new = copy.deepcopy(SPEC)
    del new["components"]["schemas"]["Order"]["properties"]["total"]
    del new["components"]["schemas"]["Order"]["properties"]["items"]["items"]["properties"]["sku"]
    found = diff_openapi(SPEC, new)
    assert kinds(found) == ["removed-property", "removed-property"]
    assert any("items[].sku" in b.location for b in found)


def test_request_side_breaks():
    new = copy.deepcopy(SPEC)
    new["components"]["schemas"]["OrderInput"]["required"].append("note")
    new["components"]["schemas"]["OrderInput"]["properties"]["status"]["enum"] = ["open"]
    new["paths"]["/orders/{id}"]["put"]["parameters"] = [{"name": "X-Tenant", "in": "header", "required": True}]
    assert kinds(diff_openapi(SPEC, new)) == ["enum-value-removed", "newly-required-parameter", "newly-required-property"]


def test_removed_path_operation_type_and_required():
    new = copy.deepcopy(SPEC)
    del new["paths"]["/health"]
    del new["paths"]["/orders/{id}"]["put"]
    new["components"]["schemas"]["Order"]["properties"]["id"]["type"] = "integer"
    new["components"]["schemas"]["Order"]["required"] = ["id"]
    assert kinds(diff_openapi(SPEC, new)) == [
        "property-no-longer-required", "removed-operation", "removed-path", "type-changed"]


def test_json_schema_event():
    old = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
           "properties": {"orderId": {"type": "string"}, "amount": {"type": "number"}}}
    new = copy.deepcopy(old)
    new["properties"]["amount"]["type"] = "string"
    assert kinds(diff_documents(old, new)) == ["type-changed"]


def test_scan_drift_over_history(repo):
    spec = copy.deepcopy(SPEC)
    repo.commit({"api/openapi.yaml": yaml.safe_dump(spec)}, "add spec", day(2025, 1, 1))

    del spec["components"]["schemas"]["Order"]["properties"]["total"]
    drift_sha = repo.commit({"api/openapi.yaml": yaml.safe_dump(spec)}, "drop total", day(2025, 1, 5))

    del spec["paths"]["/health"]
    spec["info"]["version"] = "1.1.0"
    minor_sha = repo.commit({"api/openapi.yaml": yaml.safe_dump(spec)}, "drop health", day(2025, 1, 9))

    del spec["components"]["schemas"]["Order"]["properties"]["items"]
    spec["info"]["version"] = "2.0.0"
    repo.commit({"api/openapi.yaml": yaml.safe_dump(spec)}, "v2", day(2025, 1, 12))

    spec["components"]["schemas"]["Order"]["properties"]["currency"] = {"type": "string"}
    repo.commit({"api/openapi.yaml": yaml.safe_dump(spec)}, "add currency", day(2025, 1, 15))

    events = scan_drift(repo.path, read_changes(repo.path))
    assert [(e.sha, e.kind) for e in events] == [
        (drift_sha, "drift"), (minor_sha, "minor-bump"), (events[2].sha, "signalled")]
    assert [e.is_drift for e in events] == [True, True, False]
