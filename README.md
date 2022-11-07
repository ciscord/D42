## Initial Install

Install Prerequisites:
 - [python 2.x](https://www.python.org/)
 - [node.js v4.4.3+](https://nodejs.org)
 - [virtualenv](https://virtualenv.pypa.io)
 - [postgresql](http://www.postgresql.org)
 - [psycopg2](http://initd.org/psycopg/)

### Install NodeJS (Debian/Ubuntu)

Add NodeJS v4.x APT repository (via Joyent script):
```
$ curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
$ sudo apt-get install -y nodejs build-essential
```

Verify you have both NodeJS and NPM installed correctly:
```
$ node --version
$ npm --version
```

### Install python2, pip, postgresql, and psycopg2 library:

Install required debian packages:
```
$ sudo apt-get install python2.7 python-pip python-virtualenv python-dev python-psycopg2 libpq-dev postgresql postgresql-contrib libffi-dev
```

Install Python packages:
```
$ python -m pip install virtualenv 
```

### Initialize environment

Clone this repository:

Initialize, set environment variables, and activate the virtual environment:
```
$ python -m virtualenv env
$ cat .environment >> env/bin/activate
$ source env/bin/activate
```

Verify ```pip``` dependencies installed correctly under ```virtualenv```:
```
$ which pip
> {currentpath}/env/bin/pip ```should be within the virtualenv directory```
```

Install ```pip``` dependencies using ```./requirements.txt``` they are not already installed:
```
$ pip install -r requirements.txt
```

If no errors, proceed with installing nodejs dependencies:
```
$ npm install
```

If you receive errors when running ```npm install```, try running these commands:
```
$ npm install -g gulp-cli
$ npm install gulp-sass
```

Create new role and database for PostgreSQL:
```
$ sudo su postgres
$ createuser d42 -P
> d42 ```
$ createdb --owner d42 d42
$ exit
```

Finally apply initial migration:
```
$ gulp migrate
```

=======================================

## Usage

Test dev environment. You should see "Hello, World!":
```
$ gulp --debug --serve
```

Test prod environment. You should see "Hello, World!":
```
$ gulp --serve
```

## Tasks

```gulp --debug --watch --serve```: (Best used during development) Compiles all source files, serves the site and watches for file changes. 

```gulp```: Builds the entire project in production.

```gulp optimize```:  Optimizes all images from `build` folder and outputs to `optimized` folder

All tasks are broken into micro-tasks, check out the `tasks` folder for more details. Also see `tasks/.taskconfig` for more custom flags such as `--skip-js-min`, `--skip-css-min`, etc.


## Cloud Setup (Linux)

Installing uWSGI
```
$ sudo pip install uwsgi
```

Installing Nginx
```
$ sudo apt-get install nginx
```

### Serving with uWSGI and Nginx
Configure ```website_uwsgi.ini``` and ```website_nginx.conf``` files to reflect the correct server name.

Symlink ```website_nginx.conf``` so Nginx can see it:
```
$ sudo ln -s /path/to/your/website_nginx.conf /etc/nginx/sites-enabled/
```

Restart Nginx:
```
$ sudo service nginx restart
```

Create directory for storing uWSGI vassals:
```
$ sudo mkdir /etc/uwsgi
$ sudo mkdir /etc/uwsgi/vassals
```

Symlink ```website_uwsgi.ini```
```
$ sudo ln -s /path/to/your/website_uwsgi.ini /etc/uwsgi/vassals/
```

Run uWSGI in emperor mode:
```
$ uwsgi --emperor /etc/uwsgi/vassals
```

Make uWSGI startup when the system boots using ```upstart```:
```
$ sudo nano /etc/init/uwsgi.conf
```
Add:
```
description "uWSGI Emperor"

start on runlevel [2345]
stop on runlevel [!2345]

script
    . {virtualenv_path}/bin/activate
    uwsgi --emperor /etc/uwsgi/vassals
end script
```

Visit external IP of your VM instance. Voila.

## Optional Environment Variables

1. `DJANGO_CONFIG_DEBUG`: You can set this to any string you want in `bin/activate` of your `virtualenv`. This will force `gulp` command to build the app in debug, which is useful when you have different environment setup in the cloud.

## Common Issues

1. If Nginx cannot serve the project (getting a 500 Internal Error or something like that), check the error logs at ```/var/log/nginx/error.log```.

2. If you get an error about permission issues with writing to the UDP socket upon starting the uWSGI emperor, you might need to change the owner of the project directory to the Nginx owner/group, which is probably `www-data:www-data`

3. If you are getting a 400 error, you can debug this using your browser console to see what is wrong. If you get a GET request fail on the domain itself, chances are you forgot to add your domain to the ALLOWED_HOSTS of your Django project settings.

4. If you are getting a 500 error, enable DEBUG in project/settings/prod.py. It could be something trivial.

---


# A/B Testing Views Framework

Instead of rendering your template with `render` or `render_to_response` use the `render` method on the `Experiment` object

    def landingPage(request, error_msg=''):
        exp = Experiment.objects.get(name='landingColor')
        return exp.render(request, {})

or

    def landingPage(request, error_msg=''):
        exp = Experiment.objects.get(name='landingColor')
        random = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
        return exp.render(request, {
            'error_msg': error_msg,
            'random': random,
        })

Rendering your template with the experiments render method will assign the user a Test and set some cookies to keep track of which Test they have been assigned, and consequently, which template will be rendered (until the user deletes their cookies and gets a new Test issued).

AB tests need to have a Goal. We are testing to see which template accomplishes our goal. Somewhere in your code you should call the `achieveGoal(request, response)` method on the experiment object.

for example in your `userDidSignUpAndPayUsATonOfMoney` view:

    def userDidSignUpAndPayUsATonOfMoney(request):
        ...
        exp = Experiment.objects.get(name='landingColor')
        exp.achieveGoal(request, response)
        return HttpResponse('Congratulations, you are signed up for lolcat!')

Calling this method will check to make sure our user hasn't already achieved this goal, and then increment our conversions count. 

When you are done. Open up your landingPage then clear the cookies and do it again, then do it a third time. You should see your different templates being loaded and see Test.hits being incremented in the admin.

This works to AB test your system. You will have to open up your admin panel to see the results of the test and draw your own conclusions.
