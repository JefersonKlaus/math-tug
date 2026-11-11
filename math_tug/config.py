"""Game rules and the number ranges used for problems."""

# A player wins by getting this many points ahead of the other (with 3: 3-0, 5-2, 10-7...).
WIN_LEAD = 3
WIN_LEAD_CHOICES = (3, 5, 7, 10)
OPTION_COUNT = 3

# Number ranges (inclusive) for generated problems
ADD_RANGE = (10, 50)
SUB_RANGE = (10, 99)

# Multiplication tables used by × and ÷: "7 × 8" and "56 ÷ 7" come from the 7 table.
TABLE_CHOICES = tuple(range(1, 11))
TIMES_RANGE = (1, 10)
