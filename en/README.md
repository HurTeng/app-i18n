# App-i18n

The app's internationalization script can convert translated documents into Android and iOS formats.

### GUI interface

![GUI界面](../img/program_interface.png)

### Android format

![Android格式输出](../img/output_Android.png)
![Android格式输出详情](../img/output_Android_details.png)

### iOS format

![iOS格式输出](../img/output_iOS.png)
![iOS格式输出详情](../img/output_iOS_details.png)

## Tips

The text first behavior translates the type of language, and the script automatically generates translated text based on the type (with the first column composing the translated text in the form of key-value) ![First line of text](../img/first_row.png)

The first column of the text is the index value of the translated text, that is, the key in the translation of each country (the key is available in all translations, so this column cannot be empty), and the other values are the value of the translated text of each country (automatically when switching languages) Change to this text) ![First column of text](../img/first_col.png)

***The translate.py*** script supports txt text and Excel tables, but you need to introduce xlrd and openpyxl libraries for xls and xlsx format tables.

***The translate_nolib.py*** script does not need to introduce third-party libraries, but only supports txt text. You can save the data in the Excel table as a txt file, or copy it into a text editor to generate a txt file (do not use the notepad that comes with Windows). Then use the script to generate a translation document with one click.

***The above script is for Python 2 environment, not compatible with Python 3 (the main reason is the difference of Tkinter library, you can modify the Tkinter reference, or directly remove the GUI interface, the code can basically run)***

## TODO

- Python3 compatible
- ~~Excel document support~~
- ~~GUI interface~~
- ~~Do not use third-party libraries to generate xml text~~
- ~~Sub-category to generate folders for translations of countries~~
- ~~ One button to generate Android translation text~~
- ~~ One button to generate iOS translation text~~
