# BaJA

## Definition

BaJA (BA-ha):
bottle and jinja API

Utilizing python bottle and jinja2 templates, this API ingests and displays docs, currently built to support couchbase


# Dependencies

## python
brew install libcouchbase 
pip install couchbase
pip install bottle lxml jinja2

## couchbase
N1QL needs at least one index on the bucket
    $ /Applications/Couchbase\ Server.app/Contents/Resources/couchbase-core/bin/cbq
    cbq> CREATE PRIMARY INDEX ON default USING GSI;
