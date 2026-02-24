# import sys
# import os
# import structlog
# import logging

# # Ensure src is on path when run directly
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# from mcp_mssql.config import settings
# from mcp_mssql.tools.query_tools import mcp

# structlog.configure(
#     wrapper_class=structlog.make_filtering_bound_logger(
#         getattr(logging, settings.LOG_LEVEL)
#     )
# )

# log = structlog.get_logger(__name__)

# def main():
#     log.info("mcp.server.starting")
#     mcp.run(transport="stdio")

# if __name__ == "__main__":
#     main()

import sys
import os
import logging
import structlog

# ── Redirect ALL output to stderr ─────────────────────────────
# Claude Desktop stdio transport uses stdout for JSON-RPC.
# SSE/HTTP transport uses the network — stderr is always safe.
# Never print to stdout from application code.

def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Standard library logging → stderr
    logging.basicConfig(
        stream=sys.stderr,
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),   # ← no file= parameter
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level, logging.INFO)
        ),
        # PrintLoggerFactory(file=sys.stderr) routes all output to stderr
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),  # ← stderr here
    )

configure_logging()

from mcp_mssql.config import settings
from mcp_mssql.tools.query_tools import mcp

log = structlog.get_logger(__name__)


def main():
    transport = os.getenv("TRANSPORT", "stdio")
    host      = os.getenv("HOST", "0.0.0.0")
    port      = int(os.getenv("PORT", "8000"))

    log.info(
        "mcp.server.starting",
        transport=transport,
        host=host,
        port=port,
        database=settings.MSSQL_DATABASE,
        server=settings.MSSQL_SERVER,
    )

    if transport == "stdio":
        # Used by Claude Desktop direct process connection
        mcp.run(transport="stdio")

    elif transport == "sse":
        # Used by Docker / remote connections
        # Claude Desktop connects via HTTP to http://localhost:8000/sse
        mcp.run(
            transport="sse",
            host=host,
            port=port,
        )
    else:
        log.error("mcp.server.unknown_transport", transport=transport)
        sys.exit(1)


if __name__ == "__main__":
    main()