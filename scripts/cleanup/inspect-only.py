#!/usr/bin/env python3
"""Discovery only: app-managed locations have no blanket deletion command."""
import sys
from cleanup import main

if __name__ == "__main__":
    if "execute" in sys.argv:
        raise SystemExit("Inspection-only locations cannot be deleted by this adapter.")
    main()
