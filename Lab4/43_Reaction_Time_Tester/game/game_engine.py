
import pygame
import math
import array

from .round import Round


WHITE = (255, 255, 255)
GRAY = (90, 90, 90)
GREEN = (40, 180, 90)
BLUE = (50, 90, 170)
RED = (190, 60, 60)
DARK_BLUE = (25, 40, 80)


class GameEngine:

    DIFFICULTIES = {

        "Easy": {
            "rounds": 3,
            "min_wait": 1500,
            "max_wait": 3000
        },

        "Medium": {
            "rounds": 5,
            "min_wait": 1000,
            "max_wait": 2500
        },

        "Hard": {
            "rounds": 7,
            "min_wait": 700,
            "max_wait": 1800
        }
    }

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.font = pygame.font.SysFont(
            "Arial", 28
        )

        self.small_font = pygame.font.SysFont(
            "Arial", 22
        )

        self.big_font = pygame.font.SysFont(
            "Arial", 46
        )

        self.mode = "menu"

        self.difficulty = "Medium"

        self.rounds_total = 5
        self.min_wait_ms = 1000
        self.max_wait_ms = 2500

        self.round = None

        self.reaction_times = []

        self.false_starts = 0

        self.result_shown_at = None

        self.result_pause_ms = 900

        self.message = ""

        # Initialize sound effects.
        self.sounds_enabled = False

        self._init_sounds()

    # ==================================================
    # SOUND
    # ==================================================

    def _init_sounds(self):

        try:

            # Initialize mixer if necessary.
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            sample_rate = 22050

            # GO sound
            self.go_sound = self._make_tone(
                880,
                120,
                sample_rate
            )

            # False-start sound
            self.false_start_sound = self._make_tone(
                220,
                220,
                sample_rate
            )

            # Session-ending sound
            self.end_sound = self._make_tone(
                660,
                300,
                sample_rate
            )

            self.sounds_enabled = True

        except pygame.error:

            # If audio isn't available,
            # the game still runs normally.
            self.sounds_enabled = False

    @staticmethod
    def _make_tone(
        frequency,
        duration_ms,
        sample_rate
    ):

        sample_count = int(
            sample_rate
            * duration_ms
            / 1000
        )

        amplitude = 12000

        samples = array.array(
            "h"
        )

        for i in range(sample_count):

            value = int(
                amplitude
                * math.sin(
                    2
                    * math.pi
                    * frequency
                    * (i / sample_rate)
                )
            )

            samples.append(value)

        return pygame.mixer.Sound(
            buffer=samples.tobytes()
        )

    def _play_sound(self, sound):

        if self.sounds_enabled:
            sound.play()

    # ==================================================
    # DIFFICULTY
    # ==================================================

    def _apply_difficulty(self, difficulty):

        config = self.DIFFICULTIES[difficulty]

        self.difficulty = difficulty

        self.rounds_total = config["rounds"]

        self.min_wait_ms = config["min_wait"]

        self.max_wait_ms = config["max_wait"]

    # ==================================================
    # START GAME
    # ==================================================

    def _start_game(self):

        self.reaction_times = []

        self.false_starts = 0

        self.result_shown_at = None

        self.message = ""

        self.round = Round(
            self.min_wait_ms,
            self.max_wait_ms
        )

        self.mode = "playing"

    # ==================================================
    # EVENT HANDLING
    # ==================================================

    def handle_event(self, event):

        if event.type == pygame.QUIT:
            return False

        # ----------------------------------------------
        # MENU
        # ----------------------------------------------

        if self.mode == "menu":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:

                    self._apply_difficulty(
                        "Easy"
                    )

                    self._start_game()

                elif event.key == pygame.K_2:

                    self._apply_difficulty(
                        "Medium"
                    )

                    self._start_game()

                elif event.key == pygame.K_3:

                    self._apply_difficulty(
                        "Hard"
                    )

                    self._start_game()

                elif event.key == pygame.K_ESCAPE:

                    return False

        # ----------------------------------------------
        # PLAYING
        # ----------------------------------------------

        elif self.mode == "playing":

            is_click = (
                event.type
                == pygame.MOUSEBUTTONDOWN
            )

            is_space = (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            )

            if is_click or is_space:

                reaction_ms = (
                    self.round.register_input()
                )

                # --------------------------------------
                # FALSE START
                # --------------------------------------

                if (
                    reaction_ms is None
                    and self.round.state
                    == "false_start"
                ):

                    self.false_starts += 1

                    self.message = (
                        "False start!"
                    )

                    self.result_shown_at = (
                        pygame.time.get_ticks()
                    )

                    # Task 4:
                    # play false-start sound.
                    self._play_sound(
                        self.false_start_sound
                    )

                # --------------------------------------
                # VALID REACTION
                # --------------------------------------

                elif reaction_ms is not None:

                    self.reaction_times.append(
                        reaction_ms
                    )

                    self.message = (
                        f"{reaction_ms} ms"
                    )

                    self.result_shown_at = (
                        pygame.time.get_ticks()
                    )

        # ----------------------------------------------
        # RESULTS
        # ----------------------------------------------

        elif self.mode == "results":

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_1,
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):

                    self.mode = "menu"

                elif event.key in (
                    pygame.K_2,
                    pygame.K_ESCAPE
                ):

                    return False

        return True

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if self.mode != "playing":
            return

        old_state = self.round.state

        self.round.update()

        # ----------------------------------------------
        # GO SOUND
        # ----------------------------------------------

        # Detect transition:
        #
        # waiting -> go
        #
        # This means the green screen has just appeared.

        if (
            old_state == "waiting"
            and self.round.state == "go"
        ):

            self._play_sound(
                self.go_sound
            )

        # ----------------------------------------------
        # RESULT / FALSE START
        # ----------------------------------------------

        if self.round.state in (
            "result",
            "false_start"
        ):

            now = pygame.time.get_ticks()

            if (
                self.result_shown_at is not None
                and now - self.result_shown_at
                >= self.result_pause_ms
            ):

                # --------------------------------------
                # FALSE START
                # --------------------------------------

                if (
                    self.round.state
                    == "false_start"
                ):

                    # Restart the same round.
                    self.round = Round(
                        self.min_wait_ms,
                        self.max_wait_ms
                    )

                    self.message = ""

                # --------------------------------------
                # SESSION COMPLETE
                # --------------------------------------

                elif (
                    len(self.reaction_times)
                    >= self.rounds_total
                ):

                    self.mode = "results"

                    # Task 4:
                    # play session-ending sound.
                    self._play_sound(
                        self.end_sound
                    )

                # --------------------------------------
                # NEXT ROUND
                # --------------------------------------

                else:

                    self.round = Round(
                        self.min_wait_ms,
                        self.max_wait_ms
                    )

                    self.message = ""

    # ==================================================
    # INPUT
    # ==================================================

    def handle_input(self):
        pass

    # ==================================================
    # AVERAGE
    # ==================================================

    def average_reaction_ms(self):

        if not self.reaction_times:
            return 0

        return round(
            sum(self.reaction_times)
            / len(self.reaction_times)
        )

    # ==================================================
    # RENDER
    # ==================================================

    def render(self, screen):

        if self.mode == "menu":

            self._render_menu(screen)

        elif self.mode == "playing":

            self._render_game(screen)

        elif self.mode == "results":

            self._render_results(screen)

    # ==================================================
    # MENU
    # ==================================================

    def _render_menu(self, screen):

        screen.fill(DARK_BLUE)

        title = self.big_font.render(
            "Reaction Time Tester",
            True,
            WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    self.width // 2,
                    70
                )
            )
        )

        subtitle = self.font.render(
            "Choose a difficulty",
            True,
            WHITE
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(
                    self.width // 2,
                    125
                )
            )
        )

        options = [

            (
                "1",
                "Easy",
                "3 rounds | 1.5-3.0 sec"
            ),

            (
                "2",
                "Medium",
                "5 rounds | 1.0-2.5 sec"
            ),

            (
                "3",
                "Hard",
                "7 rounds | 0.7-1.8 sec"
            )
        ]

        y = 185

        for key, name, description in options:

            line = self.font.render(
                f"{key}. {name}",
                True,
                WHITE
            )

            desc = self.small_font.render(
                description,
                True,
                WHITE
            )

            screen.blit(
                line,
                (80, y)
            )

            screen.blit(
                desc,
                (240, y + 4)
            )

            y += 60

        footer = self.small_font.render(
            "Press 1, 2 or 3 to start | Esc to exit",
            True,
            WHITE
        )

        screen.blit(
            footer,
            footer.get_rect(
                center=(
                    self.width // 2,
                    365
                )
            )
        )

    # ==================================================
    # GAME
    # ==================================================

    def _render_game(self, screen):

        if self.round.state == "waiting":

            bg = GRAY

            message = (
                "Wait for green..."
            )

        elif self.round.state == "go":

            bg = GREEN

            message = (
                "CLICK / SPACE!"
            )

        elif self.round.state == "false_start":

            bg = RED

            message = (
                "FALSE START"
            )

        else:

            bg = BLUE

            message = self.message

        screen.fill(bg)

        text = self.big_font.render(
            message,
            True,
            WHITE
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2
                )
            )
        )

        round_num = min(
            len(self.reaction_times) + 1,
            self.rounds_total
        )

        round_text = self.small_font.render(
            f"Round {round_num}/{self.rounds_total}",
            True,
            WHITE
        )

        screen.blit(
            round_text,
            (10, 10)
        )

        average = self.small_font.render(
            f"Avg: {self.average_reaction_ms()} ms",
            True,
            WHITE
        )

        screen.blit(
            average,
            (self.width - 180, 10)
        )

        difficulty = self.small_font.render(
            self.difficulty,
            True,
            WHITE
        )

        screen.blit(
            difficulty,
            (10, self.height - 35)
        )

    # ==================================================
    # RESULTS
    # ==================================================

    def _render_results(self, screen):

        screen.fill(DARK_BLUE)

        title = self.big_font.render(
            "Session Complete!",
            True,
            WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    self.width // 2,
                    45
                )
            )
        )

        summary = self.font.render(
            f"{self.difficulty} | Average: "
            f"{self.average_reaction_ms()} ms",
            True,
            WHITE
        )

        screen.blit(
            summary,
            summary.get_rect(
                center=(
                    self.width // 2,
                    90
                )
            )
        )

        y = 135

        for index, reaction in enumerate(
            self.reaction_times,
            start=1
        ):

            row = self.small_font.render(
                f"Round {index}: {reaction} ms",
                True,
                WHITE
            )

            screen.blit(
                row,
                row.get_rect(
                    center=(
                        self.width // 2,
                        y
                    )
                )
            )

            y += 30

        false_start_text = self.small_font.render(
            f"False starts: {self.false_starts}",
            True,
            WHITE
        )

        screen.blit(
            false_start_text,
            false_start_text.get_rect(
                center=(
                    self.width // 2,
                    y + 10
                )
            )
        )

        footer = self.small_font.render(
            "1/Enter/Space = play again   "
            "2/Esc = exit",
            True,
            WHITE
        )

        screen.blit(
            footer,
            footer.get_rect(
                center=(
                    self.width // 2,
                    self.height - 25
                )
            )
        )

