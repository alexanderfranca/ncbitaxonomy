
class NCBITaxonomy:
    """
    Process the nodes.dmp and names.dmp NCBI files and create the full taxonomy data for a organism.

    Attributes:
        nodes_file(file): File handle that represents the nodes.dmp file.
        names_fIle(file): File handle that represents the names.dmp file.
        nodes(dict): Dictionary format for the nodes.dmp file.
        names(dict): Dictionary format for the names.dmp file.
        name(str): String from the names dictionary/names.dmp file.
        lineage(list): Full taxonomy list for the organism.
    """

    def __init__(self, nodes_file, names_file):

        self.nodes_file = nodes_file
        self.names_file = names_file

        self.nodes = {}
        self.names = {}

        self.name = None
        self.lineage = []

    def load_taxonomy(self):
        """
        Load the names and nodes NCBI files and generate two dictionaries (self.names and self.nodes).
        """

        with open(self.nodes_file) as nodes:
            for node in nodes:
                records = node.split('|')
                query = records[0].replace('\t', '')
                parent = records[1].replace('\t', '')
                tax_type = records[2].replace('\t', '')

                self.nodes[query] = {'parent': parent, 'tax_type': tax_type}

        with open(self.names_file) as names:
            for name in names:
                records = name.split('|')
                query_id = records[0].replace('\t', '')
                query_name = records[1].replace('\t', '')
                query_type = records[3].replace('\t', '')

                if query_type == 'scientific name':
                    self.names[query_id] = query_name

    def taxonomy_by_tax_id(self, tax_id=None):
        """
        Return NCBI taxonomy by taxonomy id (Ex: 9606, 1453, etc)

        Args:
            tax_id(str): NCBI taxonomy id.

        Returns:
            (dict): Full taxonomy dictionary.
        """

        # Load the taxonomy files in case it wasn't before.
        if len(self.names) == 0 or len(self.nodes) == 0:
            self.load_taxonomy()

        tax_id = str(tax_id)

        tax = []
        taxonomy = []
        organism = {}

        # Skip if the taxonomy id doesn't exist in the NCBI
        if tax_id not in self.nodes:
            return {}

        tax.append({'tax_id': tax_id,
                    'tax_type': self.nodes[tax_id]['tax_type'],
                    'parent': self.nodes[tax_id]['parent']})
        point = self.nodes[tax_id]['parent']
        tax.append({'tax_id': point,
                    'tax_type': self.nodes[point]['tax_type'],
                    'parent': self.nodes[point]['parent']})

        organism['name'] = self.names[str(tax_id)]

        self.name = self.names[str(tax_id)]

        while True:
            point = self.nodes[point]['parent']

            data = {
                'tax_id': point,
                'tax_type': self.nodes[point]['tax_type'],
                'parent': self.nodes[point]['parent']}
            tax.append(data)

            if point == str(1):
                break

        for tax_id in tax:
            if not self.names[tax_id['parent']] == 'root':
                taxonomy.append({'tax_id': tax_id['tax_id'],
                                 'type': tax_id['tax_type'],
                                 'name': self.names[tax_id['tax_id']]})

        self.lineage = taxonomy

        organism['taxonomy'] = taxonomy

        return organism
