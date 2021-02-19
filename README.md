# AuthGGDCBot
  Since i bought auth.gg license management system i decided to make a discord bot for it in python.

# Installation
 Make sure you have python 3.8.7 or higher.
```
pip3 install -r requirements.txt
``` 

# Features
 - Colored messages.<br/>
 - Users can get their license expiration date.<br/>
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
 - Owners can set the user's hwid.
 
# ToDo
 - Make the code better.<br/>
 - Add salt to the encrypted data.<br/>
 - Add genlicense method.<br/>
 - Add a log system or something in a txt to see who used the commands.