# Typing Imitator

Typing Imitator program allows you to simulate the "typing" status in Telegram for specified contacts using the Telethon library.

## Installation and Setup

To install and run Typing Imitator, follow these steps:

### 1. Clone the repository

```
git clone https://github.com/GeRRyOD/typing-imitator.git
cd typing-imitator

```
### 2. Install Python

```
sudo apt install python3

```

### 3. Install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

```

### 4. Run the program

```
bash run.sh

```

### 5. First run
During the first run, the program will prompt for the following information:

1. Telegram API ID and API Hash

  Go to my.telegram.org, log in with your phone number.
   
  Choose "API development tools" and fill out the form to register a new application.

  Enter the API ID and API HASH into the program when prompted.
  
2. Phone number for login: Enter your phone number used for Telegram login. The program will automatically create necessary files for further operation.
3. After successful authorization, the program will ask for the desired random timeout for sending the "typing" command.
4. Then, the program requests @username or ID of users to whom we will send the "typing" status.
5. If all targets are selected, leave the field blank and press Enter.
6. The program will start its operation. To terminate the program, press Ctrl+C in the terminal window.
7. Have Fun :)

### 6. Subsequent runs
In subsequent runs of the application, your session is loaded automatically, requiring only the id/username of the target.
