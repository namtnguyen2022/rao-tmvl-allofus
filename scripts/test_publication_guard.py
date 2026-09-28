"""Small synthetic checks for the publication guard; no study data are used."""
import json
import unittest

from check_repository import check_file


class PublicationGuardTests(unittest.TestCase):
    def notebook(self, outputs=None, execution_count=None):
        return json.dumps({'metadata': {'kernelspec': {'language': 'python'}}, 'cells': [
            {'cell_type': 'code', 'source': ['x = 1'], 'metadata': {},
             'outputs': outputs or [], 'execution_count': execution_count}]}).encode()

    def test_clean_notebook(self):
        self.assertFalse(check_file('analysis.ipynb', self.notebook()))

    def test_saved_outputs_rejected(self):
        self.assertTrue(check_file('analysis.ipynb', self.notebook([{'output_type': 'stream', 'text': 'example'}])))

    def test_execution_count_rejected(self):
        self.assertTrue(check_file('analysis.ipynb', self.notebook(execution_count=1)))

    def test_data_file_rejected(self):
        self.assertTrue(check_file('results/example.csv', b'example\n'))

    def test_counts_in_definitions_rejected(self):
        self.assertTrue(check_file('definitions/procedure_concepts.csv', b'concept_id,people\n1,2\n'))

    def test_private_key_rejected(self):
        payload = ('-----BEGIN ' + 'PRIVATE KEY-----').encode()
        self.assertTrue(check_file('example.txt', payload))


if __name__ == '__main__':
    unittest.main()
