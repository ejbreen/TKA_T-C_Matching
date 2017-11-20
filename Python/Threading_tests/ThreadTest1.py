# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 18:48:54 2017

@author: Evan
"""

import urllib2
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

urls = [
        'http://www.reddit.com',
        'http://www.mail.umich.edu',
        'http://www.vox.com',
        'http://www.verge.com',
        'http://www.google.com',
        'http://www.youtube.com',
        'http://www.ifixit.com',
        'http://www.maps.google.com']

pool = ThreadPool()

results = pool.map(urllib2.urlopen, urls)

pool.close()

pool.join()