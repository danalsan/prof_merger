########################################
prof_merger
########################################

prof_merger is a tiny tool to combine all profiling pstat files into a one
single file that can be later processed by other tools.

.. class:: no-web no-pdf


.. contents::

.. section-numbering::

.. raw:: pdf

   PageBreak oneColumn


=============
Main features
=============

* Combine all pstat files present in the given dir into a single file

=============
Usage
=============

Process all files inside a directory:

.. code-block:: bash

	$ prof_merger -i ./profiling_session1/ -o combined.prof -f 01012017
	Adding file prof_01012017_26377.prof
	Adding file prof_01012017_26363.prof
	Adding file prof_01012017_26378.prof
	Writing results to combined.prof

=============
TODO
=============

* Support more file formats
* Add more filtering options
