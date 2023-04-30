import re

SEAT_REGEX = r"^([0-9]+)([A-Z]+)&([A-Z]+)([0-9]+)\+([0-9]+)$"
SEAT_REGEX_WITHOUT_STATUS = r"^([A-Z]+)&([A-Z]+)([0-9]+)\+([0-9]+)$"


def test_seat_details(seat: str, re_status=True):
    # {STATUS_CODE}{GRP_CODE}{&}{ROW}{COL}+SEAT_NO

    seat_details = None
    if re_status:
        seat_details = re.search(SEAT_REGEX, seat)
    else:
        seat_details = re.search(SEAT_REGEX_WITHOUT_STATUS, seat)
    if seat_details:
        if re_status:
            seat_status, seat_grp, row, col, seat_num = seat_details.groups()
            return {
                "seat_status": seat_status,
                "seat_grp": seat_grp,
                "row": row,
                "col": col,
                "seat_num": int(seat_num),
            }

        seat_grp, row, col, seat_num = seat_details.groups()
        return {
            "seat_grp": seat_grp,
            "row": row,
            "col": col,
            "seat_num": int(seat_num),
        }
    return None


def create_seat(status_code, grp_code, row, col, seat_num):
    return f"{status_code}{grp_code}&{row}{col}+{seat_num}"


def get_seat_details(seat: str, re_status=True):
    seat_details = test_seat_details(seat, re_status=re_status)
    if seat_details is None:
        raise ValueError(f"Seat {seat} regex pattern matching failed")
    return seat_details


def get_grp_details(grp: str):
    # {GRP_NAME}:{GRP_CODE}:{COST}:{GRP_ORDER}:{CURRENCY}:N
    grp_details = re.search(
        "^([A-Z]+_*[A-Z]+):([A-Z]+):([\d]+):([A-Z]+):([\d]+):N", grp
    )
    if grp_details:
        grp_name, grp_code, cost, grp_order, currency = grp_details.groups()
        return {
            "grp_name": grp_name,
            "grp_code": grp_code,
            "cost": int(cost),
            "grp_order": grp_order,
            "currency": currency,
        }
    raise ValueError("Group regex pattern matching failed")


def get_layout_details(layout: str):
    grp_details, seating_layout = layout.split("||")
    grps = [get_grp_details(grp) for grp in grp_details.split("|")]
    return {"grp_details": grps, "seating_layout": seating_layout}
