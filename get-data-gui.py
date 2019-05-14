from tkinter import *
import tkinter.messagebox as messagebox
import nltk
from nltk.tokenize import sent_tokenize
from tkinter import font
#from PyDictionary import PyDictionary
from googletrans import Translator
translator = Translator()
#import getParagraphs

#dictionary=PyDictionary()

content = []
par_no = 0
book_opened = False
list_buttons_pos = []; list_buttons_comb = []; list_buttons_check = []
list_buttons_content = []
list_buttons_chosen = []
list_in_words = []
nouns = []; verbs = []; adj = []
all_comb = []
under_frame_y = 400


def createChosenList(caller):
    global list_buttons_chosen
    new_button = Button (window,text=caller['text'])
    print(len(list_buttons_chosen))
    if len(list_buttons_chosen)==0:
        new_button.place(x=610,y=under_frame_y,height=25,width=95)
    else:
        new_button.place(x=610+(len(list_buttons_chosen)%4)*100,y=under_frame_y+int(len(list_buttons_chosen)/4)*30,height=25,width=95)
    list_buttons_chosen.append(new_button)


def itsaNoun(event):
    caller = event.widget
    caller.configure(bg='#A9A9A9',fg='black')
    caller.configure(borderwidth=2)
    createChosenList(caller)
    

def itsaVerb(event):
    caller = event.widget
    caller.configure(bg='#A9A9A9',fg='black')
    caller.configure(borderwidth=2)
    createChosenList(caller)


def itsanAdj(event):
    caller = event.widget
    caller.configure(bg='#A9A9A9',fg='black')
    caller.configure(borderwidth=2)
    createChosenList(caller)

def justaWord(event):
    global list_in_words
    caller = event.widget
    caller.configure(bg='#A9A9A9',fg='black')
    caller.configure(borderwidth=2)
    createChosenList(caller)
    list_in_words.append(caller['text'])
    print(list_in_words)

def on_leave(event):
    caller = event.widget
    caller.configure(borderwidth=0)

def on_enter(event):
    caller = event.widget
    caller.configure(borderwidth=2)


def translate(event):
    caller = event.widget
    toTrans = caller['text']
    r = translator.translate(toTrans,dest='ro')
    translate_frame = Text(window,height=10, width=30, borderwidth=1)
    translate_frame.place(x = 760, y = 60)
    translate_frame.configure(bg="#f1f1f1")
    translate_frame.insert(END,' '+toTrans+' = ')
    translate_frame.insert(END,r.text)


def insert_text(par):
    lastx,lasty = 0,0
    tok_text = nltk.word_tokenize(par)
    for w in tok_text:
        #while w in """.,'?"!:."""
        if lastx + len(w)*10 > 550:
            lastx,lasty = 0,lasty+30

        times14 = font.Font(font='Times',size=13)
        ss = font.Font(font='Sans-Serif', size=3)
        new_button = Button(content_frame, text = w,borderwidth=0, font=times14,fg='#0F1626')
        
        new_button.place(x=lastx, y=lasty, height=25)
        list_buttons_content.append(new_button)
        new_button.bind("<Leave>", on_leave)
        new_button.bind("<Enter>", on_enter)
        new_button.bind("<Button-1>", justaWord)
        new_button.bind("<Button-3>", translate)

        if w in nouns:
            new_button.bind("<Button-1>", itsaVerb)
            new_button.configure(bg='#2F4F4F',fg='white')

        if w in verbs:
            new_button.bind("<Button-1>", itsaVerb)
            new_button.configure(bg='#2F4F4F',fg='white')

        if w in adj:
            new_button.bind("<Button-1>", itsaVerb)
            new_button.configure(bg='#2F4F4F',fg='white')


        content_frame.update_idletasks() 
        lastx += new_button.winfo_width()
        if w in ".:!?,":lastx += 10


def open_book(event):
    global content, book_opened, list_in_words, list_buttons_content
    book_opened = True
    #text.delete(1.0, END)
    list_buttons_content=removeButtons(list_buttons_content)
    caller = event.widget
    bookNames = [e[1] for e in books]
    bookName = books[bookNames.index(caller['text'])][0]
    f = open("paragraphs/" + bookName + "-paragraphs.txt",'r')

    content = f.readlines()
    getPOS(content[0])
    insert_text(content[par_no])
    list_in_words = nouns + verbs + adj
    print(f"list_in_words = {list_in_words}")
    


