#!/usr/bin/env python
# -*- coding: utf-8 -*-
# manage.py is A manager that quickly creates an easy way custom element with
# Polymer. The elements are based in the seed-element created
# by @addyosmani in https://github.com/polymerelements/seed-element
#
# Tasks:
# ======
# Creates a new element is based in the https://github.com/polymerelements/seed-element
#
# Rules:
# ------
# bower.json (https://github.com/bower/bower.json-spec)
# description: 140 characters
# version: is deprecated. Use version manager tags.
# main: string or array of string. List of package necessary to use your package.
#
# Environment variable:
# ---------------------
# Use PYPOLYMER_CONFIG to set the folder of the your config.ini files. Default
# is config.ini.
#
# TODO: updates info to existent element.
#

import argparse
import json
import os
import urllib2
import sys

parser = argparse.ArgumentParser(description='Task manager')
parser.add_argument('--create', '-c', dest='name', type=str,
            help='Creates new custom element.')
parser.add_argument('--install_dir', '-I', dest='destination_path', type=str,
            help='Place where will install the folder.')
# Metadata: description, author name, author e-mail, username's github.
parser.add_argument('--description', '-d', type=str,
            default='This element X solve the problem Y.',
            help='Description of new custom element.')
parser.add_argument('--author-name', '-n', dest='author',
            type=str, help='Author name.')
parser.add_argument('--author-mail', '-m', dest='mail',
            type=str, help='Author e-mail address.')
# Add package necessary to use our element into bower.json.
parser.add_argument('--add-main', '-a', dest='main', nargs='*',
            help='Creates new custom element.')
parser.add_argument('--license', '-l', dest='license',
            help='Link of the license for new element.')
parser.add_argument('--ignore', '-i', dest='ignore', nargs='*',
            help='Ignored files for Bower to ignore when instaling.')
parser.add_argument('--keywords', '-k', nargs='*',
            help='Used for search by keyword.')
parser.add_argument('--homepage', '-w',
            help='URL to learn more about the package.')
parser.add_argument('--private', '-p', type=bool, default=False,
            help='If set to true, Bower will refuse to publish it.')
parser.add_argument('--repository', '-r', type=dict,
            help='Repository type and url.')
parser.add_argument('--dependencies', '-s', type=dict,
            help='Key/value with dependencies.')
parser.add_argument('--devDependencies', '-e', type=dict,
            help='Key/value with dependencies for developers.')

# For updates. Use the options `--create` with `filename` is no sense.
# parser.add_argument('filename', help='Path of the custom element existent.')

# BOWER SPEC
# See more: https://github.com/bower/bower.json-spec
BOWER = {
    'name': {
        'required': True,
        'type': str
    },
    'description': {
        'required': False,
        'type': str
    },
    'version': { # This is deprecated
        'required': False
    },
    'main': {
        'required': False,
        'type': list
    },
    'moduleType': {
        'required': False,
        'type': list
    },
    'license': {
        # This is can be identifier (https://spdx.org/licenses/) or url.
        'required': False,
        'type': str
    },
    'ignore': {
        'required': False,
        'type': list
    },
    'keywords': {
        'required': False,
        'type': list
    },
    'authors': {
        'required': False,
        'type': list
    },
    'homepage': {
        'required': False,
        'type': str
    },
    'repository': {
        'required': False,
        'type': dict
    },
    'dependencies': {
        'required': False,
        'type': dict
    },
    'devDependencies': {
        'required': False,
        'type': dict
    },
    'resolutions': {
        'required': False,
        'type': dict
    },
    'private': {
        'required': False,
        'type': bool
    },
}


def __read_json_file(path_file):
    """Retuns a dictionary after read the content from json file found in
    path_file.

    @param path_file: where the file is placed.
    """
    try:
        fp = open(path_file, 'r')
        data = fp.read()
    except IOError, e:
        content = urllib2.urlopen('https://raw.githubusercontent.com/horacioibrahim/py-polymer/master/config.json')
        data = content.read()

    return json.loads(data)

def __mixed_config(args):
    """ Mixs config.json file with argument from command line. The command line
    overrides the configuration.

    @param args: Namespace from parser.parse_args()
    """
    # loadgin config file
    config_file = os.environ.get('PYPOLYMER_CONFIG', None)
    if config_file is None:
        config_file = 'config.json' # Default is config.josn

    config = __read_json_file(config_file)
    # Author
    authors = config.get('authors') # returns a list
    # Element
    element = config.get('element')
    destination_path = element.get('targer_dir')
    prefix = element.get('prefix')
    # Bower
    bower = config.get('bower')
    description = bower.get('description')
    main = bower.get('main')
    license = bower.get('license')
    ignore = bower.get('ignore')
    keywords = bower.get('keywords')
    homepage = bower.get('homepage')
    private = bower.get('private')
    repository = bower.get('repository')
    dependencies = bower.get('dependencies')
    devDependencies = bower.get('devDependencies')

    # Loop in all local variable this function and check if already exists in
    # args. Case YES the user passed by command line so this not can changed.
    # case NO (or None) to add default values from config.json.
    for k, v in locals().items():
        # if k in args.__dict__ is True is because it was defined in .add_argument.
        if k in args.__dict__ and args.__dict__[k] == None:
            # The user could define a value as '' in the config.json
            # to keep the format. This is guarantee that only arguments not
            # provided in command line are modified.
            if v != '':
                args.__dict__[k] = v

    # authors is an exception because it isn't defined as argument by
    # add_argument.
    if 'authors' not in args.__dict__:
        args.__dict__['authors'] = authors

    return args

