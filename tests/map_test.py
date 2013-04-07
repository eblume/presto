"Tests for presto.map"

import unittest as ut

from presto.map.system import System

class TestMap(ut.TestCase):

    def test_map(self):
        "Quick test on some map data."
        stacmon = System.by_name("Stacmon")
        self.assertTrue(stacmon)
        self.assertEqual(len(list(stacmon.neighbors())), 5)
        self.assertTrue("Ostingele" in {n.name for n in stacmon.neighbors()})
        self.assertEqual(stacmon.region.name, "Placid")
        self.assertEqual(stacmon.constellation.name, "Fislipesnes")


if __name__ == '__main__':
    unittest.main()
