#!/usr/bin/env python3
"""
musicFestScheduler.py
---------------------
Schedule the maximum number of non-overlapping band performances
on a single stage in one day.

Algorithm:
    1. Sort all proposed slots by their end time (ascending).
    2. Scan the sorted list, always pick the earliest-finishing slot
       that starts after the last selected slot’s end.
This greedy rule is guaranteed optimal for the **activity-selection** problem.

Author: <your-name>
Date:   <today’s date>
"""

from typing import List, Tuple


def max_non_overlapping_slots(
    slots: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    """
    Given a list of (start, end) tuples, return the largest subset of
    mutually non-overlapping slots using a greedy earliest-finish strategy.

    Time Complexity:  O(n log n) for the sort, where n is the number of bands.
    Space Complexity: O(n) for storing the sorted copy / result list.
    """
    # Sort by end time; Python’s default Timsort is stable.
    slots_sorted = sorted(slots, key=lambda s: s[1])

    schedule: List[Tuple[int, int]] = []
    last_end = -float("inf")  # no slot selected yet

    for start, end in slots_sorted:
        if start >= last_end:
            schedule.append((start, end))
            last_end = end

    return schedule


def prompt_slots() -> List[Tuple[int, int]]:
    """
    Prompt the user for band count and their (start, end) times.
    Times are read as integers (e.g., minutes since doors open or 24-hour clock).
    """
    while True:
        try:
            n = int(input("Enter number of bands: ").strip())
            if n <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")

    slots: List[Tuple[int, int]] = []
    print("\nEnter each band’s start and end times separated by space (e.g. '100 245'):")
    for i in range(1, n + 1):
        while True:
            try:
                raw = input(f"  Band {i}: ").strip()
                start_str, end_str = raw.split()
                start, end = int(start_str), int(end_str)
                if start < 0 or end <= start:
                    raise ValueError
                slots.append((start, end))
                break
            except ValueError:
                print("    ⚠️  Invalid. Enter two integers where 0 ≤ start < end.")

    return slots


def print_schedule(schedule: List[Tuple[int, int]]) -> None:
    """Nicely print the chosen schedule."""
    print("\n🎵 Optimal Stage Schedule:")
    if not schedule:
        print("  (No bands can be scheduled.)")
        return

    for idx, (start, end) in enumerate(schedule, 1):
        print(f"  {idx}. {start} → {end}")
    print(f"\nTotal bands scheduled: {len(schedule)}")


def main() -> None:
    print("=== Music Festival Stage Scheduler ===")
    slots = prompt_slots()
    optimal_schedule = max_non_overlapping_slots(slots)
    print_schedule(optimal_schedule)


if __name__ == "__main__":
    main()
