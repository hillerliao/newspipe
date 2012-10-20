pyAggr3g470r
============

#### A simple Python news aggregator.

.. Use headers in this order #=~-_

:toc: yes
:symrefs: yes
:sortrefs: yes
:compact: yes
:subcompact: no
:rfcedstyle: no
:comments: no
:inline: yes
:private: yes

:author: Cédric Bonhomme
:contact: http://cedricbonhomme.org/


Presentation
------------
pyAggr3g470r_ is a multi-threaded news aggregator with a web interface
based on CherryPy_. Articles are stored in a MongoDB_ base.



Features
------------
* articles are stored in a MongoDB_ database;
* find an article with history;
* e-mail notification;
* export articles to HTML, EPUB, PDF or raw text;
* mark or unmark articles as favorites;
* share articles with Diaspora, Google Buzz, Pinboard, delicious, Identi.ca, Digg, reddit, Scoopeo, Blogmarks and Twitter;
* generation of QR code with the content or URL of an article. So you can read an article later on your smartphone (or share with friends).



Requierements
-------------
Software required
~~~~~~~~~~~~~~~~~
* Python_ 2.7.*;
* MongoDB_ and PyMongo_;
* feedparser_;
* CherryPy_ (version 3 and up);
* BeautifulSoup_.


Optional module
~~~~~~~~~~~~~~~
These modules are not required but enables more features:
* lxml and Genshi;
* Python Imaging Library for the generation of QR codes.


If you want to install these modules:

.. code-block:: bash

    $ sudo aptitude install  python-lxml python-genshi


Backup
------

If you want to backup your database:

.. code-block:: bash

    $ su
    $ /etc/init.d/mongodb stop
    $ cp /var/lib/mongodb/pyaggr3g470r.* ~


Donnation
---------
If you wish and if you like pyAggr3g470r, you can donate via bitcoin. My bitcoin address: 1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ
Thank you!



License
------------
pyAggr3g470r_ is under GPLv3_ license.


.. _Python: http://python.org/
.. _pyAggr3g470r: https://bitbucket.org/cedricbonhomme/pyaggr3g470r/
.. _feedparser: http://feedparser.org/
.. _MongoDB: http://www.mongodb.org/
.. _PyMongo: https://github.com/mongodb/mongo-python-driver
.. _CherryPy: http://cherrypy.org/
.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
.. _GPLv3: http://www.gnu.org/licenses/gpl-3.0.txt