#!/usr/bin/env python3
"""Render an infinite concentric circle animation in the terminal."""
from __future__ import annotations

import math
import os
import shutil
import sys
import time


def get_terminal_size() -> tuple[int, int]:
    """Return terminal width and height with sensible fallbacks."""
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    # Ensure we have a minimum canvas to render on.
    return max(columns, 40), max(rows, 20)


def render_frame(time_offset: float, width: int, height: int) -> str:
    """Generate a single animation frame for the current time offset."""
    cx = (width - 1) / 2.0
    cy = (height - 1) / 2.0
    aspect_ratio = 2.0  # compensate for character height vs width
    spacing = 3.0  # distance between consecutive rings
    thickness = 0.7  # width of each ring in distance units

    rows: list[str] = []
    for y in range(height):
        dy = (y - cy) * aspect_ratio
        row_chars: list[str] = []
        for x in range(width):
            dx = x - cx
            distance = math.hypot(dx, dy)
            # Create an infinite sequence of rings by wrapping the distance.
            phase = (distance - time_offset) % spacing
            if phase < thickness:
                # Vary the character brightness based on proximity to the ring center.
                intensity = 1.0 - (phase / thickness)
                if intensity > 0.66:
                    char = "●"
                elif intensity > 0.33:
                    char = "•"
                else:
                    char = "·"
            else:
                char = " "
            row_chars.append(char)
        rows.append("".join(row_chars))
    return "\n".join(rows)


def main() -> None:
    """Run the concentric circle animation until interrupted."""
    try:
        # Hide the cursor for a cleaner visual.
        sys.stdout.write("\x1b[?25l")
        sys.stdout.flush()
        start_time = time.perf_counter()
        max_frames = int(os.environ.get("CIRCLE_FRAMES", "0"))
        frame_count = 0
        while True:
            if max_frames and frame_count >= max_frames:
                break
            width, height = get_terminal_size()
            elapsed = time.perf_counter() - start_time
            frame = render_frame(elapsed * 2.0, width, height)
            # Clear screen and move cursor to home position.
            sys.stdout.write("\x1b[H\x1b[2J")
            sys.stdout.write(frame)
            sys.stdout.flush()
            time.sleep(1 / 30)
            frame_count += 1
    except KeyboardInterrupt:
        pass
    finally:
        # Restore cursor visibility.
        sys.stdout.write("\x1b[?25h\x1b[0m\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
