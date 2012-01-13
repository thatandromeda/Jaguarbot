# README

I've found that many READMEs assume a higher level of technical background thna I have, and I want my documentation to be reasonably complete and instructive even for people fairly new to code.  Please tell me where I've succeeded and failed, and feel free to issue pull requests to edit & improve this file.

These instructions do assume you are reasonably comfortable with the command line in Terminal, and with reading (and possibly Googling) error messages.  They also assume you can push/pull with git.

## Setting up the environment
### Mac OS 10.7.2.

* Install Xcode
    * must register as an Apple developer
    * free via http://developer.apple.com/xcode/
    * you need this anyway to do any coding on a Mac; without it you run into surprising and incomprehensible errors
* Install pip: <code>sudo easy_install pip</code>
    * you can live without it, but this package manager makes it vastly easier to install Python libraries
* Install tweepy: <code>pip install tweepy</code>
   * If you want to browse tweepy's code: http://code.google.com/p/tweepy/
* Install MySQLdb: <code>pip install mysql-python</code>
   * If mysql_config is not on your path, this will fail
      * On my machine, <code>echo 'export PATH=/usr/local/mysql/bin:$PATH' >> ~/.bash_profile</code>, then reopening my terminal window, was the needed incantation
   * This may fail with a "wrong architecture" error, in which case you need the 64-bit version of mysql:
      * shut down any currently running mysql server (System Preferences > MySQL or <code> mysqladmin -u user -ppassword shutdown</code>)
      * download from http://dev.mysql.com/downloads/mysql/
      * make sure to get the .dmg, not the .tar.gz -- easier
      * you don't actually have to create an account; there's an easy-to-miss "no thanks" link at the bottom
      * reinstall mysql-python after mysql installation completes
   * The useful reference for MySQLdb: http://www.kitebird.com/articles/pydbapi.html
* Create a user and database in mysql
   * <code>mysql</code>
   * <code>CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';</code>
   * <code>CREATE DATABASE yourdb;</code>
   * <code>GRANT ALL ON yourdb.* TO 'username'@'localhost';</code>
   * You can also do this with a graphical front end via phpmyadmin
   * Finally, you'll need to get your data from somewhere; in my case I had an SQL dump (<code>jaguars.sql</code>) of my existing Drupal database for http://jaguars.andromedayelton.com, so I imported that into my local db (named <code>jaguars</code>) with <code>mysql -u myusername -pmypassword jaguars < jaguars.sql</code>
      * note that there IS a space after -u, but there is NOT a space after -p

### Other

I tried and failed to install this on my web hosting, an Ubuntu; I needed <code>sudo</code> to install one of the dependencies for MySQLdb.  I tried and failed to install this on another always-on Ubuntu machine on which I am a sudoer.  Meh.  Would love to hear from others who got it working.

Some things I did figure out along the way:

* MySQLdb relies on mysql_config, which is _not_ part of the standard SQL install; you'll need to install <code>libmysqlclient15-dev</code> to get it (which is what requires sudo): <code>sudo apt-get install libmysqlclient-dev</code>
* you can install MySQLdb with <sudo>apt-get install python-mysqldb</code>
* you can install everything _except_ mysql_config to a virtual environment without needing sudo, if you feel like doing the virtualenv dance, but mysql_config seems to require it

## Your settings
In your local repo, copy <code>settings.py</code> to <code>mysettings.py</code>.  Fill in the database settings according to the user and database you created above.  You'll be filling in the rest of the settings during the Authorizing with Twitter steps.

<code>mysettings.py</code> is in .gitignore so don't worry -- your passwords will not be pushed up to any git repo.

## Authorizing with Twitter
* Register as a developer at https://dev.twitter.com/ .
   * Copy your CONSUMER_SECRET and CONSUMER_KEY into mysettings.py
* Create an account for your app to post to (unless you want it to post to your own timeline, but that'd be weird)
* Follow these instructions to create an app and authorize it to post to your account: http://talkfast.org/2010/05/31/twitter-from-the-command-line-in-python-using-oauth
   * note that I've modified his one-off utility script here as <code>get_access_key.py</code>
   * Make sure you're logged in _as the target account_ when you do the in-browser step in these directions
   * when you get your ACCESS_KEY and ACCESS_SECRET, copy them into mysettings.py.

## launchd
Jaguarbot is designed to run once daily.  I thought I'd do this with the standard *nix <code>cron</code> command, but there are two problems with that:
* my laptop is often asleep, and I didn't know how cron and sleep would interact; googling suggested the answer was, "badly"
* I couldn't get my dev env set up on an always-on machine, per above

launchd is Apple's One Time-Based Daemon To Rule Them All thing, replacing cron and initd and a bunch of stuff.  It has the awesome feature that it handles sleep gracefully; if a job was supposed to happen when the computer was asleep it queues it up and executes it on next wake.  It has the annoying feature that it has its own special-snowflake XML syntax that is copiously, yet unhelpfully, documented.

Anyway, to make it run you will need to...
* create a .plist file (see mine in this repo)
* put it in one of the magical locations where OS X looks for .plist files (mine is in /Library/LaunchDaemons)
* tell OS X to find it -- <code>launchctl load /path/to/filename</code>
* I'm still figuring out what I need to do to ensure it automatically gets noticed on reboot.  I think the needed steps are some combination of:
   * <code>chmod 0755 yourfilename</code>
   * <code>sudo chown root yourfilename</code> (if you put it in /Library/LaunchAgents rather than LaunchDaemons, this may not be needed)
   * add <code>launchctl load /path/to/filename</code> to /etc/launchd.conf (which you may have to create; needs sudo) 