def removeButtons(list_buttons):
    for e in list_buttons:  
        e.destroy()
    list_buttons = []
    return list_buttons


def change_par():
    if book_opened == False:
        messagebox.showwarning("Warning","Please open a book first!")
        return

    global par_no, content,all_comb, list_in_words, list_buttons_chosen
    global list_buttons_check, list_buttons_comb, list_buttons_content
    all_comb = []

    # Remove previous buttons
    # removeButtons(list_buttons_pos)
    list_buttons_check=removeButtons(list_buttons_check)
    list_buttons_comb=removeButtons(list_buttons_comb)
    list_buttons_content=removeButtons(list_buttons_content)
    list_buttons_chosen=removeButtons(list_buttons_chosen)
    print('list_buttons_chosen = ',list_buttons_chosen)

    getPOS(content[par_no])
    insert_text(content[par_no])
    list_in_words = nouns + verbs + adj


def prev_par(event):
    global par_no
    par_no = par_no - 1
    change_par()


def next_par(event):
    global par_no
    par_no = par_no + 1
    change_par()


def getPOS(par):    
    print("Original Paragraph: ",par);print()
    # Remove Punctuation
    par = re.sub(r'[^\w\s]',' ',par)
    par = par.lower() # won't be able to identify NNPs
    
    ## Word tokenization
    tok_text = nltk.word_tokenize(par)
    print("Tokenized Paragraph: ",tok_text);print()

    # Removing Stopwords
    from nltk.corpus import stopwords
    stop_words=set(stopwords.words("english"))
    filtered_par=[]
    for w in tok_text:
        if w not in stop_words and w not in filtered_par:
            filtered_par.append(w)
    print("Filterd Paragraph:",filtered_par);print()

    # POS tagging
    parts_of_speech = nltk.pos_tag(filtered_par)
    print(parts_of_speech);print()

    global nouns,verbs,adj
    # Get Nouns
    nouns = [e[0] for e in parts_of_speech if 'NN' in e[1]]
    #createButtons(nouns,700,60,True)
    print("Nouns: ",nouns);print()

    # Get Actions
    verbs = [e[0] for e in parts_of_speech if 'VB' in e[1] or 'RB' in e[1]]
    #createButtons(verbs,800,60,True)
    print("Actions: ",verbs);print()

    # Get Adjectives
    adj = [e[0] for e in parts_of_speech if 'JJ' in e[1]]
    #createButtons(adj,900,60,True)
    print("Adjectives: ",adj);print()




def createButtons(list,xi,yi,col):
    
    global list_buttons_pos, list_buttons_comb
    i=0
    for item in list:
        new_button = Button(window, text = item)
        if col:
            new_button.place(x=xi, y=yi+i*30,width = 95, height=25)
            list_buttons_pos.append(new_button)
        else:
            new_button.place(x=xi+i*100, y=yi,width = 95, height=25)
            list_buttons_comb.append(new_button)
        i=i+1


def check_comb(event):
    caller = event.widget
    index = caller['text']
    print("index = ", index)
    index = (int(index)-1)*3
    for i in [index-3,index-2,index-1]:
        createChosenList(list_buttons_comb[i])




def getRand(n):
    import random
    return random.randint(0,n-1)


def genComb(event):
    if book_opened == False:
        messagebox.showwarning("Warning","Please open a book first!")
        return

    global nouns,verbs,adj,all_comb,list_buttons_check
    nn = len(nouns)
    nv = len(verbs)
    na = len(adj)

    #print(f"Limit = {nn*nv*na}. When hitting Hint Button, len = ",len(all_comb))

    n = 5 ##### 10
    left = nn*nv*na-len(all_comb)
    print("left : ", left)
    if  6 >= left:
        n = left
        messagebox.showwarning("Warning","These are the last combinations left!")

    for e in range(1,n+1):
        new_button = Button(window, text = str(e+len(all_comb)))
        new_button.place(x=140, y=under_frame_y+e*30,width = 35, height=25)
        new_button.bind("<Button-1>", check_comb)
        list_buttons_check.append(new_button)


    for i in range(n):
        r = [ getRand(nn),getRand(nv),getRand(na)]
        while r in all_comb:
            print("Duplicat: ",r)
            r = [ getRand(nn),getRand(nv),getRand(na)]
            
        all_comb.append(r)
        #print("After Appending r, len = ",len(all_comb))
        createButtons([nouns[r[0]],verbs[r[1]],adj[r[2]]],185,under_frame_y+(i+1)*30,False)


