from __future__ import annotations

import uuid


def generate_demo_user_id() -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo@aicodevisualizer.local"))
