import random
import pygame


class Round:
    def __init__(self, min_wait_ms=1000, max_wait_ms=3000):
        self.wait_delay_ms = random.randint(min_wait_ms, max_wait_ms)

        # waiting -> go -> result
        # false_start is used when the player reacts too early.
        self.state = "waiting"

        self.start_time = pygame.time.get_ticks()
        self.go_time = None
        self.reaction_ms = None

    def update(self):
        if self.state == "waiting":
            now = pygame.time.get_ticks()

            if now - self.start_time >= self.wait_delay_ms:
                self.state = "go"

                # IMPORTANT:
                # This is the exact moment the screen changes to green.
                self.go_time = now

    def register_input(self):
        """
        Handle a click or Space press.

        Returns:
            reaction time in milliseconds if the player reacted
            after GO.

            None if the player reacted too early.
        """

        # Player clicked while the screen was still grey.
        if self.state == "waiting":
            self.state = "false_start"
            self.reaction_ms = None
            return None

        # Ignore input if the round is already over.
        if self.state != "go" or self.go_time is None:
            return None

        # Valid reaction.
        now = pygame.time.get_ticks()

        # Measure from GO, NOT from the beginning of the round.
        self.reaction_ms = now - self.go_time

        self.state = "result"

        return self.reaction_ms

