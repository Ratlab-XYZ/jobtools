default:
	nuitka --standalone --onefile --output-dir=dist --nofollow-imports \
	--include-module=click \
	--include-module=requests \
	--include-module=dns \
	--include-module=email \
	--lto=no -j 8 --output-filename=uw main.py
