default: py

py:
	sudo python LilyFrog.py

ui:
	pyuic4 -o GUI/MainWindowUI.py GUI/MainWindowUI.ui

clean:
	find . -type f -iname '*.pyc' | xargs rm -rfv