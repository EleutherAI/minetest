Contributions guide
===================

Thank you for your interest in contributing to Minetester! This guide is meant to provide potential contributors with a clear overview 
of how they can participate in the project, adhere to the community standards, and enhance the codebase.
All contributions, no matter how minor, are greatly appreciated.
All contributors are expected to adhere to the project's `Code of Conduct <CODE_OF_CONDUCT.html>`_.

Getting Started
---------------

- `Fork the repository on GitHub <https://github.com/EleutherAI/minetest/fork>`_.

- Clone the repository:

.. code-block:: bash

    git clone https://github.com/your_username/minetest.git

- Follow the `build instructions <../advanced/building_source.html>`_ to build from your fork's source code.
- In addition, you should install development tools and pre-commit:

.. code-block:: bash

    pip install -e .[dev]
    pre-commit install

Making a Contribution
---------------------

- Look through the `GitHub Issues <https://github.com/EleutherAI/minetest/issues>`_ to find one you are interested in addressing. You're also free to create your own issue if you identify a bug or enhancement that hasn't been raised yet.

- Create a new branch with a somewhat informative name of what you are doing.

.. code-block:: bash

    git checkout -b your_branch_name

- Develop your bug fix or feature and write tests if possible.

- Commit your changes:

.. code-block:: bash

    git commit -m "Brief description of changes"

- Push your changes to your fork.

.. code-block:: bash

    git push origin your_branch_name

- Open a pull request in the original repository. Please fill in the pull request template and reference the issue you're addressing. Feel free to request a review from one of the maintainers.
