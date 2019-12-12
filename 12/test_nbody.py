from nbody import Point3D, Particle


def test_point3d():
    t = Point3D(3, 4, 5)
    assert t.x == 3
    assert t.y == 4
    assert t.z == 5


def test_particle():
    t = Particle()
    assert t.point.x == 0
    assert t.point.y == 0
    assert t.point.z == 0
    assert t.velocity.x == 0
    assert t.velocity.y == 0
    assert t.velocity.z == 0
    t = Particle(Point3D(3, 4, 5))
    assert t.point.x == 3
    assert t.point.y == 4
    assert t.point.z == 5
    assert t.velocity.x == 0
    assert t.velocity.y == 0
    assert t.velocity.z == 0
