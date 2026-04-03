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
    - NO_COLOR: Disable colors if set
    - FORCE_COLOR: Force enable colors if set
    - TERM: Terminal type is checked
    
    Returns:
        bool: True if ANSI colors are supported, False otherwise.
    """
    if os.environ.get("NO_COLOR"):
        return False
    
    if os.environ.get("FORCE_COLOR"):
        return True
    
    if platform.system() == "Windows":
        return True
    
    if not sys.stdout.isatty():
        return False
    
    term = os.environ.get("TERM", "").lower()
    return term not in ("dumb", "")

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
        
        self.name = name.upper()
        self.code = self.Colors[self.name]
        self._styles: list[int] = []
        self._intense = False

    def bold(self) -> Self:
        """
        Returns the ANSI escape sequence for bold text.
        """
        if 1 not in self._styles:
            self._styles.append(1)

        return self

    def dim(self) -> Self:
        """
        Returns the ANSI escape sequence for dimmed text.
        """
        if 2 not in self._styles:
            self._styles.append(2)
        return self

    def italic(self) -> Self:
        """
        Returns the ANSI escape sequence for italic text.
        """
        if 3 not in self._styles:
            self._styles.append(3)
        return self

    def underline(self) -> Self:
        """
        Returns the ANSI escape sequence for underlined text.
        """
        if 4 not in self._styles:
            self._styles.append(4)
        return self
    
    def blink(self) -> Self:
        """
        Returns the ANSI escape sequence for blinking text.
        """
        if 5 not in self._styles:
            self._styles.append(5)
        return self
    
    def reversed(self) -> Self:
        """
        Returns the ANSI escape sequence for reversed colors.
        """
        if 7 not in self._styles:
            self._styles.append(7)
        return self
    
    def strikethrough(self) -> Self:
        """
        Returns the ANSI escape sequence for strikethrough text.
        """
        if 9 not in self._styles:
            self._styles.append(9)
        return self
    
    def intense(self) -> Self:
        """
        Returns the ANSI escape sequence for intense colors.
        """
        if self.name != "DEFAULT":
            self._intense = True
        return self
    
    def reset(self) -> Self:
        """
        Reset all styles.
        """
        self._styles.clear()
        self._intense = False
        return self

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
