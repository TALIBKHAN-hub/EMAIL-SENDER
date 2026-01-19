import customtkinter as ctk
import smtplib
from email.message import EmailMessage
import json
import os

app = ctk.CTk()
app.geometry("450x700+600+150")
app.title("EMAIL SENDER----TALIB")
app.resizable(False,False)

# ---------------------- PAGE SHOWING FUNCTION--------------------------

def show_page(frame):
    page1.pack_forget()
    page2.pack_forget()
    page3.pack_forget()
    page4.pack_forget()
    frame.pack(fill="both",expand=True)

# ------------------ PAGE1 == EMAIL FRONT PAGE--------------------------

page1 = ctk.CTkFrame(app,fg_color="#0f141a")

main_head = ctk.CTkLabel(
    page1,
    text="EMAIL SENDER",
    font = ("Verdana",30,"bold"),
    fg_color="#232a30",
    text_color="#AFACAC",
    corner_radius=40,
    padx=60,
    pady=3
).pack(pady=20)

list_frame = ctk.CTkScrollableFrame(
    page1,
    width=400,
    height=460,
    fg_color="transparent",
    corner_radius=15
)
list_frame.pack(pady=5)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMAIL_DATA_PATH = os.path.join(BASE_DIR, "email_data", "Emaildata.json")
SENDEMAIL_DATA_PATH = os.path.join(BASE_DIR, "email_data", "sendemail.json")

with open(EMAIL_DATA_PATH,"r") as file:
    data = json.load(file)

for i, value in enumerate(data["info"]):
    if len(value) > 0 and len(value) > 1:
        label = ctk.CTkLabel(
            list_frame,
            height=40,
            width=40,
            text=value[0].upper(),
            font = ("Verdana",30,"bold"),
            fg_color="#CA5C5C",
            text_color="#ffffff",
            corner_radius=20
        ).grid(row=i,column=0,sticky="e",pady=20)

        label_text = ctk.CTkButton(
            list_frame,
            text=value,
            height=40,
            font = ("Arial",20,"bold"),
            text_color="#ffffff",
            fg_color="#232a30",
            command=lambda user=i: open_email(user)
        ).grid(row=i,column=1,sticky="w",padx=20,pady=20)
    else:
        continue

button_frame = ctk.CTkFrame(
    page1,
    fg_color="transparent",
    height = 90
)
button_frame.pack(side="bottom",fill="x",padx=10,pady=10)

compose_btn = ctk.CTkButton(
    button_frame,
    text = "Compose",
    font = ("Tahoma",20,"bold"),
    command = lambda: show_page(page2),
    fg_color="#374955",
    text_color="#000000",
    width=50,
    height=50,
    corner_radius=20
).pack(side="right")


# ------------------ PAGE2 == EMAIL SENDING PAGE--------------------------
page2 = ctk.CTkFrame(app,fg_color="#0f141a")

from_txt = ctk.CTkLabel(
    page2,
    text = "FROM:",
    font = ("Verdana",20,"bold"),
).grid(row=0,column=0,padx=10,pady=10,sticky="w")

from_box = ctk.CTkLabel(
    page2,
    text="YOUR_EMAIL_ACCOUNT",
    justify="left",
    font = ("Arial",17),
    fg_color="#1D1B1B",
    corner_radius=10,
    width =300
).grid(row=0,column=1,pady=10)

to_txt = ctk.CTkLabel(
    page2,
    text = "TO:",
    font = ("Verdana",20,"bold"),
).grid(row=1,column=0,padx=10,pady=10,sticky="w")

to_box = ctk.CTkEntry(
    page2,
    placeholder_text="Enter HERE",
    justify="left",
    font = ("Arial",15),
    fg_color="#1D1B1B",
    corner_radius=10,
    border_width=2,
    border_color="#A3A2A2",
    width =300
)
to_box.grid(row=1,column=1,pady=10)

