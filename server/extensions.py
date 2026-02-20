"""
File contains “global objects” that both app.py and routes.py can import without importing each other.
Before:
    - app.py needed auth/routes.py (to register routes)
    - auth/reoutes.py needed app.py (to get limiter)
Python tries to import app.py, but it can’t finish because it has to import routes.py, which tries to import 
app.py again while it’s only half-built. That’s where “partially initialized objects” happen.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# establish a rate limiter to prevent brute force attacks
limiter = Limiter(key_func=get_remote_address, default_limits=[])
