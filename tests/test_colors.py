"""Tests for color utilities and ANSI detection."""

from __future__ import annotations

import HmLogger
import HmLogger.colors as colors_module


def test_color_is_immutable_and_chainable() -> None:
    color = HmLogger.Color("red")
    styled = color.bold().underline()

    assert color is not styled
    assert str(color) == "\033[31m"
    assert str(styled) == "\033[1;4;31m"

    # Re-applying an existing style should not create a new object.
    assert styled.bold() is styled


def test_color_apply_wraps_reset() -> None:
    text = HmLogger.Color("green").bold().apply("hello")
    assert text.startswith("\033[")
    assert text.endswith(HmLogger.Color.RESET)
    assert "hello" in text


def test_supports_ansi_honors_no_color(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr(colors_module.sys.stdout, "isatty", lambda: True)
    assert HmLogger.supports_ansi() is False


def test_supports_ansi_with_tty_and_term(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setattr(colors_module.sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr(colors_module.platform, "system", lambda: "Linux")
    monkeypatch.setenv("TERM", "xterm-256color")
    assert HmLogger.supports_ansi() is True