sbj_txt = ctk.CTkLabel(
    page2,
    text = "SUBJECT:",
    font = ("Verdana",20,"bold"),
).grid(row=2,column=0,padx=10,pady=10,sticky="w")

sbj_box = ctk.CTkEntry(
    page2,
    placeholder_text="Enter HERE",
    justify="left",
    font = ("Arial",15),
    fg_color="#1D1B1B",
    corner_radius=10,
    border_width=2,
    border_color="#A3A2A2",
    width =300
)
sbj_box.grid(row=2,column=1,pady=10)

msg_txt = ctk.CTkLabel(
    page2,
    text = "MESSAGE:",
    font = ("Verdana",20,"bold"),
).grid(row=3,column=0,padx=10,pady=10,sticky="n")

msg_box = ctk.CTkTextbox(
    page2,
    font = ("Arial",15),
    corner_radius=10,
    border_width=2,
    border_color="#A3A2A2",
    width =300,
    height=400
)
msg_box.grid(row=3,column=1,pady=10)


send_btn = ctk.CTkButton(
    page2,
    text="SEND",
    font = ("Tahoma",20,"bold"),
    command = lambda: on_send(),
    fg_color="#374955",
    text_color="#000000",
    width=50,
    height=50,
    corner_radius=20
).grid(row=4,column=1,pady=60,sticky="e")
    
back_btn = ctk.CTkButton(
    page2,
    text="BACK",
    font = ("Tahoma",20,"bold"),
    command = lambda: show_page(page1),
    fg_color="#374955",
    text_color="#000000",
    width=50,
    height=50,
    corner_radius=20
).grid(row=4,column=0,pady=60,padx=10,sticky="w")

# ------------------ PAGE3 == EMAIL SENDED PAGE--------------------------

page3 = ctk.CTkFrame(app,fg_color="#0f141a")

done_msg = ctk.CTkLabel(
    page3,
    text = "EMAIL SEND",
    text_color="#000000",
    fg_color="#72D4EC",
    font = ("Verdana",20,"bold"),
    corner_radius=20,
    height=100,
    width=300
).grid(row=0,column=0,padx=80,pady=250)

cross_btn = ctk.CTkButton(
    page3,
    text="OK",
    text_color="#ffffff",
    fg_color="#4d4a4a",
    command = lambda: (load_history(), show_page(page1)),
    width=20,
    height=20,
    corner_radius=10
).grid(row=1,column=0)


# ------------------ PAGE4 == EMAILCHECKING PAGE--------------------------
page4 = ctk.CTkFrame(app,fg_color="#0f141a")

from_txtdata = ctk.CTkLabel(
    page4,
    text = "FROM:",
    font = ("Verdana",20,"bold"),
).grid(row=0,column=0,padx=10,pady=10,sticky="w")

from_data = ctk.CTkLabel(
    page4,
    text="YOUR_EMAIL_ACCOUNT",
    font = ("Arial",17),
    fg_color="#1D1B1B",
    corner_radius=10,
    width =300
).grid(row=0,column=1,pady=10)

to_txtdata = ctk.CTkLabel(
    page4,
    text = "TO:",
    font = ("Verdana",20,"bold"),
).grid(row=1,column=0,padx=10,pady=10,sticky="w")

to_data = ctk.CTkLabel(
    page4,
    text="",
    font = ("Arial",15),
    fg_color="#1D1B1B",
    corner_radius=10,
    width =300
)
to_data.grid(row=1,column=1,pady=10)

sbj_txtdata = ctk.CTkLabel(
    page4,
    text = "SUBJECT:",
    font = ("Verdana",20,"bold"),
).grid(row=2,column=0,padx=10,pady=10,sticky="w")

sbj_data = ctk.CTkLabel(
    page4,
    text="",
    font = ("Arial",15),
    fg_color="#1D1B1B",
    corner_radius=10,
    width =300
)
sbj_data.grid(row=2,column=1,pady=10)

