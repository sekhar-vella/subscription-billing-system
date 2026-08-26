from fastapi import HTTPException


ALLOWED_TRANSITIONS = {
    "trial": {"active", "cancelled"},
    "active": {"past_due", "cancelled"},
    "past_due": {"active", "cancelled"},
    "cancelled": set(),
}


def validate_status_transition(
    current_status: str,
    new_status: str
):
    allowed_states = ALLOWED_TRANSITIONS.get(current_status)

    if allowed_states is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid current status: {current_status}"
        )

    if new_status not in ALLOWED_TRANSITIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid new status: {new_status}"
        )

    if new_status not in allowed_states:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid transition: "
                f"{current_status} -> {new_status}"
            )
        )

    return True