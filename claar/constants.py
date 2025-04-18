"""
Collection of constants
"""
from decimal import Decimal

# file sizes

PERCENT = 100
PERCENTAGE = Decimal('0.01')

KB = 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024
EB = TB * 1024

# amounts
THOUSAND = 1000
MILLION = 1_000_000
BILLION = 1_000_000_000
TRILLION = 1_000_000_000_000

# parts
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
SECONDS_PER_HOUR = MINUTES_PER_HOUR * SECONDS_PER_MINUTE

HOURS_PER_DAY = 24
MINUTES_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR
SECONDS_PER_DAY = HOURS_PER_DAY * SECONDS_PER_HOUR

MILLISECONDS_PER_SECOND = 1_000
MILLISECONDS_PER_MINUTE = MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE
MILLISECONDS_PER_QUARTER_HOUR = MILLISECONDS_PER_MINUTE * SECONDS_PER_HOUR // 4
MILLISECONDS_PER_HOUR = MILLISECONDS_PER_MINUTE * MINUTES_PER_HOUR
MILLISECONDS_PER_DAY = MILLISECONDS_PER_HOUR * HOURS_PER_DAY

NANOSECONDS_PER_MILLISECOND = 1_000
NANOSECONDS_PER_SECOND = 1_000_000


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
