"Tests for presto.map"

import unittest as ut

from presto.map import System, Constellation, Region

class TestMap(ut.TestCase):

    def test_map(self):
        "Basic map data functionality test"
        stacmon = System.by_name("Stacmon")
        self.assertTrue(stacmon)
        self.assertEqual(len(list(stacmon.neighbors())), 5)
        self.assertTrue("Ostingele" in {n.name for n in stacmon.neighbors()})
        self.assertEqual(stacmon.region.name, "Placid")
        self.assertEqual(stacmon.constellation.name, "Fislipesnes")
        fislipesnes = Constellation.by_name("Fislipesnes")
        placid = Region.by_name("Placid")
        self.assertEqual(fislipesnes, stacmon.constellation)
        self.assertEqual(placid, stacmon.region)
        self.assertEqual(len(stacmon.region.systems), 71)


if __name__ == '__main__':
    unittest.main()
