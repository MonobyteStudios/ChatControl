![ChatControl Logo](https://monobyte.studio/assets/projects/chatcontrol.png)
# ChatControl
A lightweight Twitch ChatBot that allows viewers to send inputs and commands directly to your computer, safely and in real time.

ChatControl utilizes a combination of PyAutoGui for mouse actions and AutoHotkey for keyboard actions, both of which are reliable for their respective purposes. No installation for AutoHotkey is required; it's all integrated into the codebase.

> Packages used: TwitchIO (2.10), python-dotenv, pyautogui

![Python](https://img.shields.io/badge/Python-3.10--3.13-blue)
![License](https://img.shields.io/github/license/MonobyteStudios/ChatControl)
![Issues](https://img.shields.io/github/issues/MonobyteStudios/ChatControl)

## 💫 Features

- 🕒 Real-time actions - Once someone executes a command, it happens immediately

- 🎮 Works with games - Keyboard actions use **AutoHotKey**, which allows movement in certain games. It's automatically set up in the codebase; no installation required.

- 🛠️ Restrictions Implemented - Stock restrictions have already been implemented inside ChatControl, including moderator-only commands & restricted `!keybind` combinations

- ✅ Easy to Expand - ChatControl already has integrated modules separating commands into different Python files. It's highly organized and easy to expand for whatever you need.

## 🛠️ All Commands
A list of all commands your viewers can execute in chat.

### 🖱️ Mouse
- `!click <left/right>` - Click the mouse
- `!goto <x> <y>` - Move the mouse to specified coordinates
- `!pos` - Retrieve the mouse's x and y position
- `!center` - Center the mouse in the middle of the screen
- `!drag <x> <y>` - Drag the mouse from its starting point to the specified x, y coordinates
- `!scroll <up/down> <amount>` - Scroll the mouse up or down, with an amount in pixels
- `!tiny,small,big[amount, up/down/left/right]` - A command collection for incremented movements (Ex. !tinydown, !smalldown, !bigdown)

### ⌨️ Keyboard
- `!type <content>` - Types specified content onto the host
- `!keybind <keybind, ex. 'ctrl+shift+esc'>` - Execute a keybind on the host, blacklisted keybinds are provided in `config.json`
- `!holdkey <key> <duration` - Holds a key for a certain time, max limit is 20 seconds
- `!clear` - Clears selected text using `ctrl+a+del`

### 🛠️ Moderation
Only moderators of chat can execute these commands
- `!togglecontrol` - Toggle the main feature of this application

# ⚒️ Installation
⚠️ Keyboard actions **will not** function on non-Windows versions; It's an AutoHotkey restriction. **Make sure you have Python 3.10+ installed on your computer globally!**

1. Download `codebase.zip` from the `Releases` tab. Make sure you're using the latest version!
   
2. After installation and extraction, head to `data > var` and open `client.env`. This is where you will put down credentials for ChatControl to function.

   Here's a guide on how to fill out everything:
   
   - Head to this link: https://dev.twitch.tv/console/apps and create an application in the top right corner.
     
     > You need 2FA to create applications; if you haven't turned it on, head to your Twitch account settings, go to the `Security and Privacy` tab, and enable it from there.

     - Set the `Name` to whatever you want
       
     - Set `OAuth Redirect URLs` to `http://localhost`, make sure it's using `http`, not `https`.
       
     - Set `Category` to `Chat Bot`, and make sure `Client Type` is `Confidential`.
       
     - Complete the "I am not a bot" check and create the application.
       
       
   - Click `Manage` on your recently made application, and copy the `Client ID` field in the section.
       
     - Copy this link and open it in a browser. **Make sure you replace `[CLIENT_ID]` with the client ID you copied!**
       ```
       https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=[CLIENT_ID]&redirect_uri=http://localhost&scope=chat:read+chat:edit+user:bot&force_verify=true
       ```

     - After you've authorized your application, you will be redirected to `localhost`. **Do not exit the tab!**
    
     - Look at the URL of the link, you should see something like:
        ```
             http://localhost/#access_token=[ACCESS_TOKEN]&scope=chat%3Aread+chat%3Aedit+user%3Abot&token_type=bearer
        ```
        Copy the access token provided in the link [`#access_token=[ACCESS_TOKEN]`]. **Do not copy  `&` at the end, that's a separator.**

     - Replace `OAUTH_TOKEN` inside `client.env` with the token you copied. It should look like:
          ```
       OAUTH_TOKEN=abcdefghijklmnopqrstuvwxyz
          ```

    - Go back to the `Manage` tab of your recently made application and create a Client Secret. Copy that, and paste it into the `CLIENT_SECRET` variable in `client.env`. Make sure you also get the Client ID and paste that into the `CLIENT_ID` field too!

     - The `BOT_ID` field inside `client.env` is the user ID of the **account you used when you authorized the application using the `id.twitch.tv` link.** For example, if you authorize the application on account User1, you would use the user ID of that account for the field.
       
       - To get the user ID of the account, open `Terminal` on your computer, and paste this:
         
         ```
         curl -X GET "https://id.twitch.tv/oauth2/validate" -H "Authorization: OAuth [OAUTH_TOKEN]"
         ```
         Before executing the command, replace `[OAUTH_TOKEN]` with the token you pasted inside `client.env`, specifically the field `OAUTH_TOKEN`.

       - If it was successful, it should return with JSON content:
         ```json
         {"client_id":"[CLIENT_ID]","login":"[ACCOUNT_USERNAME]","scopes":["chat:edit","chat:read","user:bot"],"user_id":"[USER_ID]","expires_in":123456789}
         ```

         Ensure the content provided matches what you need, and lastly, copy the `user_id` field inside the response, and paste it into the `BOT_ID` field inside `client.env`.

   - Lastly, the `CHAT` field inside `client.env` is the **channel username you want the application to monitor. ChatControl will listen and respond to commands in their chat.** For example, if you authorized the application as `user2` via the `id.twitch.tv` link and want it to monitor the chat of `user1`, you'd input `user1` inside the `CHAT` field.
  
   That's it for everything inside `client.env`; make sure you double-check what you put in there before continuing.

3. If you use Visual Studio Code, open it now, and open the `ChatControl` folder, **not** the `codebase` folder.
   > If you don't use Visual Studio Code, open a command prompt of your choice and navigate to the `ChatControl` folder by using `cd` or any other method.

    - It is recommended to create a virtual environment using venv. In Visual Studio Code, this can be done easily by selecting the Python interpreter you'd like to use (preferably Python 3.10–3.13), and letting it create a virtual environment automatically.

    - When prompted, choose `requirements.txt` as the base file for installing packages.

4. If you're not using Visual Studio Code or prefer setting up the environment manually, follow these steps:
     > ⚠️ Make sure your path is set to the ChatControl folder; environment setup may fail if you don't follow this step.
   
    ### Windows
     ```
     python -m venv venv
     .\venv\Scripts\activate
     pip install -r requirements.txt
      ```

   ### non-Windows
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. Once your virtual environment is installed, you're ready to use ChatControl. You can run ChatControl with this:
   
   ### Windows
    ```
    venv\Scripts\python.exe structure/main.py
    ```
  
    ### non-Windows
    ```
    venv/bin/python structure/main.py
    ```

    You don't have to run ChatControl this way; you can do it via Visual Studio Code, `.bat` files, you name it.

    > 💡 You can also activate venv first, then directly run main.py from there. If you don't want the terminal to show, use `pythonw.`
