plexify
=======

A new content notification script for Plex Media Center.

---

Tested with Python 2.7.6 and Plex Media Server 0.9.9.7.429-f80a8d6 (Ubuntu 64-bit)

##### Install
1. Run `git clone https://github.com/b225ccc/plexify.git`
1. Install python modules `requests` and `bs4`
1. Update `config.py`
1. Add SMTP password to file `pass.txt`
1. Run `./plexify.py` manually and/or add to cron:


    ````
    crontab -e
    
    # plexify
    0 * * * * /home/username/plexify/plexify.py 2>&1 &
    ````
   
#### Example notification email
````
Date: Mon, 13 Oct 2014 21:42:37 -0700 (PDT)
From: xxxxxxx@gmail.com
To: xxxxxx@gmail.com
Subject: New content in Plex - 2014-10-13 22:41:04

New music:
 * Slipknot - .5: The Gray Chapter
 * Stone Sour - House Of Gold & Bones, Part 2
 * Hellyeah - Blood for Blood

New movies:
 * Jack Ryan: Shadow Recruit

New TV shows:
 * Hell on Wheels (Season 4)
 * Cosmos: A Spacetime Odyssey (Season 1)
````