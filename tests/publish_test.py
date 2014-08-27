from .. import publish
import argparse

def test_known_args():
    publish.main(['--twitter'])

def test_unknown_args():
    publish.main(['--something'])

def test_no_args():
    publish.main([])