msg_txtdata = ctk.CTkLabel(
    page4,
    text = "MESSAGE:",
    font = ("Verdana",20,"bold"),
).grid(row=3,column=0,padx=10,pady=10,sticky="n")

msg_data = ctk.CTkTextbox(
    page4,
    font = ("Arial",15),
    fg_color="#1D1B1B",
    corner_radius=10,
    width =300,
    height = 400
)
msg_data.grid(row=3,column=1,pady=10)
msg_data.configure(state="disabled")

mainback_btn = ctk.CTkButton(
    page4,
    text="BACK",
    font = ("Tahoma",20,"bold"),
    command = lambda: show_page(page1),
    fg_color="#374955",
    text_color="#000000",
    width=50,
    height=50,
    corner_radius=20
).grid(row=4,column=0,pady=60,padx=10,sticky="w")

# ------------------ SENDING EMAIL PROCESS FUNCTION --------------------------

def on_send():
    to_msg = to_box.get()
    subj = sbj_box.get()
    body = msg_box.get("1.0", "end")
    
    send_mail(to_msg,subj,body)

# ------------------ FUNCTION TO LOAD THE HISTORY --------------------------

def load_history():
    # clear old widgets
    for widget in list_frame.winfo_children():
        widget.destroy()

    with open(EMAIL_DATA_PATH,"r") as file:
        data = json.load(file)

    for i, value in enumerate(data["info"]):
        if len(value) > 1:
            ctk.CTkLabel(
                list_frame,
                height=40,
                width=40,
                text=value[0].upper(),
                font=("Verdana",30,"bold"),
                fg_color="#CA5C5C",
                text_color="#ffffff",
                corner_radius=20
            ).grid(row=i,column=0,sticky="e",pady=20)

            ctk.CTkButton(
                list_frame,
                text=value,
                height=40,
                font=("Arial",20,"bold"),
                text_color="#ffffff",
                fg_color="#232a30",
                command=lambda user=i: open_email(user)
            ).grid(row=i,column=1,sticky="w",padx=20,pady=20)

# ------------------ FUNCTION TO SEND EMAIL --------------------------

def send_mail(to_msg,subj,body):

    sender_email = "YOUR_EMAIL_ACCOUNT"
    password = "YOUR_GMAIL_APP_PASSWORD"

    to_email = to_msg.strip().replace("\n", "")
    subject = subj.strip().replace("\n", "")
    
    with open(EMAIL_DATA_PATH,"r") as file:
        data = json.load(file)

    data["info"].append(to_msg)
    with open(EMAIL_DATA_PATH,"w") as f:
        json.dump(data, f)

    send_data = [to_msg,subj,body]

    with open(SENDEMAIL_DATA_PATH,"r") as dfile:
        allmsg_data = json.load(dfile)

    allmsg_data["data"].append(send_data)
    with open(SENDEMAIL_DATA_PATH,"w") as df:
        json.dump(allmsg_data,df)

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)

        # clear input fields
        to_box.delete(0, "end")
        sbj_box.delete(0, "end")
        msg_box.delete("1.0", "end")

        show_page(page3)

    except Exception as e:
        print("Error:", e)

# ------------------ FUNCTION TO SHOW THE OLD DATA --------------------------

def open_email(value):
    user_data = value
    with open(SENDEMAIL_DATA_PATH,"r") as file:
        data = json.load(file)

    user_add = data["data"][user_data][0]
    user_subj = data["data"][user_data][1]
    user_msg = data["data"][user_data][2]

    to_data.configure(text=user_add)
    sbj_data.configure(text=user_subj)
    msg_data.configure(state="normal")
    msg_data.delete("1.0", "end")
    msg_data.insert("1.0", user_msg)
    msg_data.configure(state="disabled")

    show_page(page4)

show_page(page1)
app.mainloop()