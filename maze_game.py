import random
import time
import copy

# N = 10 # Global N removed

class Mai:
    def __init__(self, N_val=10):
        self.N = N_val
        self.mat = [[2 for _ in range(self.N)] for _ in range(self.N)] # Use self.N
        self.stack = []
        self.tos = 0
        self.f_flag_find = 0
        self.path_found_globally = False

    def push(self, x, y):
        self.stack.append((x, y))
        self.tos += 1

    def pop(self):
        if self.tos > 0:
            self.tos -= 1
            return self.stack.pop()
        return None

    def inti(self, p):
        for i in range(self.N):
            for j in range(self.N):
                self.mat[i][j] = p

    def _clear_screen(self):
        print("\n" * 50)

    def _tim(self, duration_ms):
        time.sleep(duration_ms / 1000.0)

    def print_maze(self):
        prefix = "@!\t\t"
        for i in range(self.N):
            print(prefix, end="")
            for j in range(self.N):
                cell_value = self.mat[i][j]
                if cell_value == 7: # Path segment for find/guide
                    print("  ", end="")
                else:
                    print(f"{cell_value:2}", end="")
            print()

        footer = (
            "\n\t!!!++++++++++++++++++++++++++++!!!\n"
            "\t!======Powered by Pejman.Gh======!\n"
            "\t!=========Haika.ir=========!\n"
            "\t!!!++++++++++++++++++++++++++++!!!"
        )
        print(footer)

    def route(self):
        r, c = 0, 0
        # Start with a grid of 2s (already set by __init__ or game.inti(2))
        self.mat[r][c] = 0  # Mark starting cell

        for _ in range(2 * self.N * self.N * self.N): # Timeout
            if r == self.N - 1:
                return 1  # Success

            prev_r, prev_c = r, c
            temp_next_r, temp_next_c = prev_r, prev_c

            if prev_r == 0 or prev_c == 0:
                temp_next_r = prev_r + 1
                temp_next_c = prev_c + 1
            else:
                k = random.randint(0, 17)
                if k == 1: temp_next_r = prev_r + 1
                elif k == 2: temp_next_c = prev_c + 1
                elif k == 3 or k == 10: temp_next_r = prev_r + 1; temp_next_c = prev_c - 1
                elif k == 4 or k == 8: temp_next_r = prev_r - 1; temp_next_c = prev_c + 1
                elif k == 5 or k == 9 or k == 14: temp_next_r = prev_r - 1
                elif k == 6 or k == 11 or k == 15: temp_next_c = prev_c - 1
                elif k == 7 or k == 12 or k == 13 or k == 16: temp_next_r = prev_r - 1; temp_next_c = prev_c - 1
                else: temp_next_r = prev_r + 1; temp_next_c = prev_c + 1

            temp_next_r = max(0, min(temp_next_r, self.N - 1))
            temp_next_c = max(0, min(temp_next_c, self.N - 1))

            h_count = 0
            p_start, p_end = max(0, temp_next_r - 1), min(self.N - 1, temp_next_r + 1)
            q_start, q_end = max(0, temp_next_c - 1), min(self.N - 1, temp_next_c + 1)

            for p_iter in range(p_start, p_end + 1):
                for q_iter in range(q_start, q_end + 1):
                    if self.mat[p_iter][q_iter] == 0:
                        h_count += 1

            if h_count == 1 and self.mat[temp_next_r][temp_next_c] != 0:
                r, c = temp_next_r, temp_next_c
                self.mat[r][c] = 0
            else:
                r, c = prev_r, prev_c
        return -1 # Timeout

    def complete(self):
        for r in range(self.N):
            for c in range(self.N):
                if self.mat[r][c] == 2: # Process only unvisited cells by route
                    h_count = 0
                    p_start, p_end = max(0, r - 1), min(self.N - 1, r + 1)
                    q_start, q_end = max(0, c - 1), min(self.N - 1, c + 1)

                    for p in range(p_start, p_end + 1):
                        for q in range(q_start, q_end + 1):
                            if p == r and q == c: continue
                            if self.mat[p][q] == 0:
                                h_count += 1

                    is_last_row = (r == self.N - 1)
                    condition_A = is_last_row and h_count == 0
                    condition_B = (not is_last_row) and (h_count < 2)

                    if condition_A or condition_B:
                        self.mat[r][c] = 0
                    else:
                        self.mat[r][c] = 1

    def find(self, r, c):
        if self.path_found_globally:
            return True

        nr_from, nr_to = max(0, r - 1), min(self.N - 1, r + 1)
        nc_from, nc_to = max(0, c - 1), min(self.N - 1, c + 1)

        for nr in range(nr_from, nr_to + 1):
            for nc in range(nc_from, nc_to + 1):
                if self.path_found_globally:
                    return True

                if nr == r and nc == c:
                    continue

                if self.mat[nr][nc] == 0:
                    if self.f_flag_find == 1:
                        self._clear_screen()
                        self.mat[r][c] = 1
                        self.print_maze(); self._tim(150)
                        self.mat[r][c] = 7
                        self.print_maze(); self._tim(150)
                        self._clear_screen()
                        self.mat[r][c] = 1
                        self.print_maze(); self._tim(150)
                        self.mat[r][c] = 7
                        self.print_maze(); self._tim(200)
                        self.f_flag_find = 0

                    self.push(nr, nc)
                    self.mat[nr][nc] = 7

                    self._clear_screen()
                    self.print_maze()
                    print('\a', end='', flush=True)
                    self._tim(250)

                    if nr == self.N - 1:
                        for _ in range(6):
                            print('\a', end='', flush=True); self._tim(50)
                        print("\n      Route Found!")
                        self.inti(1) # Fills with 1s
                        self.path_found_globally = True
                        return True

                    else:
                        if self.find(nr, nc):
                           return True

        if self.path_found_globally:
            return True

        self._clear_screen()
        self.mat[r][c] = 1
        if self.tos > 0 and self.stack and self.stack[-1] == (r,c) :
             self.pop()

        self.print_maze()
        print('\a', end='', flush=True)
        self._tim(100)
        self.f_flag_find = 1
        return False

    def fill_route_on_matrix(self, value):
        for (r_path, c_path) in self.stack: # renamed to avoid conflict
            if 0 <= r_path < self.N and 0 <= c_path < self.N:
                self.mat[r_path][c_path] = value

    def is_on_stack(self, r_check, c_check):
        return (r_check, c_check) in self.stack

    def guide_animation(self, path_value):
        for k in range(len(self.stack)):
            curr_anim_r, curr_anim_c = self.stack[k]

            self._clear_screen()
            if 0 <= curr_anim_r < self.N and 0 <= curr_anim_c < self.N:
                self.mat[curr_anim_r][curr_anim_c] = path_value # Current anim cell gets path_value

            prefix = "@!\t\t"
            for r_print in range(self.N):
                print(prefix, end="")
                for c_print in range(self.N):
                    if r_print == curr_anim_r and c_print == curr_anim_c:
                        val_to_print = self.mat[r_print][c_print]
                        print(f"{val_to_print:2}", end="")
                    elif self.is_on_stack(r_print, c_print):
                        # Other cells on stack are temporarily hidden or shown differently
                        # If they were previously set by fill_route_on_matrix, guide_animation might overwrite them
                        # For this logic: other stack cells are blanked.
                        print("  ", end="")
                    else:
                        cell_val = self.mat[r_print][c_print]
                        if cell_val == 7: # Should not happen if path cells are handled above
                            print("  ", end="")
                        else:
                            print(f"{cell_val:2}", end="")
                print()

            footer = (
                "\n\t!!!++++++++++++++++++++++++++++!!!\n"
                "\t!======Powered by Pejman.Gh======!\n"
                "\t!=========Haika.ir=========!\n"
                "\t!!!++++++++++++++++++++++++++++!!!"
            )
            print(footer)
            self._tim(80)

        print('\a', end='', flush=True)


