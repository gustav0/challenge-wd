import urllib.parse
from typing import Dict, Optional


class ConnectionURL:

    def __init__(
        self,
        scheme: str,
        host: str,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        path: Optional[str] = None,
        query: Optional[Dict[str, str]] = None,
    ):
        """
        Initializes the connection URL with its components.
        """
        self.scheme = scheme
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path
        self.query = query or {}

    def __str__(self) -> str:
        # Build the netloc: "username:password@host:port"
        netloc = ""
        if self.username:
            netloc += self.username
        if self.password:
            netloc += f":{self.password}"

        if self.username or self.password:
            netloc += "@"
        netloc += self.host

        if self.port:
            netloc += f":{self.port}"

        # Build query string if any
        query_str = urllib.parse.urlencode(self.query)

        # Use urllib.parse.urlunparse to combine parts
        return urllib.parse.urlunparse(
            (
                self.scheme,
                netloc,
                self.path or "",
                "",
                query_str,
                "",
            )
        )

    def as_string(self) -> str:
        return str(self)
