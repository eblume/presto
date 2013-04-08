"Tests for presto.items"

import unittest as ut

from presto.items import Type, Group, Category, MarketGroup

class TestItems(ut.TestCase):

    def test_types(self):
        "Basic item/type functionality test"
        dc = Type.by_name("Damage Control I")
        group = dc.group
        category = dc.group.category
        marketcat = dc.marketgroup

        self.assertEqual(dc.name, "Damage Control I")
        self.assertEqual(group.name, "Damage Control")
        self.assertEqual(category.name, "Module")

        market_cats = []
        while True:
            market_cats.append(marketcat)
            marketcat = marketcat.parentgroup
            if not marketcat:
                break

        marketcat = market_cats[0]  # Reset

        self.assertEqual(len(market_cats), 3)
        self.assertEqual(market_cats[0].name, "Damage Controls")
        self.assertEqual(market_cats[1].name, "Hull & Armor")
        self.assertEqual(market_cats[2].name, "Ship Equipment")

        group_neighbors = group.types
        market_neighbors = marketcat.types
        self.assertTrue("Internal Force Field Array I" in 
                        {x.name for x in group_neighbors})
        self.assertEqual(len(group_neighbors), 14)
        self.assertEqual(len(market_neighbors), 13)

        for i in range(min(len(group_neighbors), len(market_neighbors))):
            self.assertEqual(group_neighbors[i].name, market_neighbors[i].name)

        self.assertEqual(group_neighbors[i+1].name, "Civilian Damage Control")
        self.assertTrue("Civilian Damage Control" not in 
                        {x.name for x in market_neighbors})

