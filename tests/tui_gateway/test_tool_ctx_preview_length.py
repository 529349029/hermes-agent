"""`_tool_ctx` must honor `display.tool_preview_length` so the TUI can show a full
tool command instead of the compact 80-char default.

The TUI previously hardcoded `max_len=80`, bypassing the same config key the classic
CLI already uses (0 = unlimited). `_load_cfg()` intentionally does not merge defaults,
so an ABSENT key must keep the compact TUI default while an explicit value wins.
"""

from tui_gateway import server


def _ctx(monkeypatch, display, code):
    monkeypatch.setattr(server, "_display_cfg", lambda: display)
    return server._tool_ctx("execute_code", {"code": code})


def test_absent_key_keeps_the_compact_tui_default(monkeypatch):
    out = _ctx(monkeypatch, {}, "A" * 200)

    assert len(out) == 80
    assert out.endswith("...")


def test_explicit_zero_is_unlimited(monkeypatch):
    out = _ctx(monkeypatch, {"tool_preview_length": 0}, "A" * 200)

    assert out == "A" * 200


def test_explicit_length_is_honored(monkeypatch):
    out = _ctx(monkeypatch, {"tool_preview_length": 40}, "A" * 200)

    assert len(out) == 40
    assert out.endswith("...")
