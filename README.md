# Change terminal background color with CUI.

## Requirements
- Python3
- python module
  - pip3 install -r requirements

## Usage
### Change color
python3 vtcolor.py

```
---------------------------------
VTBACKGROUND   0   0   0
             ~~~ ~~~ ~~~
            red green blue
---------------------------------
Key:
←,→: left or right cursor.
↑,↓: increment or decriment color value.
ENTER: save config to ~/.vtcolor and exit
CTRL+C: exit
ESC+ESC: exit
```

### Apply colors on login.
Add the following ~/.bashrc
```
if [ -f ~/.vtcolor ]; then
  source ~/.vtcolor
  echo -ne "\e]11;${VTBACKGROUND}\e\\"
fi
```