if __name__ == "__main__":
    user_n = 10 # Default
    while True:
        try:
            raw_input_val = input(f"Enter the maze size (N x N), e.g., 10 (current default: {user_n}, min 5, max 30): ")
            if not raw_input_val: # User pressed Enter without typing anything
                print(f"Using default size N={user_n}.")
                break
            temp_n = int(raw_input_val)
            if 5 <= temp_n <= 30:
                user_n = temp_n
                break
            else:
                print("Size out of range. Please enter a value between 5 and 30.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
        except EOFError: # Handle non-interactive environment
            print(f"No input received. Using default size N={user_n}.")
            break # user_n remains its default or last valid value

    game = Mai(N_val=user_n)
    game._clear_screen()
    print("\t\tPLEASE WAIT COMPUTER IS MAKING PUZZLE\n")

    while True:
        game.inti(2) # Ensure fresh state of 2s for route generation
        route_success_code = game.route()
        if route_success_code != -1:
            break
        # game.inti(2) # Already done at the start of the loop

    game.complete()
    maze_snapshot_mat = copy.deepcopy(game.mat)

    game._clear_screen()
    game.print_maze()
    game._tim(40)

    print('\a', end='', flush=True)
    print("\n\t\t PUZZLE MAKE Correctly")
    print("\t  Press Any Key to See How Locate")
    print("\n ( ( ) is Guid & 0 is Open route & 1 is Close route)")
    try:
        input()
    except EOFError:
        print("Continuing without input (EOFError).")
    game._tim(200)

    path_actually_found = False
    if game.mat[0][0] == 0:
        game.push(0,0)
        game.mat[0][0] = 7
        path_actually_found = game.find(0,0)
    else:
        print("Error: (0,0) is not a valid starting path cell after maze generation.")

    if path_actually_found:
        # find() called inti(1), matrix is all 1s. Stack has the path.
        # guide_animation loop (0, 1, 2)
        # The C++ version calls gu(0), then gu(1), then gu(2).
        # Each gu(p) sets current animated cell to p. Other stack cells are "  ". Non-stack cells are background.
        # So, after gu(0), path is 0s. After gu(1), path is 1s. After gu(2), path is 2s.
        # The matrix is all 1s before this loop.
        # guide_animation will modify game.mat.
        for i in range(3):
            # At start of each guide_animation, path cells in game.mat are from previous animation step or inti(1)
            # For the first run (i=0), game.mat is all 1s (from inti(1) in find).
            # guide_animation will set cells on stack to 0 one by one.
            # Then for i=1, it will set them to 1 one by one.
            # Then for i=2, it will set them to 2 one by one.
            # So, after this loop, all cells on the stack in game.mat will be 2.
            game.guide_animation(i)

        game._clear_screen()
        for i in range(11):
            game._clear_screen()
            path_val_blink = 0 if i % 2 == 0 else 7
            # game.mat currently has path cells as 2 (from last guide_animation(2))
            # and non-path cells as 1 (from inti(1)).
            # fill_route_on_matrix will change the '2's on the stack to 0 or 7.
            game.fill_route_on_matrix(path_val_blink)
            game.print_maze() # Will show blinking path (0 or spaces) on background of 1s
            print('\a', end='', flush=True)
            game._tim(80)

        for _ in range(4): print('\a', end='', flush=True); game._tim(50)
        print('\a', end='', flush=True); game._tim(500)
        for _ in range(4): print('\a', end='', flush=True); game._tim(50)

        game._clear_screen()
        # game.mat has path as 0 or 7 from last blink. Non-path is 1.
        game.fill_route_on_matrix(7) # Final path shown as 7 (spaces)
        game.print_maze()

    game_snapshot_display = Mai()
    game_snapshot_display.mat = maze_snapshot_mat
    game_snapshot_display.N = game.N
    print("\nOriginal maze (snapshot before find):")
    game_snapshot_display.print_maze()

    print('\a', end='', flush=True)
    game._tim(50)
    print("\n\t\t\t  OK")
    print("\t\tPress Any Key to Exit")
    try:
        input()
    except EOFError:
        print("Exiting without input (EOFError).")
    game._clear_screen()

    game._tim(30)
    print('\a', end='', flush=True)
    print("\n\n\n\n\n\t\t\t\t THANK YOU")
    game._tim(300)
    print("\n\n\t\t\t\a       Haika.ir ")
    game._tim(300)
