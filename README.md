# Discord_tool ⛏️
This is a custom tool for discord with a gui used for easily deleting open dms, group dms, and server messages. It can also be used to easily open closed dms and easily view message counts for different servers or dms.

# Features
* User Friendly GUI to easily navigate different aspects of a users account.  
* custom delete delay between messages.  
* ability to open closed dms from the discord data package and see which ones are already open.  
* display and choose to delete all messages from multiple servers at once.  
* Get and Display all sever and dm messages counts  

# Compile
If you would like to compile yourself. You can do it with pyinstaller and run this command once in the directory. To do this clone the dir with:  
```sh
git clone https://github.com/NathanZC/discord_tool.git
cd discord_tool
pip install -r requirements.txt
```

And then run this command to compile it (make sure you have pyinstaller installed):  
```pyinstaller --onedir --windowed --debug=bootloader --add-data "test_images;test_images" --icon=icon.ico --name DiscordTool gui.py```  

If you would just like to run the program:  
```python gui.py```


# Preview  
![thingggg](https://github.com/NathanZC/discord_tool/assets/58007916/bafac0ad-67da-402d-89d1-571ba14a47d7)

