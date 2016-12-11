# heat2d3
Heat template to javascript convertor for d3 visualization

Dependencies:
* PyYaml

Usage:
```
cat heat.json | ./heat2d3.py > heat.js
cat heat.yaml | ./heat2d3.py > heat.js
```

Server:
Minimal HTML server to serve the generated graph as svg.
Temp files are written to /tmp and removed afterwards.
Default port 1112.

Dependencies:
* Graphviz
* Flask

Usage:
```
./heat2d3_server.py
```
