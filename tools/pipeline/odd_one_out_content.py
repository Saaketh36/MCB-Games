"""
Authored content for the Odd One Out activities.

An odd-one-out question shows four pictures and asks the student to tap the one
that does not belong. Each set below names its four pictograms, the index of
the odd one, and the reason, so the answer is grounded in a real shared
property rather than being arbitrary.

The two Odd One Out activities in the curriculum are:
  Class I    Mathematics - Odd One Out Zoo       (Shapes & Spatial Understanding)
  Class III  EVS         - My Neighbourhood Explorer (Observation & Identification)
"""

ODD_ONE_OUT = {
    "Odd One Out Zoo": [
        {
            "set_id": "zoo-mammals",
            "prompt": "Three of these animals walk on four legs. Tap the odd one out.",
            "items": ["lion", "tiger", "cow", "eagle"],
            "odd": 3,
            "reason": "A lion, a tiger and a cow are mammals that walk on four legs. "
                      "An eagle is a bird with two legs and wings, so it does not belong.",
        },
        {
            "set_id": "zoo-sound",
            "prompt": "Three of these animals make a low animal sound. Tap the odd one out.",
            "items": ["lion", "cow", "tiger", "eagle"],
            "odd": 3,
            "reason": "A lion, a cow and a tiger are mammals. An eagle is a bird, "
                      "so it does not belong with them.",
        },
        {
            "set_id": "zoo-pets",
            "prompt": "Three of these animals are pets that live with people. Tap the odd one out.",
            "items": ["cow", "tiger", "lion", "eagle"],
            "odd": 3,
            "reason": "A cow is a farm animal, and a lion and a tiger are wild animals. "
                      "An eagle is a bird that flies and nests in trees, so it does not belong.",
        },
    ],
    "My Neighbourhood Explorer": [
        {
            "set_id": "hood-vehicles",
            "prompt": "Three of these help people travel from one place to another. "
                      "Tap the odd one out.",
            "items": ["bus", "train", "bicycle", "shop"],
            "odd": 3,
            "reason": "A bus, a train and a bicycle are vehicles used for travel. "
                      "A shop is a place where we buy things, so it does not belong.",
        },
        {
            "set_id": "hood-places",
            "prompt": "Three of these are places you go to for a service. Tap the odd one out.",
            "items": ["school", "hospital", "shop", "tree"],
            "odd": 3,
            "reason": "A school, a hospital and a shop are buildings we visit. "
                      "A tree is a living plant, so it does not belong.",
        },
        {
            "set_id": "hood-living",
            "prompt": "Three of these are living things that grow. Tap the odd one out.",
            "items": ["tree", "flower", "grass", "train"],
            "odd": 3,
            "reason": "A tree, a flower and grass are living plants that grow. "
                      "A train is a machine and does not grow, so it does not belong.",
        },
    ],
}


def sets_for(activity_name):
    """Authored sets for one activity, or an empty list."""
    return ODD_ONE_OUT.get(activity_name, [])