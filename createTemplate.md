# How-to create template

Once your template is working perfect, do not forget to submit it to the community via a Pull Request!

## HTML Files
You are free to implement any HTML + CSS files to get the look and feel you want, however, do not forget to do the bridge with the core javascript part described in the next section.

## Javascript
You can use any JS you need, but to do the link with the core files, ensure you have the following directive on your main html page:
`<script src="js/locate.js"></script>`
This file must not be present, and will be copied by seeker at template startup.

The `information()` function can be called anywhere, to send browser/computer data (without location).

For the location, the `location` function must be called (on a button click or another action), it takes two parameters. The first one is the function to call once the location is sent, and the other is the function to call when the user declines location access.

```
<a class="tgme_action_button_new" onclick="locate(popup, function(){$('#change').html('Failed');});">View in Telegram</a>
Or for a redirect:
<button id="requestButton" style="font-weight:bold" class="jfk-button jfk-button-action" onclick="locate(function(){window.location='REDIRECT_URL';}, function(){$('#change').html('Failed');});">Request access</button>
```

## Template files
There is a unique `templates.json` file, add another entry to this file, at the end.
```        
        ,
        {
            "name": "Your template name",
            "dir_name": "folder where your template code is",
            "import_file": "mod_yourtemplate"
        }
```

## Python file
In the `template` folder, you will find a set of mod_*.py file, you can copy and adapt an existing one and report the name in the `templates.json` file described above.
This python file is used to replace variables, and prepare files at template startup.

## PHP file
PHP side is managed by seeker, do not include any PHP file
