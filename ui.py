from tkinter import *
import query_proc


def entered(arg):                                   # on click of enter button
    res = query_proc.start(arg.lower())
    Result_Field['text'] = 'length = {}\n{}'.format(len(res), res)


root = Tk()
root.title('IR System')



master=LabelFrame(root,bg='grey',padx=40,pady=40,width=800,height=800)
master.pack()


title=Label(master,text="IR SYSTEM",font="Times 10 bold")
title.pack(pady=20)


Query_Frame=LabelFrame(master,text="Enter your query",font="Times 10 bold",bg='grey')
Query_Frame.pack(pady=20)


Query_Field=Entry(Query_Frame,width=100,bg="white",fg='black')
Query_Field.pack(pady=20)


b=Button(Query_Frame,text="Enter",command=lambda:entered(Query_Field.get()))
b.pack()


output=LabelFrame(master,text="Output",font="Times 10 bold",width=12000,height=50)
output.pack(pady=20)

Result_Field=Label(output,text="",width=200,font="Times 10 bold")
Result_Field.pack()
output.pack_propagate(0)
root.mainloop()