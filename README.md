
[![Build Status](https://travis-ci.org/bisonlou/ireporter.svg?branch=master)](https://travis-ci.org/bisonlou/ireporter) [![Maintainability](https://api.codeclimate.com/v1/badges/9d3f3eadf80b3a89bcfe/maintainability)](https://codeclimate.com/github/bisonlou/ireporter/maintainability) [![Coverage Status](https://coveralls.io/repos/github/bisonlou/ireporter/badge.svg?branch=master)](https://coveralls.io/github/bisonlou/ireporter?branch=master)

#### A web app to aid government and citizens reduce corruption, and holding leaders and representatives honest and efficient.


Installation
------------
To access the api, browse to https://bisonlou.herokuapp.com/ using postman

***To register***
``` {.sourceCode .bash}
/api/v1/register

Body - application/json
{
    "username": "your-email",
    "password": "your-password",
    "phone": "your-phone-no"
}

```

***To login***
``` {.sourceCode .bash}
/api/v1/login

Body - application/json
{
    "username": "your-email",
    "password": "your-password"
}

and copy your access token.

```

***To post a red flag***
``` {.sourceCode .bash}
/api/v1/red_flag

Body - application/json
{
    "title": "flag-title",
    "comment": "flag-body",
    "location": "(0.000000, 15.00000)",
    "images": "[image_name.jpg, 300]",
    "videos": "[video_name.mov, 1024]"
}

use the access token obtained at login to authenticate.

```

***To get a red flag***
``` {.sourceCode .bash}
/api/v1/red_flag/1

use the access token obtained at login to authenticate.

```

***To get all red flag***
``` {.sourceCode .bash}
/api/v1/red_flags/

use the access token obtained at login to authenticate.

```

***To put a red flag***
``` {.sourceCode .bash}
/api/v1/red_flags/1

Body - application/json
{
    "title": "flag-title",
    "comment": "flag-body",
    "location": "(0.000000, 15.000000)",
    "images": "[image_name.jpg, 300]",
    "videos": "[video_name.mov, 1024]"
    "status": "Pending"
}

use the access token obtained at login to authenticate.

```

***To patch a red flag***
``` {.sourceCode .bash}
/api/v1/red_flags/1/location

Body - application/json
{
    "title": "flag-title",
    "comment": "flag-body",
    "location": "(0.000000, 0.000000)",
    "images": "[image_name.jpg, 300]",
    "videos": "[video_name.mov, 1024]"
    "status": "Pending"
}

use the access token obtained at login to authenticate.

```

***To delete a red flag***
``` {.sourceCode .bash}
/api/v1/red_flags/1

use the access token obtained at login to authenticate.

```

**Contributers**
----------------
Innocent Lou <bisonlou@gmail.com>

How to Contribute
-----------------
```
1.  Check for open issues or open a fresh issue to start a discussion
    around a feature idea or a bug.
2.  Clone [the repository](https://github.com/bisonlou/ireporter.git) on
    GitHub to start making your changes to the **deploy** branch (or
    branch off of it).
3.  Write a test which shows that the bug was fixed or that the feature
    works as expected.
4.  Send a pull request and bug the maintainer until it gets merged and
    published. 
```

**License**
------------------
Read only

