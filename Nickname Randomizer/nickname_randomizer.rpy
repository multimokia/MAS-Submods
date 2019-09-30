init 999 python:
    config.label_overrides["post_pick_random_topic"] = "post_pick_random_topic_override"

init python:
    nick_list = [
        "Darling",
        "Sweetheart",
        "Honey",
        "Love",
        "Angel",
        "Sweetie",
        "Monika",
    ]

    player_nick_list = [
        "honey",
        "sweetie",
        "sweetheart",
        persistent.playername,
    ]


label post_pick_random_topic_override:
    $ _return = None
    $ m_name = renpy.random.choice(nick_list)
    $ player = renpy.random.choice(nick_list)
    jump ch30_loop