def pos_parser(args):
    """This makes two basic taks:

        1)  returns the `args Namespace` of the source `parser.parse_args()`
        where the __dict__ is modified with default values based on config.json.
        This task works as autocomplete for the values not provided by user.

        2) Evaluates if `author` and `mail` address was passed in command line and
        concatenates both within list `authors` removing `author` and
        `mail` of the args Namespace.

    @param args: args after ran parser.parse_args()
    @type args: Namespace
    """
    args = __mixed_config(args)

    if ('author' in args and 'mail' in args) and \
        (args.author is not None and args.mail is not None):
        args.__dict__['authors'].append('{author} <{email}>'.format(
                author=args.author, email=args.mail))
        del args.__dict__['author']
        del args.__dict__['mail']

    return args

class Bower(object):

    def __init__(self, bower_json, **kwargs):
        self.bower = bower_json

    def to_json(self):
        return json.dumps(self.bower)

    @property
    def bower(self):
        return self._bower

    @bower.setter
    def bower(self, value):
        """ Sets bower attribute. """
        loaded_json = self._validate(value)
        self._bower = loaded_json

    @bower.deleter
    def bower(self):
        del self._bower

    def _validate(self, value):
        """Validates if json or dict was passed as a valid bower.json.
        """

        if isinstance(value, dict):
            loaded_json = value
        else:
            loaded_json = json.loads(value)

        # Valdations
        for field, rules in BOWER.items():
            # required fields
            if 'required' in rules and rules['required'] is True:
                if field not in loaded_json:
                    raise TypeError('%s is required in bower.json specs' % field)
            # validation for types...
            # cleanup when None
            for f, value in loaded_json.items():
                if value is None:
                    del loaded_json[f]

            if field in loaded_json and rules['type'] == str:
                if type(loaded_json[field]) is unicode:
                    loaded_json[field] = str(loaded_json[field])

            if field in loaded_json and not isinstance(loaded_json[field], rules['type']):
                raise TypeError('%s must be of the type %s' % (field, rules['type']))

        return loaded_json


class PolymerElement(object):
    """
    Manager to make tasks on polymer element.
    """

    # Links for externals resources. If a value of a key is dict it's (key) a
    # directory rather is file.
    external_links = {
        'index': 'https://raw.githubusercontent.com/PolymerElements/seed-element/master/index.html',
        'seed_element': 'https://raw.githubusercontent.com/PolymerElements/seed-element/master/seed-element.html',
        'readme': 'https://raw.githubusercontent.com/PolymerElements/seed-element/master/README.md',
        'hero': 'https://raw.githubusercontent.com/PolymerElements/seed-element/master/hero.svg',
        'demo': { # This is directory
            'index': 'https://raw.githubusercontent.com/PolymerElements/seed-element/master/demo/index.html'
        },
        'test': { # This is directory
            'index': 'https://raw.githubusercontent.com/PolymerElements/seed-element/master/test/index.html',
            'basic_test': 'https://raw.githubusercontent.com/PolymerElements/seed-element/master/test/basic-test.html'
        }
    }

    def __str__(self):
        return self.name

    def __init__(self, **kwargs):
        name = kwargs.get('name', None)
        if name is None:
            name = raw_input("Type a name for new element [new-element]:")
            if name == '':
                name = 'new-element'

        self.name = name

        # Set Place
        path = kwargs.get('destination_path', '_build')
        self.destination_path = os.path.abspath(path)

    def create(self):
        """ Creates a directory of the new element.
        """
        # create the dir element
        os.mkdir(self._destination)
        # change for other dir
        os.chdir(self._destination)
        # get and create files
        contents_copied = self._get_external_resources()

        for item, content in contents_copied.items():
            filename = item
            # create file or folder. If filename contain a directory
            # the variable folder will be a list with at least 2 elements.
            folder = filename.split('/')
            # only one level is predicted
            if isinstance(folder, list) and len(folder) == 2:
                filename = folder[1]
                folder = folder[0]
                if not os.path.exists(folder):
                    os.mkdir(folder) # if not exists create it.
                os.chdir(folder)

            fp = open(filename, 'w')
            content = content.replace('seed-element', self.name)
            fp.write(content)
            fp.close()
            os.chdir(self._destination)

        print "New custom element create with successful %s" % (self._destination)

    @property
    def _validate_name(self):
        """ Validates if name is correct.
        """
        if '-' in self.name and (not self.name.startswith('-') and not self.name.endswith('-')):
            return self.name
        raise TypeError('The character `-` is required in the element name.')

    @property
    def _destination(self):
        """ Creates the destination folder based new element name.
        """
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)

        return '/'.join([self.destination_path, self._validate_name])

    def _get_external_resources(self):
        """ Gets the content from remote resources for create our local files.
        """
        content = {}
        element = self._validate_name + '.html'
        element_files = {
            'root': { # the root directory
                'index.html': self.external_links['index'],
                element: self.external_links['seed_element'], # seed-element
                'README.md': self.external_links['readme'],
                'hero.svg': self.external_links['hero']
            },
            'subdir': { # and subdirectories
                'demo': {
                    'index.html': self.external_links['demo']['index'],
                },
                'test': {
                    'index.html': self.external_links['test']['index'],
                    'basic-test.html': self.external_links['test']['basic_test']
                }
            }
        }
        # for all files in the root
        print "Please waiting resources externals on remote host..."
        for k, v in element_files['root'].items():
            # create file
            content[k] = urllib2.urlopen(v).read()
            print '[Done] %s' % v
        # for all sub objects
        for subdir, dict_files in element_files['subdir'].items():
            # folder loop
            for filename, link_external in dict_files.items():
                print '[Done] %s' % link_external
                content['/'.join([subdir, filename])] = urllib2.urlopen(link_external).read()

        return content


if __name__ == '__main__':
    args = parser.parse_args()
    args = pos_parser(args)
    el = PolymerElement(**args.__dict__)
    el.create()
