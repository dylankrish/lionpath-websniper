# LionPath Sniper
<div align="left" width="100%">
    <img src="./assets/sniperlogo.png" width="2000" alt="" />
</div>

LionPath Sniper is an open-source easy-to-use Python auto register script for LionPath.

<img src="./assets/Screenshot.png" width="900" alt="" />

Features
--
- Automatic course enrollment (enroll in courses automatically when they open)
- Automatic 2FA support (automatically enters 2FA code when prompted)
- Wait until 12AM (waits until course registration opens at 12AM)
- Error handling (restarts script if there is an error logging in, so you can sleep peacefully)
- Idle timeout handling (automatically stays logged in to LionPath when a "Your session is about to expire" prompt appears)
- Multi-platform support (Windows, Mac, Linux)
- Dark Mode (sets the browser to dark mode as well as the LionPath website)
- Automatically detects the amount of classes you want to enroll in
- Discord Integration (Send enrollment results to Discord via a webhook)
- 100% free and open-source

Installation
--
1. Python is required to run this script. If you do not have Python installed, you can download it [here](https://www.python.org/downloads/).
2. Clone this repository or download the zip file and extract it.
3. Run the following commands in a terminal:
```
python3 setup.py
```
You will be taken through the setup process where you will be asked to provide your LionPath credentials, the semester you want to select, and other options.

Usage
--
Once the setup is complete, run the following command in a terminal:
```
python3 main.py
```
The script will now run and automatically enroll you in your courses when they open.

Configuration
--
You can configure the script by editing the `config.py` file. The following options are available:
- `radnum`: Which semester to enroll in (which radio button to click starting from 1)
- `waitUntil12AM`: Wait for 12AM to enroll (for waiting for registration to open)
- `waitTimerEnable`: Wait until 3 minutes before 12AM to start the script (saves resources, but you can disable this to run the script manually)
- `darkMode`: Dark Mode (sets the browser to dark mode, also sets the LionPath website to dark mode)
- `useTOTP`: TOTP Support for 2FA (TOTP must be enabled and set as the default method on your Microsoft account for this to work)
- `useBrave`: Brave Browser Support
- `useEdge`: Microsoft Edge Support
- `sendDiscordNotification`: Discord Webhook Integration (sends enrollment results to Discord via a webhook)
- `discordWebhookURL`: Discord Webhook URL (the webhook URL to send enrollment results to)

Discord Integration
--
This script is configured to send your enrollment results to Discord via a webhook. To enable this feature, you must first create a webhook in a Discord server. To do this, follow the steps below:
1. Open Discord and navigate to the server you want to send the enrollment results to.
2. Click the settings icon next to the server name and click "Integrations".
3. Click "Create Webhook".
4. Enter a name for the webhook and click "Copy Webhook URL".
5. Paste the webhook URL into the `discordWebhookURL` option in the `config.py` file.

License
--
This project is licensed under the GNU General Public License version 3.0 (GPLv3). You are allowed to modify and redistribute this project under the terms of the GPLv3. However, please note that the GPLv3 does allow commercial use of the project. If you modify and distribute this project or its derivatives, you must make the source code available to users and distribute it under the GPLv3. Proper attribution to the original author(s) is required. See the [LICENSE](LICENSE) file for more information.