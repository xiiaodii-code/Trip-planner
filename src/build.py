import json, re, subprocess, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
lf = root/'node_modules/leaflet/dist'
js = re.sub(r'//# sourceMappingURL=.*', '', (lf/'leaflet.js').read_text(encoding='utf-8'))
css = re.sub(r'/\*# sourceMappingURL=.*?\*/', '', (lf/'leaflet.css').read_text(encoding='utf-8'))
sample = subprocess.run(['python3', str(root/'src/sample.py')], capture_output=True, text=True, check=True).stdout
json.loads(sample)
sample = sample.replace('<', '\\u003c')
html = (root/'src/app.html').read_text(encoding='utf-8')
for k, v in [('/*LEAFLET_CSS*/', css), ('/*LEAFLET_JS*/', js), ('/*SAMPLE*/', sample)]:
    assert html.count(k) == 1, k
    html = html.replace(k, v)
assert ' ' not in html and ' ' not in html
out = root/'public/index.html'
out.write_text(html, encoding='utf-8')
print('built', out, len(html))
