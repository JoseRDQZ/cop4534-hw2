#!/usr/bin/env python3
"""
conferenceScheduler.py
======================
Greedy two-room seminar scheduler that attempts to maximize total profit.

Strategy
--------
1. Sort seminars by descending profit (most lucrative first).
2. For each seminar, place it in the first room where it fits
   (no time overlap). If it fits in neither room, skip it.
3. Within each room, keep the schedule sorted by start time for
   quick overlap checks.

Note
----
This greedy heuristic is not guaranteed optimal for the two-room
weighted-interval problem. A counter-example will be provided in the
written explanation, along with references to optimal DP/flow methods.

Author : <your-name>
Date   : <today’s date>
"""
from typing import List, Tuple


Seminar = Tuple[int, int, int]          # (start, end, profit)
Schedule = List[Seminar]                # list of non-overlapping seminars


# ---------------------------------------------------------------
#  Greedy helpers
# ---------------------------------------------------------------
def fits(room: Schedule, seminar: Seminar) -> bool:
    s, e, _ = seminar
    for a, b, _ in room:
        if not (e <= a or s >= b):      # overlap
            return False
    return True


def add_to_room(room: Schedule, seminar: Seminar) -> None:
    """Insert seminar and keep schedule ordered by start time."""
    room.append(seminar)
    room.sort(key=lambda x: x[0])


# ---------------------------------------------------------------
#  Main greedy algorithm
# ---------------------------------------------------------------
def greedy_two_room_schedule(seminars: List[Seminar]) -> Tuple[Schedule, Schedule, int]:
    seminars_sorted = sorted(seminars, key=lambda x: x[2], reverse=True)

    room1: Schedule = []
    room2: Schedule = []
    total_profit = 0

    for sem in seminars_sorted:
        if fits(room1, sem):
            add_to_room(room1, sem)
            total_profit += sem[2]
        elif fits(room2, sem):
            add_to_room(room2, sem)
            total_profit += sem[2]
        # else: cannot place without a third room

    return room1, room2, total_profit


# ---------------------------------------------------------------
#  I/O helpers
# ---------------------------------------------------------------
def prompt_int(prompt: str, cond=lambda x: True) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if not cond(val):
                raise ValueError
            return val
        except ValueError:
            print("  Invalid input. Please enter a valid integer.")


def get_seminars_interactively() -> List[Seminar]:
    print("\nEnter seminar data:")
    n = prompt_int("  Number of seminars: ", lambda x: x > 0)

    seminars: List[Seminar] = []
    print("  Provide each seminar as: start end profit")
    for i in range(1, n + 1):
        while True:
            raw = input(f"    Seminar {i}: ").strip().split()
            if len(raw) != 3:
                print("      Please enter exactly 3 integers.")
                continue
            try:
                s, e, p = map(int, raw)
                if not (0 <= s < e and p >= 0):
                    raise ValueError
                seminars.append((s, e, p))
                break
            except ValueError:
                print("      Invalid values. Try again.")
    return seminars


def demo_seminars() -> List[Seminar]:
    """Fixed demo set (8 seminars)."""
    return [
        (9,  12,  8),
        (11, 14, 10),
        (13, 16,  5),
        (15, 18,  7),
        (10, 11,  3),
        (12, 15,  6),
        (16, 19, 12),
        (9,  10,  4)
    ]


# ---------------------------------------------------------------
#  Pretty printing
# ---------------------------------------------------------------
def print_schedule(room: Schedule, name: str) -> None:
    if not room:
        print(f"  {name}: (empty)")
        return
    print(f"  {name}:")
    for s, e, p in sorted(room, key=lambda x: x[0]):
        print(f"    {s:02d}-{e:02d}  profit = {p}")


# ---------------------------------------------------------------
#  Main driver
# ---------------------------------------------------------------
def main() -> None:
    print("=== Conference Room Scheduler (2 rooms, greedy) ===")
    use_demo = input("Load demo seminars? [Y/n]: ").strip().lower()
    seminars = demo_seminars() if use_demo in ("", "y", "yes") else get_seminars_interactively()

    room1, room2, total = greedy_two_room_schedule(seminars)

    print("\nFinal Schedule:")
    print_schedule(room1, "Room 1")
    print_schedule(room2, "Room 2")
    print(f"\nTotal profit: {total}")


if __name__ == "__main__":
    main()
