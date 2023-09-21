from estate_bot.main import last_msg_id


def test_isdigit_num():
    msg_id = last_msg_id()
    assert msg_id > 1
