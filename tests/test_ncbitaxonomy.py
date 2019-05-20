import sys
import os
import pprint
import unittest
from ncbitaxonomy.ncbitaxonomy import *
import re


class TestNCBITaxonomy( unittest.TestCase ):

    def setUp( self ):
        self.tax = NCBITaxonomy(
                            nodes_file='./tests/fixtures/nodes1.dmp',
                            names_file='./tests/fixtures/names1.dmp',
                            )

    def test_load_taxonomy( self ):

        self.tax.load_taxonomy()

        self.assertTrue( len( self.tax.names ) > 1 )
        self.assertTrue( len( self.tax.nodes ) > 1 )

    def test_invalid_taxonomy_by_tax_id( self ):

        tax = self.tax.taxonomy_by_tax_id( 666666 )

        self.assertTrue( type( tax ) is dict )
        self.assertTrue( len( tax ) == 0 )

    def test_taxonomy_by_tax_id( self ):

        tax = self.tax.taxonomy_by_tax_id( 9606 )

        self.assertTrue( type( tax ) is dict )
        self.assertEqual( tax['name'], 'Homo sapiens' )



if __name__ == "__main__":
    unittest.main()
