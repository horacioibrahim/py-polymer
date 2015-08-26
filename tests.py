import unittest
import os
import time
import json
import argparse
from pyPolymer import Bower, parser, pos_parser, PolymerElement

class GeneralTests(unittest.TestCase):

    def test_pos_parser(self):
        """ tests if json is built correctly
        """
        args = parser.parse_args(['--create', 'ds-new'])
        args_pos = pos_parser(args)
        self.assertIsInstance(args_pos, argparse.Namespace)


class BowerTests(unittest.TestCase):

    def tearDown(self):
        """ Deletes the new custom element folder.
        """
        pass

    def test_json(self):
        args = parser.parse_args()
        args = pos_parser(args)
        # simulate argument from CLI
        args.__dict__['name'] = 'iron-element'
        bower = Bower(bower_json=args.__dict__)
        self.assertIsInstance(bower, Bower)
        data = bower.to_json()
        self.assertIsInstance(data, str)
        data = json.loads(data)
        self.assertIsInstance(data, dict)

    def test_get_bower(self):
        args = parser.parse_args()
        args = pos_parser(args)
        # simulate argument from CLI
        args.__dict__['name'] = 'iron-element'
        bower = Bower(bower_json=args.__dict__)
        self.assertIsInstance(bower.bower, dict)

    def test_setter_bower(self):
        args = parser.parse_args()
        args = pos_parser(args)
        # simulate argument from CLI
        args.__dict__['name'] = 'iron-element'
        bower = Bower(bower_json=args.__dict__)
        data = bower.to_json()
        bower.bower = data # json/string
        self.assertIsInstance(bower.bower, dict)
        self.assertEqual(bower.bower['name'], 'iron-element')

    def test_validate_bower(self):
        b = {"name": "ds-new"}
        bower = Bower(b)
        self.assertIsInstance(bower, Bower)

    def test_invalid_bower(self):
        b = {"withoutName": "ds-new"}
        self.assertRaises(TypeError, Bower, b)


class PolymerElementTests(unittest.TestCase):

    def tearDown(self):
        import shutil

        if self.target_dir:
            shutil.rmtree(self.target_dir)

    def test_create(self):
        """Tests if directory was created.
        """
        args = parser.parse_args(['--create', 'ds-new'])
        args = pos_parser(args)
        el = PolymerElement(args, **args.__dict__)
        el.create()
        self.target_dir = os.path.abspath('.')
        demo_dir = self.target_dir + '/demo'
        test_dir = self.target_dir + '/test'
        self.assertTrue(os.path.exists(self.target_dir))
        self.assertTrue(os.path.exists(demo_dir))
        self.assertTrue(os.path.exists(test_dir))

    #@unittest.skip('skipped for travis')
    def test_create_no_name(self):
        """Tests if directory was created.
        """
        args = parser.parse_args(['--private', False])
        args = pos_parser(args)
        el = PolymerElement(args, **args.__dict__)
        el.create()
        self.target_dir = os.path.abspath('.')
        demo_dir = self.target_dir + '/demo'
        test_dir = self.target_dir + '/test'
        self.assertTrue(os.path.exists(self.target_dir))
        self.assertTrue(os.path.exists(demo_dir))
        self.assertTrue(os.path.exists(test_dir))

if __name__ == '__main__':
    unittest.main()
