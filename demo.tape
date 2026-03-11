# peasy-pdf — Python PDF Toolkit Demo
Output demo.gif

Set FontSize 20
Set Width 1000
Set Height 580
Set Shell "zsh"
Set Theme "Catppuccin Mocha"
Set TypingSpeed 30ms
Set Padding 24

Type "uv run --with peasy-pdf python3"
Enter
Sleep 2.5s

Type "from peasy_pdf import info, merge, split, compress"
Enter
Sleep 1s

Type "# Get PDF info"
Enter
Sleep 0.5s

Type "info('/tmp/sample.pdf')"
Enter
Sleep 2s

Type "# Split into individual pages"
Enter
Sleep 0.5s

Type "pages = split('/tmp/sample.pdf')"
Enter
Sleep 1.5s

Type "print(f'{len(pages)} pages extracted')"
Enter
Sleep 1.5s

Type "# Merge them back"
Enter
Sleep 0.5s

Type "merged = merge(pages[0], pages[1], pages[2])"
Enter
Sleep 1.5s

Type "print(f'Merged: {len(merged)/1024:.1f} KB')"
Enter
Sleep 1.5s

Type "exit()"
Enter
Sleep 1s
