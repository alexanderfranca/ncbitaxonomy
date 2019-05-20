# -*- coding: utf-8 -*-

import pprint

from ncbitaxonomy.ncbitaxonomy import *

tax = NCBITaxonomy(
        nodes_file='./tests/fixtures/nodes1.dmp',
        names_file='./tests/fixtures/names1.dmp',
        )

tax.load_taxonomy()

data = tax.taxonomy_by_tax_id( 9606 )

pprint.pprint(data)


