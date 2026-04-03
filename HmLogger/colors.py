"""
Modul for ANSI color handling in terminal output. 
Exports:
- `Color`: A class for defining color codes for colored console output.
- `Text`: A class for defining text styles for colored console output.
- `supports_ansi`: A function to detect ANSI color support in the terminal.

Features:
- Provides a simple interface to create colored and styled text for terminal output.
- Automatic detection of terminal ANSI capabilities.
Usage:
```python
from logger.colors import Color, Text, supports_ansi

# Check if terminal supports ANSI colors
if supports_ansi():
    red_bold = Color("RED").bold()
    print(red_bold("This is a bold red text!"))
else:
    print("Terminal does not support ANSI colors")
```
"""

import os
import sys
import platform
from typing import Self

__all__ = ["Color", "Text", "supports_ansi"]


def supports_ansi() -> bool:
    """
    Check if the terminal supports ANSI colors.
    
    Considers various environments and returns True if colors are supported,
    False otherwise.
    
    The following environment variables are considered:
    - NO_COLOR: Disable colors if set (https://no-color.org)
    - FORCE_COLOR: Force enable colors if set
    - COLORTERM: 'truecolor' or '24bit' implies full ANSI support
    - TERM: 'dumb' disables colors
    - CI: Common CI environments are treated as ANSI-capable
    
    On Windows, attempts to enable Virtual Terminal Processing via the
    Win32 API before falling back to a version check.
    
    Returns:
        bool: True if ANSI colors are supported, False otherwise.
    """
    if os.environ.get("NO_COLOR"):
        return False

    if os.environ.get("FORCE_COLOR"):
        return True

    if any(os.environ.get(v) for v in ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "TF_BUILD")):
        return True

    if not sys.stdout.isatty():
        return False

    if os.environ.get("TERM", "").lower() == "dumb":
        return False

    if platform.system() == "Windows":
        return _windows_ansi_supported()

    # COLORTERM signals explicit colour capability
    if os.environ.get("COLORTERM", "").lower() in ("truecolor", "24bit"):
        return True

    term = os.environ.get("TERM", "")
    return bool(term) 


def _windows_ansi_supported() -> bool:
    """Try to enable ANSI via Win32 API; fall back to Windows version check."""
    try:
        import ctypes
        import ctypes.wintypes
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32 = ctypes.windll.kernel32  
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        mode = ctypes.wintypes.DWORD()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        if mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING:
            return True
        return bool(kernel32.SetConsoleMode(
            handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
        ))
    except Exception:
        ver = sys.getwindowsversion()  
        return ver.major > 10 or (ver.major == 10 and ver.build >= 14393)

class Color():
    """Represents an ANSI color with optional styles like bold, italic, underline, etc."""
    Colors : dict[str, int] = {
        "DEFAULT": 0,
        "GREY": 30,
        "RED": 31,
        "GREEN": 32,
        "YELLOW": 33,
        "BLUE": 34,
        "MAGENTA": 35,
        "CYAN": 36,
        "WHITE": 37,
    }

    RESET = "\033[0m"

    def __init__(self, name: str):
        if name.upper() not in self.Colors:
            raise ValueError(f"Invalid color name: {name}. Allowed values are: {', '.join(self.Colors.keys())}")
        
        object.__setattr__(self, 'name', name.upper())
        object.__setattr__(self, 'code', self.Colors[name.upper()])
        object.__setattr__(self, '_styles', ())
        object.__setattr__(self, '_intense', False)

    def __setattr__(self, name: str, value) -> None:
        raise AttributeError("Color instances are immutable")

    def __hash__(self) -> int:
        return hash((self.name, self._styles, self._intense))

    def _copy_with(self, *, styles: tuple[int, ...] | None = None, intense: bool | None = None) -> Self:
        new = Color.__new__(Color)
        object.__setattr__(new, 'name', self.name)
        object.__setattr__(new, 'code', self.code)
        object.__setattr__(new, '_styles', self._styles if styles is None else styles)
        object.__setattr__(new, '_intense', self._intense if intense is None else intense)
        return new

    def bold(self) -> Self:
        """
        Returns the ANSI escape sequence for bold text.
        """
        if 1 in self._styles:
            return self
        return self._copy_with(styles=(*self._styles, 1))

    def dim(self) -> Self:
        """
        Returns the ANSI escape sequence for dimmed text.
        """
        if 2 in self._styles:
            return self
        return self._copy_with(styles=(*self._styles, 2))

    def italic(self) -> Self:
        """
        Returns the ANSI escape sequence for italic text.
        """
        if 3 in self._styles:
            return self
        return self._copy_with(styles=(*self._styles, 3))

    def underline(self) -> Self:
        """
        Returns the ANSI escape sequence for underlined text.
        """
        if 4 in self._styles:
            return self
        return self._copy_with(styles=(*self._styles, 4))

    def blink(self) -> Self:
        """
        Returns the ANSI escape sequence for blinking text.
        """
        if 5 in self._styles:
            return self
        return self._copy_with(styles=(*self._styles, 5))

    def reversed(self) -> Self:
        """
        Returns the ANSI escape sequence for reversed colors.
        """
        if 7 in self._styles:
            return self
        return self._copy_with(styles=(*self._styles, 7))

    def strikethrough(self) -> Self:
        """
        Returns the ANSI escape sequence for strikethrough text.
        """
        if 9 in self._styles:
            return self
        return self._copy_with(styles=(*self._styles, 9))

    def intense(self) -> Self:
        """
        Returns the ANSI escape sequence for intense colors.
        """
        if self._intense or self.name == "DEFAULT":
            return self
        return self._copy_with(intense=True)

    def reset(self) -> Self:
        """
        Reset all styles.
        """
        if not self._styles and not self._intense:
            return self
        return self._copy_with(styles=(), intense=False)

    def __str__(self) -> str:
        color_code = self.code + 60 if self._intense and self.name != "DEFAULT" else self.code
        segments = [*self._styles, color_code]
        return f"\033[{';'.join(map(str, segments))}m"

    def apply(self, text: str) -> str:
        """
        Wrap text with current style and append a reset.
        """
        return f"{self}{text}{self.RESET}"

    def __call__(self, text: str) -> str:
        return self.apply(text)

    def __repr__(self) -> str:
        return self.__str__()

class Text():
    """Represents text with a specific color and optional styles."""
    def __init__(self, text: str, color: Color):
        self.text :str = text
        self.color :Color = color

    def __str__(self) -> str:
        return self.color(self.text)
