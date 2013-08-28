#!/bin/sh

pyuic4 import.ui -o ui_import.py;
pyuic4 export.ui -o ui_export.py;
pyuic4 pick_target.ui -o ui_pick_target.py;
pyuic4 new_store.ui -o ui_new_store.py;

