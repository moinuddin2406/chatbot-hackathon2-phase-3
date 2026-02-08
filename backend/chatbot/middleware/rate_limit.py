from fastapi import Request, HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict
import time


class RateLimiter:
    def __init__(self, requests: int = 10, window: int = 60):
        """
        Initialize rate limiter
        :param requests: Number of requests allowed per window
        :param window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.requests_log: Dict[str, list] = defaultdict(list)

    def check_rate_limit(self, identifier: str) -> bool:
        """
        Check if the identifier has exceeded the rate limit
        :param identifier: Identifier for the client (e.g., IP address or user ID)
        :return: True if rate limit is not exceeded, False otherwise
        """
        now = time.time()
        # Clean old requests outside the window
        self.requests_log[identifier] = [
            req_time for req_time in self.requests_log[identifier]
            if now - req_time < self.window
        ]

        # Check if the number of requests is within the limit
        if len(self.requests_log[identifier]) < self.requests:
            # Add current request
            self.requests_log[identifier].append(now)
            return True

        return False


# Global rate limiter instance
rate_limiter = RateLimiter(requests=20, window=60)  # 20 requests per minute


def check_api_rate_limit(request: Request) -> bool:
    """
    Check rate limit for API requests
    Uses IP address as identifier
    """
    # Get client IP address
    client_ip = request.headers.get("X-Forwarded-For")
    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "unknown"

    return rate_limiter.check_rate_limit(client_ip)


def rate_limit_middleware(request: Request):
    """
    Middleware function to enforce rate limiting
    """
    if not check_api_rate_limit(request):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )