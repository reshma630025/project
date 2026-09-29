import re

with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add text file reading logic to handleFile
handle_file_orig = r"function handleFile(file, kind){"
handle_file_new = """function handleFile(file, kind){
  // Universal Text/Dataset file drop parsing
  if (['scamTextFile', 'emailTextFile', 'urlTextFile', 'jobTextFile', 'socialTextFile'].includes(kind)) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const text = e.target.result;
      let targetId = '';
      if (kind === 'scamTextFile') targetId = 'scamText';
      if (kind === 'emailTextFile') targetId = 'emailBody';
      if (kind === 'urlTextFile') targetId = 'urlInput';
      if (kind === 'jobTextFile') targetId = 'jobDesc';
      if (kind === 'socialTextFile') targetId = 'socialText';
      
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.value = text.length > 5000 ? text.substring(0, 5000) + '\\n...[TRUNCATED]' : text;
        toast('File Loaded', `Loaded content from ${file.name}`, 'info');
      }
    };
    reader.readAsText(file);
    return;
  }
"""

html = html.replace(handle_file_orig, handle_file_new)

# Add dropzones to the respective textareas
dropzone_template = """<div class="dropzone" data-accept="text/plain,text/csv,application/json" data-kind="{kind}" style="padding:15px; margin-bottom:10px; min-height:80px;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px; height:24px; margin-bottom:4px;"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"></path><path d="M14 3v5h5M16 13H8M16 17H8M10 9H8"></path></svg>
            <h4 style="font-size:13px; margin:0;">Drop Dataset or Text File</h4>
            <p style="font-size:11px; margin:0;">TXT, CSV, JSON</p>
          </div>"""

# Scam
html = html.replace('<textarea class="textarea" id="scamText"', dropzone_template.format(kind='scamTextFile') + '\n          <textarea class="textarea" id="scamText"')

# Email
html = html.replace('<textarea class="textarea" id="emailBody"', dropzone_template.format(kind='emailTextFile') + '\n          <textarea class="textarea" id="emailBody"')

# URL
html = html.replace('<input type="url" class="field" id="urlInput"', dropzone_template.format(kind='urlTextFile') + '\n          <input type="url" class="field" id="urlInput"')

# Job
html = html.replace('<textarea class="textarea" id="jobDesc"', dropzone_template.format(kind='jobTextFile') + '\n          <textarea class="textarea" id="jobDesc"')

# Social
html = html.replace('<textarea class="textarea" id="socialText"', dropzone_template.format(kind='socialTextFile') + '\n          <textarea class="textarea" id="socialText"')


with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "w", encoding="utf-8") as f:
    f.write(html)
