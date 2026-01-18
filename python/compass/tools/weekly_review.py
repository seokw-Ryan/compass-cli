"""Weekly review tool."""

from typing import Dict, Any
from datetime import datetime, timedelta


class WeeklyReview:
    """Facilitate weekly reviews (stub)."""

    def generate_review(self) -> Dict[str, Any]:
        """Generate weekly review prompts."""
        today = datetime.now()
        week_start = today - timedelta(days=7)

        return {
            "week_start": week_start.isoformat(),
            "week_end": today.isoformat(),
            "prompts": [
                "What did I accomplish this week?",
                "What challenges did I face?",
                "What did I learn?",
                "What are my priorities for next week?",
            ],
        }
