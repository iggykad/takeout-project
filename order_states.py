allowed = {

    "placed": ["received"],
    "received": ["in_process"],
    "in_process": ["almost_ready"],
    "almost_ready": ["ready"],
    "ready": ["out_for_delivery", "picked_up"],
    "out_for_delivery": ["delivered"],
    "delivered": [],
    "picked_up": [],
}

def can_move (current, new):
    return new in allowed[current]
print(can_move("placed", "received"))
print (can_move("placed", "ready"))