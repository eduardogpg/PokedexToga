python -m helloworld vs python helloworld.py

Note the -m flag and absence of the .py extension in this command line. If you run python helloworld.py, you may see some errors like:

NotImplementedError: Application does not define open_document()
Toga apps must be executed as modules - hence the -m flag.
