# ietf-yang-static-webpage

this project depends the following 3pp python library:  
- jinja2  

This python programme is used to generate static web page for the result (json file) generated by `crwal-ietf-yang`.  

The static web page uses `bootstrap` and `flat-ui` CSS libaraies, which are embedded into the project in lab folder. (including several images in lab folder)  

you can generate the web pages and populate the web pages into the lab folder and run it as following
1. generate the web pages:  
```
python main.py <the r.json location> <the position to populate the genreated files>
```
for example - generate the pages into lab folder:  
```
python main.py ../../r.json ./lab/

```
2. the generated files are in lab folder. you can double click the `index.html` file to open it in your browser.  