#!/usr/bin/env python3
"""Convenient repository entry point; the distributable Skill owns the implementation."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parent / 'skills/organize-search-documents/scripts/docflow.py'), run_name='__main__')
