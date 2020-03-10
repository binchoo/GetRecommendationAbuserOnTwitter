#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import multiprocessing, subprocess

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweetsearch.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def start_crawler() :
        subprocess.run(["python", "./DirectiveMerger/main.py"])

if __name__ == '__main__':
    crawler_process = multiprocessing.Process(name='crawler_process', target=start_crawler)
    crawler_process.start()
    main()
