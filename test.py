import codecs

t = "\\xe2\\x80\\x9cWell, one of,\\xe2\\x80\\x9d he"
#unicode escape converts string to latin-1+reglar non slash characters in byte format, since it interprets byte by byte, so instead once we decode, we encode it back in latin-1 to give us the proper one slash syntax
#then we decode it with utf-8
t = t.encode().decode("unicode-escape").encode("latin-1").decode('utf-8')

t = ["hello.","get me."]
y = "."
y =  y.upper() == y.lower()
m = ["".join(y for y in x if y.upper() != y.lower() or y == " ").lower() for x in t]
""