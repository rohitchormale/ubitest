"""
Base config for different environments like test/dev/prod.
This config will be overridden by `instance/config.py`
"""

DEBUG = False
SITE_TITLE = "ubitest"

# fpc service configurations
FP_CREDIT_DURATION_HOURS = 0
FP_CREDIT_DURATION_MINS = 3
FP_CREDIT_POINTS = 50
FP_CREDIT_MAX_POINTS = 200