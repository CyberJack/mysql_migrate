MySQL Migrate
=============

You can use this script to migrate mysql databases to a new server while keeping the users, passwords and rights.<br>
It will show you what databases to migrate (based on user rights) and shows you the sql queries which will re-create the users (with rights).

<b><u>Only database with specific user rights will be shown!
If you have users without access to a database or databases without specific user rights, they will be excluded from the overview!</u></b>

Make sure you migrate the databases before adding the users to the new MySQL server.<br>
Rights cannot be set to non existing databases.

Requirements
------------

- MySQL / Percona / MariaDB
- Python 3

Installation
------------

Clone this repository and alter the mysql_migrate.py script.<br>
Change the configuration part to provide the path to the mysql executable, mysql root username and password.

### Example configuration
<pre># Replace the path of the mysql executable and set the root username/password
mysql = {
	"cmd": "/usr/bin/mysql",
	"username": "root",
	"password": "myverysecretrootpassword"
}</pre>

When using a mysql without a user password (shame on you!) you can leave the password field empty.<br><br>
If you are using a custom <code>~/.mycnf</code> file, make sure the username matches and leave the password empty. MySQL will read it automaticaly.

Running
-------
To run the script, just make sure its executable and run <code>./migrate_mysql.py</code><br>
The script will gather the migration information and will show the following output:

### Example output
<pre>MySQL Migrate = 0.1a

Gathering user information: done
Gathering rights and database information: done

Migrate the following databases:
  api
  test1
  test2

Migrate the users with the following sql queries:
  GRANT USAGE ON *.* TO 'testuser'@'localhost' IDENTIFIED BY PASSWORD '...';
  GRANT ALL PRIVILEGES ON `test1`.* TO 'testuser'@'localhost';
  GRANT ALL PRIVILEGES ON `test2`.* TO 'testuser'@'localhost';
  GRANT USAGE ON *.* TO 'apiuser'@'localhost' IDENTIFIED BY PASSWORD '...';
  GRANT ALL PRIVILEGES ON `api`.* TO 'apiuser'@'localhost';</pre>

Todo
-----
- commandline parameters for mysql executable, username and password
- configuration file so main script does not need to be altered
