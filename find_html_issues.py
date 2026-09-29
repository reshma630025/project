with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines in index.html:', len(lines))

# Check for obvious issues:
# 1. Unclosed tags or malformed attributes
for i, line in enumerate(lines):
    # Check for unescaped < in attributes or broken tags
    if '<<' in line or '>>' in line:
        print(f'Line {i+1}: possible double bracket: {line.strip()[:60]}')
    if 'undefined' in line and not line.strip().startswith('//') and not line.strip().startswith('*'):
        if 'typeof' not in line and '!==' not in line and '===' not in line:
            # check if literal undefined is used incorrectly
            pass

# Check the script tag at the end
print('Last 10 lines:')
for i in range(len(lines)-10, len(lines)):
    print(f'{i+1}: {lines[i].rstrip()}')
