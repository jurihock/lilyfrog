default: py

py:
	sudo python LilyFrog.py

ui:
	pyuic4 -o GUI/MainWindowUI.py GUI/MainWindowUI.ui