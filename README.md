# AuthGGDCBot
  Since i bought auth.gg license management system i decided to make a discord bot for it in python.

# Features
 - On ready message.
 - Colored messages.<br/>
 - Async requests.<br/>
 - Clear function.
 - Clears console on start.
 - Erros with colored print.
 - Ascii art.
 - Log with colored print and datetime.
 - Logs can be viewed from the log.txt.
 - Users can get their license expiration date.<br/>
 - Users can view the commands with the help command.<br/>
 - Almost every variable has an empty check.<br/>
 - Every method has a json value error check with a colored message.<br/>
 - Every sensitive data is encrypted in the configs.json.<br/>
 - Admins can get the user's (email, rank, hwid, variable, lastlogin, lastip, expiry date).<br/>
 - Admins can delete users from the database.<br/>
 - Admins can edit user variables.<br/>
 - Admins can edit the user's rank.<br/>
 - Admins can change the user's password if the user forgot it.<br/>
 - Admins can check the user count.<br/>
 - Admins can get license infos by license (rank, used, used by, created at).<br/>
 - Admins can delete user's license.<br/>
 - Admins can set the license state to used.<br/>
 - Admins can set the license state to unused.<br/>
 - Admins can check the license count.<br/>
 - Admins can get the user's hwid.<br/>
 - Admins can change the bot's prefix.<br/>
 - Admins can change the authkey.<br/>
 - Owners can change the auth.gg aid.<br/>
 - Owners can change the auth.gg apikey.<br/>
 - Owners can change the auth.gg secret.<br/>
 - Owners can reset the user's hwid.<br/>
 - Owners can set the user's hwid.<br/>
 - Owners can generate license keys.<br/>
 - Owners can clear the logs.

# Installation
 Make sure you have python 3.8.7 or higher.<br/>
 Change the aid, apikey, secret, authkey with the bot do not add it to the configs.json.
```
pip3 install -r requirements.txt
``` 
 
# Configs.json 
 - token (your token for the discord bot).<br/>
 - admin_role_id (the id of the admin role on your server).<br/>
 - owner_role_id (the id of the owner role on your server).<br/>
 - prefix (bot prefix for the commands for example -help - is the prefix here).<br/>
 - aid (your auth.gg aid which you can find at the settings tab on the auth.gg website).<br/>
 - apikey (your auth.gg apikey which you can find at the settings tab on the auth.gg website).<br/>
 - secret (your application's secret key which you can find at the settings tab on the auth.gg website).<br/>
 - authkey (your application's auth key which you can find at the application's panel).

# Console
![](https://i.ibb.co/ryt6QrY/tool.png)

# ToDo
 - Add salt to the encrypted data.
 
# Support
 - PayPal: onemanbuildsofficial@gmail.com<br/>
 - BTC: 1M3MdGLNp9FvHWDyeu1ekCyY36pwwGcP7B