from tkinter import *
from tkinter import filedialog

import json
import antlang

data = json.load(open('styles.json'))

CURSOR=data['cursor']

r = Tk()
r.wm_title(data['title'])
r.configure(cursor=CURSOR)
r.configure()

FONT = (data['font-family'], data['font-size'])

symbols = []

infovar = StringVar()
infobox = Label(r, textvariable=infovar, font=FONT, relief=RIDGE)
infobox.pack(side=TOP, fill=BOTH)
infovar.set('\n')

content = StringVar()
text = Entry(r, font=FONT, textvariable=content)

def copy(string): text.insert(INSERT,string)

frame = Frame()

def add_symbol(symbol, info, example, key=None):
	global symbols
	symbols = sorted([symbol] + symbols, key = lambda s: 1/len(s))
	btn = Button(frame, text=symbol, command=lambda: copy(symbol), font=FONT)
	btn.pack(side=LEFT, fill=BOTH, expand=True)
	btn.bind('<Enter>',
	         lambda e: infovar.set(info+(' (CTRL ' + key + ')'
	                   if key is not None
	                   else '')+'\nExample: '+example))
	if key is not None:
		r.bind('<Control_L>' + key, lambda e: copy(symbol))

men = Menu(r, font=FONT)
men.config(cursor=CURSOR)

def sub_add_command(submen, symbol):
	submen.add_command(label=symbol, command=lambda *a: copy(symbol))

def add_namespace(name, symbols):
	submen = Menu(men, font=FONT, tearoff=1)
	submen.config(cursor=CURSOR)
	for symbol in symbols:
		sub_add_command(submen, symbol)
	men.add_cascade(label=name, menu=submen)

filemen = Menu(men, font=FONT, tearoff=0)
filemen.config(cursor=CURSOR)
def import_json(*a):
	data = json.load(filedialog.askopenfile())
	for key in data.keys():
		antlang.stdlib[key] = data[key]
filemen.add_command(label='Import JSON', command=import_json)
men.add_cascade(label='File', menu=filemen)

add_namespace('Comparison', ['eq','ne','lt','le','gt','ge'])
add_namespace('Math', [ 'sin'
                      , 'cos'
                      , 'tan'
                      , 'asin'
                      , 'acos'
                      , 'atan'
                      , 'sinh'
                      , 'cosh'
                      , 'tanh'
                      , 'asinh'
                      , 'acosh'
                      , 'atanh'
                      ])
add_namespace('Lists', ['length', 'range'])

r.config(menu=men)

frame.pack(side=TOP, expand=False, fill=BOTH)

add_symbol('+', 'Plus', '3+5')
add_symbol('\\', 'Minus', '3\\5')
add_symbol('×', 'Times', '3×5', key='+')
add_symbol('÷', 'Divide', '3÷5', key='-')
add_symbol('|', 'Magnitude', '5|3')
add_symbol('^', 'Power', '2^0.5')
add_symbol('∧', 'Minimum', '1∧0', key='1')
add_symbol('∨', 'Maximum', '1∨0', key='2')
add_symbol(',', 'Catenate', '1,2,3')
add_symbol('⌷', 'Take', '-2⌷1,2,3', key='i')
add_symbol('⌷̶', 'Drop', '-2⌷̶1,2,3', key='j')
add_symbol('⌽', 'Mingle', '(1,2,3)⌽4,5,6', key='l')
add_symbol('∘', 'Apply', '\∘5', key='o')
add_symbol('⍣', 'Apply N', '({x+1}⍣5)∘10', key='n')
add_symbol("'", 'Each', "sin'range∘5")
add_symbol('?', 'Filter', '{x gt 5}?range∘10')
add_symbol('/', 'Reduce', '0+/ 1,2,3')
add_symbol('-', 'Negate', '-1')
add_symbol('(  )', 'Group', '(5×1)+2')
add_symbol('{  }', 'Function', '1 {x+2×y} 3')

r.geometry('800x600')

text.pack(side=BOTTOM, fill=X)
text.config(cursor=CURSOR)

antlang.symbols = symbols

lbox = Listbox(r,font=FONT, relief=SUNKEN)
lbox.pack(side=BOTTOM, fill=BOTH, expand=True)

def log(string):
	lbox.insert(END, str(string))
	lbox.yview(END)

def execute(string):
	try:
		log(antlang.evaluate(string))
	except Exception as e:
		log(e)
	log('')

text.bind('<Return>', lambda *a: [log(content.get()),execute(content.get()),text.select_range(0,END)][-1])

r.mainloop()
