"""Root-level compatibility shim — re-exports backend.models."""
from backend.models import *  # noqa: F401,F403
from backend.models import db  # noqa: F401
