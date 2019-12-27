from pack_the_boxes import pack_the_boxes


def test_pack_the_boxes():
    boxes = [v + 1 for v in range(5)] + [v for v in range(7, 12)]
    assert pack_the_boxes(boxes) == 99
