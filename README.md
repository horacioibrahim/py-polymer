# py-polymer

[![Build Status](https://travis-ci.org/horacioibrahim/py-polymer.svg?branch=master)](https://travis-ci.org/horacioibrahim/py-polymer)

A manager that quickly creates an easy way custom element with Polymer. The
elements are based in the seed-element created by @addyosmani in
[seed-element](https://github.com/polymerelements/seed-element).

## Quick usage

git clone https://github.com/horacioibrahim/py-polymer.git
python pyPolymer.py --create iron-myElement -I bower_components/

Now the iron-myElement is placed in bower_components/

## Usage with config.json
The config.json help us for NOT have that to pass authors, mail address, prefix,
license, etc. all times.

## Add your env PATH
vim ~/.bashrc (or bash_profile)
alias pyPolymer="FOLDER_WHERE_CLONED/py-polymer/pyPolymer.py"

## License

py-polymer is available under the [MIT license](http://opensource.org/licenses/MIT).
