from collections import deque


def solve_monkey_banana(
    monkey_start="A", box_start="C", banana_pos="B", positions=("A", "B", "C")
):
    """Solves the Monkey Banana Problem using Breadth-First Search (BFS).

    State representation:
        (monkey_pos, box_pos, monkey_level, has_banana)
        - monkey_pos: 'A', 'B', or 'C'
        - box_pos: 'A', 'B', or 'C'
        - monkey_level: 'floor' or 'on_box'
        - has_banana: True or False
    """
    initial_state = (monkey_start, box_start, "floor", False)

    # Queue stores: (current_state, action_history)
    queue = deque([(initial_state, [])])
    visited = {initial_state}

    while queue:
        (m_pos, b_pos, m_lvl, has_banana), path = queue.popleft()

        # Goal test
        if has_banana:
            return path

        # --- Transition Rules / Actions ---

        # 1. Walk: Monkey moves alone on the floor
        if m_lvl == "floor":
            for dest in positions:
                if dest != m_pos:
                    next_state = (dest, b_pos, m_lvl, has_banana)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append(
                            (
                                next_state,
                                path + [f"Walk from {m_pos} to {dest}"],
                            )
                        )

        # 2. Push: Monkey pushes the box along the floor
        if m_lvl == "floor" and m_pos == b_pos:
            for dest in positions:
                if dest != b_pos:
                    next_state = (dest, dest, m_lvl, has_banana)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append(
                            (
                                next_state,
                                path
                                + [f"Push the box from {b_pos} to {dest}"],
                            )
                        )

        # 3. Climb onto the box
        if m_lvl == "floor" and m_pos == b_pos:
            next_state = (m_pos, b_pos, "on_box", has_banana)
            if next_state not in visited:
                visited.add(next_state)
                queue.append(
                    (next_state, path + [f"Climb onto the box at {m_pos}"])
                )

        # 4. Climb down to the floor
        if m_lvl == "on_box":
            next_state = (m_pos, b_pos, "floor", has_banana)
            if next_state not in visited:
                visited.add(next_state)
                queue.append(
                    (next_state, path + [f"Climb down to the floor at {m_pos}"])
                )

        # 5. Grasp the banana
        if m_lvl == "on_box" and m_pos == banana_pos and not has_banana:
            next_state = (m_pos, b_pos, m_lvl, True)
            if next_state not in visited:
                visited.add(next_state)
                queue.append(
                    (next_state, path + [f"Grasp the banana at {banana_pos}"])
                )

    return None


if __name__ == "__main__":
    print("Initial Configuration:")
    print("  Monkey: Floor at A")
    print("  Box:    Floor at C")
    print("  Banana: Ceiling at B\n")

    steps = solve_monkey_banana()

    if steps:
        print("Plan Found:")
        for i, step in enumerate(steps, start=1):
            print(f"  Step {i}: {step}")
        print(f"\nGoal Reached in {len(steps)} steps!")
    else:
        print("No solution found.")
