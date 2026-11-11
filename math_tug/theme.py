"""Colours of the app."""

from .domain.player import Player

BG = "#10182F"
PANEL = "#202E56"
MUTED = "#8D99BC"
BLUE = "#65B5FF"
PINK = "#FF5D98"
GOLD = "#FFCF69"
GREEN = "#5EE3A1"
RED = "#FF7A7A"

# Each player's colour. Their names and initials are translated (i18n "player.left", ...).
PLAYER_COLORS = {
    Player.LEFT: BLUE,
    Player.RIGHT: PINK,
}