def resetColors():
    for b in list_buttons_content:
        if b['text'] in list_in_words:
            b.configure(bg='#2F4F4F',fg='white')
        if b['text'] not in nouns+verbs+adj:
            b.configure(bg='#f1f1f1',fg='black')


def reset(event):
    global list_buttons_chosen
    list_buttons_chosen=removeButtons(list_buttons_chosen)
    list_in_words = nouns + verbs + adj
    print(list_in_words)
    resetColors()
    

def sendComb(event):
    global list_in_words, list_buttons_chosen
    list_out_words = []

    for b in list_buttons_chosen:
        list_out_words.append(b['text'])

    f = open("Data/Data.txt",'a')
    for w in list_in_words:
        f.write(w + " ")
    f.write('\t')

    for w in list_out_words:
        f.write(w + " ")
    f.write('\n')
    


def getInfo(event):
    pass

books = [('the-little-prince','The Little Prince','Antoine de Saint Exupery'),
    ('to-kill-a-mocking-bird','To Kill a Mocking Bird','Harper Lee'),
    ('breakfast-at-tiffany',"Breakfast at Tiffany's",'Truman Capote')]

def openBooksList():
    global books_list
    books_list = Toplevel(window)
    books_list.title('Books List')
    books_list.geometry("400x600")

    for book in books:
        b = Button(books_list,text = book[1],command=books_list.destroy)
        b.place(x=30,y=30*books.index(book))
        b.configure(borderwidth=0)
        b.bind("<Button-1>", open_book) 
 

def openArticlesList():
    art_list = Toplevel(window)
    art_list.title('Articles List')
    art_list.geometry("400x600")


window = Tk()
window.geometry("1100x700")
window.title('Reading Assistant')



menubar = Menu(window)

# create a pulldown menu, and add it to the menu bar
filemenu1 = Menu(menubar, tearoff=0)
filemenu1.add_command(label="Book", command=openBooksList) # call open_book
filemenu1.add_command(label="Article", command=openArticlesList)
filemenu1.add_separator()
filemenu1.add_command(label="Exit", command=window.quit)

filemenu2 = Menu(menubar, tearoff=0)

menubar.add_cascade(label="Open", menu=filemenu1)
menubar.add_cascade(label="Info", menu=filemenu2) # call getInfo

window.config(menu=menubar)



label_paragraph = Label(window, text = "Paragraph:")
label_paragraph.place(x = 30, y = 60, width=100, height=25)
label_paragraph.configure(bg='black', fg='white')

content_frame = Frame(window,height=300, width=600, borderwidth=2, relief="groove") #, fg = '#003333'
content_frame.place(x = 140, y = 60)

button_prev_par = Button(window, text = "<<")
button_prev_par.place(x = 140, y = 30, width=30, height=25)
button_prev_par.bind("<Button-1>", prev_par)
button_prev_par.configure(bg='black',fg='white')

button_next_par = Button(window, text = ">>")
button_next_par.place(x = 170, y = 30, width=30, height=25)
button_next_par.bind("<Button-1>", next_par)
button_next_par.configure(bg='black',fg='white')

label_nouns2 = Label(window, text = "Nouns:", borderwidth=2, relief="groove")
label_nouns2.place(x = 185, y = under_frame_y, width=95, height=25)

label_actions2 = Label(window, text = "Actions:",borderwidth=2, relief="groove")
label_actions2.place(x = 285, y = under_frame_y, width=95, height=25)

label_adjectives2 = Label(window, text = "Adjectives:",borderwidth=2, relief="groove")
label_adjectives2.place(x = 385, y = under_frame_y, width=95, height=25)

button_hint=Button(window, text="Hint")
button_hint.place(x=90, y=under_frame_y, width=40, height=25)
button_hint.bind("<Button-1>", genComb)

label_check = Label(window, text='Check')
label_check.place(x=140, y=under_frame_y,width = 40, height=25)
label_check.configure(bg='black', fg='white')

button_reset=Button(window, text="Reset")
button_reset.place(x=505, y=under_frame_y+30, width=100, height=25)
button_reset.bind("<Button-1>", reset)

label_chosen = Label(window, text = "Chosen:")
label_chosen.place(x = 505, y = under_frame_y, width=100, height=25)
label_chosen.configure(bg='black', fg='white')

button_send = Button(window, text="Send")
button_send.place(x=505, y=under_frame_y+60, width=100, height=25)
button_send.bind("<Button-1>", sendComb)
button_send.configure(bg='black', fg='white')

window.mainloop()