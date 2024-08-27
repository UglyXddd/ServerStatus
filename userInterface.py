import subprocess
import threading
import tkinter.ttk
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import schedule

import excel
import sys
import ping_file
import pyperclip
import tg_bot
import Main
import pandas as pd
import customtkinter as ctk
import PIL
from PIL import Image
import os
import json

category_and_IP = ["", "", ""]  # category, name, address
ctk.set_appearance_mode('light')
ctk.set_default_color_theme("theme.json")
global_data = ''


def check_ip_in_excel(enter_IP: str, begin_row='') -> bool:
    try:
        tmp = list(map(int, enter_IP.split('.')))
        if len(tmp) < 4 or any(True for i in tmp if i > 255 or i < 0) or enter_IP == begin_row:
            messagebox.showwarning("Ошибка", "Такого IP не может существовать.")
            return True
    except:
        messagebox.showerror("Ошибка", "Такого IP не может существовать.")
        return True
    for i in excel.read_col('Адреса-Микротов.xlsx', [i[0] for i in excel.HEADERS]).values.tolist():
        for j in i:
            if enter_IP == j:
                return True
    return False


def open_Agency_page():
    if not Agency_page_opened.get():
        global Agency_window, del_button, change_button, change_page_opened, global_data
        Agency_window = tk.Toplevel(root)
        Agency_window.title("Cтраница представительств")
        Agency_window.geometry("1920x1080")
        Agency_window.protocol("WM_DELETE_WINDOW",
                               lambda: close_page(Agency_page_opened, Agency_window, Agency_button, 'Agency'))
        Agency_window.bind("<F11>", toggle_fullscreen)
        Agency_window.bind("<Escape>", exit_fullscreen)

        columns = ("name", "ip", "status")
        tree = tk.ttk.Treeview(Agency_window, height=25, columns=columns, show="headings", style="Treeview")
        tree.tag_configure('green', foreground='green')
        tree.tag_configure('red', foreground='red')

        tree.place(anchor=tk.CENTER, rely=0.45, relx=0.5)
        tree.heading("name", text="Название", anchor='w')
        tree.heading("ip", text="IP", anchor='w')
        tree.heading("status", text="Статус", anchor='w')

        tree.column("#1", stretch=True, width=220)
        tree.column("#2", stretch=True, width=120)
        tree.column("#3", stretch=True, width=80)

        change_button = ctk.CTkButton(Agency_window, text="Изменить",
                                      command=lambda: open_change_page(int(tree.selection()[0]),
                                                                       global_data[0].values.tolist()[
                                                                           int(tree.selection()[0])], tree, 0))
        change_button.place(relx=0.45, rely=0.89, anchor=tk.CENTER)
        del_button = ctk.CTkButton(Agency_window, text="Удалить",
                                   command=lambda: delete_row(int(tree.selection()[0]), tree, 0))
        del_button.place(relx=0.55, rely=0.89, anchor=tk.CENTER)
        Agency_page_opened.set(True)
        Agency_button.configure(state=tk.DISABLED)
        Agency_window.update()
        tree = update_ip(tree, 0)
        tree.bind("<Control-Key-c>", lambda x: copy_from_treeview(tree, x))
        tree.bind('<ButtonRelease-3>', lambda x: copy_from_treeview(tree, x))
        schedule.every(1).minutes.do(lambda: update_ip(tree, 0)).tag('Agency')


def open_Sklad_page():
    global Sklad_window, global_data, change_page_opened, change_button, del_button
    if not Sklad_page_opened.get():
        Sklad_window = tk.Toplevel(root)
        Sklad_window.title("Cтраница складов")
        Sklad_window.geometry("1920x1080")
        Sklad_window.protocol("WM_DELETE_WINDOW",
                              lambda: close_page(Sklad_page_opened, Sklad_window, Sklad_button, 'Sklad'))
        Sklad_window.bind("<F11>", toggle_fullscreen)
        Sklad_window.bind("<Escape>", exit_fullscreen)

        columns = ("name", "ip", "status")
        tree = tk.ttk.Treeview(Sklad_window, height=25, columns=columns, show="headings", style="Treeview")
        tree.tag_configure('green', foreground='green')
        tree.tag_configure('red', foreground='red')

        tree.place(anchor=tk.CENTER, rely=0.45, relx=0.5)
        tree.heading("name", text="Название", anchor='w')
        tree.heading("ip", text="IP", anchor='w')
        tree.heading("status", text="Статус", anchor='w')

        tree.column("#1", stretch=True, width=220)
        tree.column("#2", stretch=True, width=120)
        tree.column("#3", stretch=True, width=80)

        # кнопка изменения
        change_button = ctk.CTkButton(Sklad_window, text="Изменить",
                                      command=lambda: open_change_page(int(tree.selection()[0]),
                                                                       global_data[1].values.tolist()[
                                                                           int(tree.selection()[0])], tree, 1))
        change_button.place(relx=0.45, rely=0.89, anchor=tk.CENTER)
        # кнопка удаления
        del_button = ctk.CTkButton(Sklad_window, text="Удалить",
                                   command=lambda: delete_row(int(tree.selection()[0]), tree, 1))
        del_button.place(relx=0.55, rely=0.89, anchor=tk.CENTER)

        Sklad_page_opened.set(True)
        Sklad_button.configure(state=tk.DISABLED)
        Sklad_window.update()
        tree = update_ip(tree, 1)
        tree.bind("<Control-Key-c>", lambda x: copy_from_treeview(tree, x))
        tree.bind('<ButtonRelease-3>', lambda x: copy_from_treeview(tree, x))
        schedule.every(1).minutes.do(lambda: update_ip(tree, 1)).tag('Sklad')


def open_Child_page():
    global Child_window, global_data, change_page_opened, change_button, del_button
    if not Child_page_opened.get():
        Child_window = tk.Toplevel(root)
        Child_window.title("Cтраница дочерних предприятий")
        Child_window.geometry("1920x1080")
        Child_window.protocol("WM_DELETE_WINDOW",
                              lambda: close_page(Child_page_opened, Child_window, Child_button, 'Child'))
        Child_window.bind("<F11>", toggle_fullscreen)
        Child_window.bind("<Escape>", exit_fullscreen)

        columns = ("name", "ip", "status")
        tree = tk.ttk.Treeview(Child_window, height=25, columns=columns, show="headings", style="Treeview")
        tree.tag_configure('green', foreground='green')
        tree.tag_configure('red', foreground='red')

        tree.place(anchor=tk.CENTER, rely=0.45, relx=0.5)
        tree.heading("name", text="Название", anchor='w')
        tree.heading("ip", text="IP", anchor='w')
        tree.heading("status", text="Статус", anchor='w')

        tree.column("#1", stretch=True, width=220)
        tree.column("#2", stretch=True, width=120)
        tree.column("#3", stretch=True, width=80)

        change_button = ctk.CTkButton(Child_window, text="Изменить",
                                      command=lambda: open_change_page(int(tree.selection()[0]),
                                                                       global_data[2].values.tolist()[
                                                                           int(tree.selection()[0])], tree, 2))
        change_button.place(relx=0.45, rely=0.89, anchor=tk.CENTER)

        # кнопка удаления
        del_button = ctk.CTkButton(Child_window, text="Удалить",
                                   command=lambda: delete_row(int(tree.selection()[0]), tree, 2))
        del_button.place(relx=0.55, rely=0.89, anchor=tk.CENTER)

        Child_page_opened.set(True)
        Child_button.configure(state=tk.DISABLED)
        Child_window.update()
        tree = update_ip(tree, 2)
        tree.bind("<Control-Key-c>", lambda x: copy_from_treeview(tree, x))
        tree.bind('<ButtonRelease-3>', lambda x: copy_from_treeview(tree, x))
        schedule.every(1).minutes.do(lambda: update_ip(tree, 2)).tag('Child')


def open_CentOffice_page():
    global CentOffice_window, global_data, change_page_opened, change_button, del_button
    if not CentOffice_page_opened.get():
        CentOffice_window = tk.Toplevel(root)
        CentOffice_window.title("Cтраница центрального офиса")
        CentOffice_window.geometry("1920x1080")
        CentOffice_window.protocol("WM_DELETE_WINDOW",
                                   lambda: close_page(CentOffice_page_opened, CentOffice_window, CentOffice_button,
                                                      'CentOffice'))
        CentOffice_window.bind("<F11>", toggle_fullscreen)
        CentOffice_window.bind("<Escape>", exit_fullscreen)

        columns = ("name", "ip", "status")
        tree = tk.ttk.Treeview(CentOffice_window, height=25, columns=columns, show="headings", style="Treeview")
        tree.tag_configure('green', foreground='green')
        tree.tag_configure('red', foreground='red')

        tree.place(anchor=tk.CENTER, rely=0.45, relx=0.5)
        tree.heading("name", text="Название", anchor='w')
        tree.heading("ip", text="IP", anchor='w')
        tree.heading("status", text="Статус", anchor='w')

        tree.column("#1", stretch=True, width=220)
        tree.column("#2", stretch=True, width=120)
        tree.column("#3", stretch=True, width=80)
        change_button = ctk.CTkButton(CentOffice_window, text="Изменить",
                                      command=lambda: open_change_page(int(tree.selection()[0]),
                                                                       global_data[3].values.tolist()[
                                                                           int(tree.selection()[0])], tree, 3))
        change_button.place(relx=0.45, rely=0.89, anchor=tk.CENTER)

        # кнопка удаления
        del_button = ctk.CTkButton(CentOffice_window, text="Удалить",
                                   command=lambda: delete_row(int(tree.selection()[0]), tree, 3))
        del_button.place(relx=0.55, rely=0.89, anchor=tk.CENTER)

        CentOffice_page_opened.set(True)
        CentOffice_button.configure(state=tk.DISABLED)
        CentOffice_window.update()
        tree = update_ip(tree, 3)
        tree.bind("<Control-Key-c>", lambda x: copy_from_treeview(tree, x))
        tree.bind('<ButtonRelease-3>', lambda x: copy_from_treeview(tree, x))
        schedule.every(1).minutes.do(lambda: update_ip(tree, 3)).tag('CentOffice')


def open_Korpus_page():
    global Korpus_window, global_data, change_page_opened, change_button, del_button
    if not Korpus_page_opened.get():
        Korpus_window = tk.Toplevel(root)
        Korpus_window.title("Cтраница корпусов")
        Korpus_window.geometry("1920x1080")
        Korpus_window.protocol("WM_DELETE_WINDOW",
                               lambda: close_page(Korpus_page_opened, Korpus_window, Korpus_button, 'Korpus'))
        Korpus_window.bind("<F11>", toggle_fullscreen)
        Korpus_window.bind("<Escape>", exit_fullscreen)

        columns = ("name", "ip", "status")
        tree = tk.ttk.Treeview(Korpus_window, height=25, columns=columns, show="headings", style="Treeview")
        tree.tag_configure('green', foreground='green')
        tree.tag_configure('red', foreground='red')

        tree.place(anchor=tk.CENTER, rely=0.45, relx=0.5)
        tree.heading("name", text="Название", anchor='w')
        tree.heading("ip", text="IP", anchor='w')
        tree.heading("status", text="Статус", anchor='w')

        tree.column("#1", stretch=True, width=220)
        tree.column("#2", stretch=True, width=120)
        tree.column("#3", stretch=True, width=80)

        change_button = ctk.CTkButton(Korpus_window, text="Изменить",
                                      command=lambda: open_change_page(int(tree.selection()[0]),
                                                                       global_data[4].values.tolist()[
                                                                           int(tree.selection()[0])], tree, 4))
        change_button.place(relx=0.45, rely=0.89, anchor=tk.CENTER)

        # кнопка удаления
        del_button = ctk.CTkButton(Korpus_window, text="Удалить",
                                   command=lambda: delete_row(int(tree.selection()[0]), tree, 4))
        del_button.place(relx=0.55, rely=0.89, anchor=tk.CENTER)
        Korpus_page_opened.set(True)
        Korpus_button.configure(state=tk.DISABLED)
        Korpus_window.update()
        tree = update_ip(tree, 4)
        tree.bind("<Control-Key-c>", lambda x: copy_from_treeview(tree, x))
        schedule.every(1).minutes.do(lambda: update_ip(tree, 4)).tag('Korpus')


def open_change_page(selected: int, data: list, tree: tk.ttk.Treeview, ind: int):
    global change_window
    if not change_page_opened.get():
        change_window = tk.Toplevel(root)
        change_window.title("Страница изменения IP")
        change_window.geometry("1920x1080")
        change_window.protocol("WM_DELETE_WINDOW",
                               lambda: close_page(change_page_opened, change_window, change_button))
        change_window.bind("<F11>", toggle_fullscreen)
        change_window.bind("<Escape>", exit_fullscreen)

        enter_ip = ctk.CTkEntry(change_window, width=180)
        enter_ip.insert(0, data[1])
        enter_ip.pack()

        enter_new_name = ctk.CTkEntry(change_window, width=180)
        enter_new_name.insert(0, data[0])
        enter_new_name.pack()

        ready_button = ctk.CTkButton(change_window, text="Сохранить",
                                     command=lambda: apply_change(selected, data, [enter_ip, enter_new_name], tree,
                                                                  ind))
        ready_button.pack()

        change_window.event_add('<<Paste>>', '<Control-igrave>')
        change_window.event_add("<<Copy>>", "<Control-ntilde>")

        change_page_opened.set(True)

        change_button.configure(state=tk.DISABLED)
    else:
        messagebox.showwarning("Ошибка", "Закройте страницу изменения и повторите попытку")


def open_add_page():
    global add_window

    def on_entry_focus_in(event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, tk.END)

    def on_entry_focus_out(event, entry, default_text):
        if entry.get() == "":
            entry.insert(0, default_text)

    if not add_page_opened.get():
        add_window = tk.Toplevel(root)
        add_window.geometry("400x400")
        add_window.protocol("WM_DELETE_WINDOW", lambda: close_page(add_page_opened, add_window, add_button))
        add_window.title("Страница добавления IP")

        add_page_opened.set(True)
        add_window.bind("<F11>", toggle_fullscreen)
        add_window.bind("<Escape>", exit_fullscreen)

        enter_name = ctk.CTkEntry(add_window, width=300, height=40)
        enter_name.insert(0, "Название")
        enter_name.pack(pady=10)
        enter_name.bind('<FocusIn>', lambda event: on_entry_focus_in(event, enter_name, "Название"))
        enter_name.bind('<FocusOut>', lambda event: on_entry_focus_out(event, enter_name, "Название"))

        enter_IP = ctk.CTkEntry(add_window, width=300, height=40)
        enter_IP.insert(0, "IP-адрес")
        enter_IP.pack(pady=10)
        enter_IP.bind('<FocusIn>', lambda event: on_entry_focus_in(event, enter_IP, "IP-адрес"))
        enter_IP.bind('<FocusOut>', lambda event: on_entry_focus_out(event, enter_IP, "IP-адрес"))

        OPTIONS = ["Представительство", "Склад", "Дочернее предприятие", "Центральный офис", "Корпус"]
        variable = tk.StringVar(add_window)
        variable.set(OPTIONS[0])  # default value

        def choice_func(choice):
            variable.set(choice)

        dropdown = ctk.CTkOptionMenu(add_window, values=OPTIONS, command=choice_func, anchor="center")
        dropdown.pack(pady=10)

        button = ctk.CTkButton(add_window, text="Добавить", width=20, height=30,
                               command=lambda: pick_category(variable, enter_name, enter_IP))
        button.pack(pady=10)
        add_window.event_add('<<Paste>>', '<Control-igrave>')
        add_window.event_add("<<Copy>>", "<Control-ntilde>")

        add_button.configure(state=tk.DISABLED)


def open_Offline_page():
    global Offline_window
    if not Offline_page_opened.get():
        Offline_window = tk.Toplevel(root)
        Offline_window.title("Страница нерабочих IP")
        Offline_window.geometry("1920x1080")
        Offline_window.protocol("WM_DELETE_WINDOW",
                                lambda: close_page(Offline_page_opened, Offline_window, Offline_button, 'Offline'))
        Offline_window.bind("<F11>", toggle_fullscreen)
        Offline_window.bind("<Escape>", exit_fullscreen)
        columns = ("name", "ip", "status")
        tree = tk.ttk.Treeview(Offline_window, height=25, columns=columns, show="headings", style="Treeview")

        tree.tag_configure('red', foreground='red')

        tree.place(anchor=tk.CENTER, rely=0.45, relx=0.5)
        tree.heading("name", text="Название", anchor='w')
        tree.heading("ip", text="IP", anchor='w')
        tree.heading("status", text="Статус", anchor='w')

        tree.column("#1", stretch=True, width=220)
        tree.column("#2", stretch=True, width=120)
        tree.column("#3", stretch=True, width=80)

        Offline_page_opened.set(True)
        Offline_button.configure(state=tk.DISABLED)

        Offline_window.update()
        tree = offline_ip(tree)
        tree.bind('<ButtonRelease-1>', lambda event: selectItem(tree, event))
        tree.bind("<Control-Key-c>", lambda x: copy_from_treeview(tree, x))
        tree.bind('<ButtonRelease-3>', lambda x: copy_from_treeview(tree, x))
        schedule.every(5).minutes.do(lambda: offline_ip(tree)).tag('Offline')


def on_entry_focus_in_mail(self, event, entry, default_text):
    if entry.get() == 'MAIL':
        entry.delete(0, tk.END)


def on_entry_focus_in_TG(event, entry, default_text):
    if default_text == entry.get() and default_text == 'TG':
        entry.delete(0, tk.END)


def on_entry_focus_out(event, entry, default_text='MAIL'):
    if entry.get() == "":
        entry.insert(0, default_text)


class CustomDropdown:
    def __init__(self, root):
        self.root = root
        self.emails = []

        self.emails = load_emails()

        self.combo_frame = tk.ttk.Frame(self.root)
        self.combo_frame.place(anchor=tk.CENTER, rely=0.05, relx=0.41)

        self.remove_button = ctk.CTkButton(self.combo_frame, text="-", command=self.remove_email, height=30,
                                           width=40)
        self.remove_button.pack(side=tk.LEFT)

        self.add_button = ctk.CTkButton(self.combo_frame, text="+", command=self.add_email, height=30, width=40)
        self.add_button.pack(side=tk.LEFT)

        self.entry_mail = ctk.CTkEntry(self.combo_frame, width=260)
        self.entry_mail.pack(side=tk.LEFT, padx=5)
        self.entry_mail.insert(0, 'MAIL')
        self.entry_mail.bind('<FocusIn>',
                             lambda event: on_entry_focus_in_mail(self, event, self.entry_mail, 'MAIL'))
        self.entry_mail.bind('<FocusOut>', lambda event: on_entry_focus_out(event, self.entry_mail))

        self.combo_arrow = tk.ttk.Label(self.combo_frame, text="▼", cursor="hand2")
        self.combo_arrow.pack(side=tk.LEFT)
        self.combo_arrow.bind('<Button-1>', self.toggle_dropdown)

        self.combo_listbox = tk.Listbox(self.root, bd=2)
        self.combo_listbox.bind('<<ListboxSelect>>', self.select_email)

        self.update_dropdown()

    def add_email(self):
        email = self.entry_mail.get()
        if email != "MAIL":
            if email:
                if email not in self.emails:
                    self.emails.append(email)
                    save_emails(self.emails)
                    self.update_dropdown()
                else:
                    messagebox.showerror("Ошибка", "Такой email уже есть в списке.")

    def remove_email(self):
        selected_index = self.combo_listbox.curselection()
        if selected_index:
            email = self.combo_listbox.get(selected_index)
            self.emails.remove(email)
            save_emails(self.emails)
            self.update_dropdown()

    def update_dropdown(self):
        self.combo_listbox.delete(0, tk.END)
        self.emails = load_emails()
        for email in self.emails:
            self.combo_listbox.insert(tk.END, email)

    def toggle_dropdown(self, event):
        if self.combo_listbox.winfo_ismapped():
            self.hide_dropdown()
        else:
            self.show_dropdown()

    def show_dropdown(self):
        x = self.combo_frame.winfo_rootx()
        y = self.combo_frame.winfo_rooty() + self.combo_frame.winfo_height()

        self.combo_listbox.place(x=x + 82, y=y - 30, width=250)
        self.combo_listbox.lift()

    def hide_dropdown(self):
        self.combo_listbox.place_forget()

    def select_email(self, event):
        selected_index = self.combo_listbox.curselection()
        if selected_index:
            email = self.combo_listbox.get(selected_index)
            self.entry_mail.delete(0, tk.END)
            self.entry_mail.insert(tk.END, email)

    def return_mail(self):
        return self.entry_mail

custom_dropdown = ''


def open_settings_page():
    global Settings_window, enter_mail, enter_TG, select_all_tg_button, select_all_mail_button
    if not Settings_page_opened.get():
        Settings_window = tk.Toplevel(root)
        Settings_window.title("Страница настроек")
        Settings_window.geometry("1920x1080")
        Settings_window.protocol("WM_DELETE_WINDOW",
                                 lambda: close_page(Settings_page_opened, Settings_window, settings_button))
        Settings_window.bind("<F11>", toggle_fullscreen)
        Settings_window.bind("<Escape>", exit_fullscreen)
        default_text = readFile()

        def reboot_bot():
            print("ребут прожался")
            tg_bot.main.is_updated = False

        #
        global custom_dropdown
        custom_dropdown = CustomDropdown(Settings_window)

        enter_TG = ctk.CTkEntry(Settings_window, width=200)
        enter_TG.insert(0, default_text[1])
        enter_TG.bind('<FocusIn>', lambda event: on_entry_focus_in_TG(event, enter_TG, default_text[1]))
        enter_TG.bind('<FocusOut>', lambda event: on_entry_focus_out(event, enter_TG, default_text[1]))

        enter_TG.place(anchor=tk.CENTER, rely=0.05, relx=0.56)
        save_button = ctk.CTkButton(Settings_window, text="Сохранить", width=40, height=40,
                                    command=lambda: save_notification(tree, enter_TG))
        save_button.place(anchor=tk.CENTER, rely=0.1, relx=0.5)

        select_all_button = ctk.CTkButton(Settings_window, text="Вбрать все", width=40, height=40,
                                          command=lambda: select_buttons(tree, 0))
        select_all_button.place(anchor=tk.CENTER, rely=0.2, relx=0.7)

        select_all_tg_button = ctk.CTkButton(Settings_window, text="Вбрать все тг", width=40, height=40,
                                             command=lambda: select_buttons(tree, 1))
        select_all_tg_button.place(anchor=tk.CENTER, rely=0.25, relx=0.7)

        select_all_mail_button = ctk.CTkButton(Settings_window, text="Вбрать все почты", width=40, height=40,
                                               command=lambda: select_buttons(tree, 2))
        select_all_mail_button.place(anchor=tk.CENTER, rely=0.3, relx=0.7)

        unselect_all_button = ctk.CTkButton(Settings_window, text="Убрать все", width=40, height=40,
                                            command=lambda: select_buttons(tree, 3))
        unselect_all_button.place(anchor=tk.CENTER, rely=0.35, relx=0.7)

        unselect_new_choose = ctk.CTkButton(Settings_window, text="Отменить выбор", width=40, height=40,
                                            command=lambda: select_buttons(tree, 4))

        unselect_new_choose.place(anchor=tk.CENTER, rely=0.4, relx=0.7)

        restart_bot = ctk.CTkButton(Settings_window, text="Перезапустить бота", width=40, height=40,
                                    command=lambda: reboot_bot())

        tree = tk.ttk.Treeview(Settings_window, height=25, columns=("name", "ip", "tg", "mail"), show="headings",
                               style="Treeview")
        tree.place(anchor=tk.CENTER, rely=0.54, relx=0.5)
        tree.heading("name", text="Название", anchor='w', command=lambda: sort(tree, 0, False))
        tree.heading("ip", text="IP", anchor='w', command=lambda: sort(tree, 1, False))
        tree.heading("tg", text="TG", anchor='w', command=lambda: sort(tree, 2, False))
        tree.heading("mail", text="MAIL", anchor='w', command=lambda: sort(tree, 3, False))

        tree.column("#1", stretch=True, width=220)
        tree.column("#2", stretch=True, width=120)
        tree.column("#3", stretch=True, width=50)
        tree.column("#4", stretch=True, width=60)
        tree.bind('<ButtonRelease-1>', lambda event: selectItem(tree, event))
        tree = settings_ip(tree, Settings_window)
        tree.bind('<ButtonRelease-3>', lambda x: copy_from_treeview(tree, x))
        Settings_window.event_add('<<Paste>>', '<Control-igrave>')
        Settings_window.event_add("<<Copy>>", "<Control-ntilde>")
        Settings_page_opened.set(True)
        settings_button.configure(state=tk.DISABLED)
        Settings_window.update()


def save_emails(emails):
    with open("mail_user.txt", "w") as file:
        json.dump(";".join(str(i) for i in emails), file)


def load_emails():
    try:
        with open("mail_user.txt", "r") as file:
            return file.read().replace('"', '').split(";")
    except FileNotFoundError:
        return []


def readFile():
    file_mail = 'mail_user.txt'
    file_bot = 'ApiBot.txt'
    mass = []
    if os.path.exists(file_mail):
        # Файл существует, читаем его содержимое
        with open(file_mail, 'r') as file:
            mass.append(file.readline())
    else:
        # Файл не существует
        mass.append("MAIL")

    if os.path.exists(file_bot):
        # Файл существует, читаем его содержимое
        with open(file_bot, 'r') as file:
            mass.append(file.readline())
    else:
        # Файл не существует
        mass.append("TG")
    return mass


def sort(tree, col, reverse):
    l = [(tree.set(k, col), k) for k in tree.get_children("")]
    l.sort(reverse=reverse)
    for index, (_, k) in enumerate(l):
        tree.move(k, "", index)
    tree.heading(col, command=lambda: sort(tree, col, not reverse))


def select_buttons(tree: tk.ttk.Treeview, ind_butt: int, coun=0):
    match ind_butt:
        case 0:
            for i in range(1, len(tree.get_children()) + 1):
                tree.set(i, '#3', '☑')
                tree.set(i, '#4', '☑')
        case 1:
            if coun == 0:
                select_all_tg_button.configure(text="Убрать все тг", command=lambda: select_buttons(tree, 1, 1))
                for i in range(1, len(tree.get_children()) + 1):
                    tree.set(i, '#3', '☑')

            elif coun == 1:
                select_all_tg_button.configure(text="Выбрать все тг", command=lambda: select_buttons(tree, 1, 0))
                for i in range(1, len(tree.get_children()) + 1):
                    tree.set(i, '#3', '☐')

        case 2:
            if coun == 0:
                select_all_mail_button.configure(text="Убрать все почты", command=lambda: select_buttons(tree, 2, 1))
                for i in range(1, len(tree.get_children()) + 1):
                    tree.set(i, '#4', '☑')

            elif coun == 1:
                select_all_mail_button.configure(text="Вбрать все почты", command=lambda: select_buttons(tree, 2, 0))
                for i in range(1, len(tree.get_children()) + 1):
                    tree.set(i, '#4', '☐')
        case 3:
            for i in range(1, len(tree.get_children()) + 1):
                tree.set(i, '#3', '☐')
                tree.set(i, '#4', '☐')
        case 4:
            tree = settings_ip(tree, Settings_window)


def save_notification(tree: tk.ttk.Treeview, enter_tg):
    global Settings_window
    row_list = []
    text2 = enter_tg.get()
    entery_mail = custom_dropdown.return_mail()
    lld = load_emails()
    lld.append(entery_mail.get())
    save_emails(lld)
    custom_dropdown.update_dropdown()
    if text2 != 'TG':
        with open('ApiBot.txt', 'w') as file:
            file.write(text2)  # Добавляем текст в файл c API бота
        for child in tree.get_children():
            row_list.append(tree.item(child)["values"])
        row_list = pd.DataFrame(row_list)
        row_list.to_csv('notification_data.csv', index=False)


def selectItem(tree: tk.ttk.Treeview, event: tk.Event):
    try:
        curItem = tree.item(tree.focus())
        col = tree.identify_column(event.x)
        ind = tree.selection()[0]
        if col == '#3':
            cell_value = curItem['values']
            if cell_value[2] == '☐':
                tree.set(ind, col, '☑')
            elif cell_value[2] == '☑':
                tree.set(ind, col, '☐')
        elif col == '#4':
            cell_value = curItem['values']
            if cell_value[3] == '☐':
                tree.set(ind, col, '☑')
            elif cell_value[3] == '☑':
                tree.set(ind, col, '☐')
    except:
        pass


def delete_row(selected: int, tree: tk.ttk.Treeview, ind: int):
    global global_data, change_page_opened
    if not change_page_opened.get():
        tree.delete(selected)
        global_data[ind] = pd.DataFrame([tree.item(child)["values"][:2] for child in tree.get_children()],
                                        columns=excel.HEADERS[ind])
        excel.unite_to_exel(global_data)
        global_data = excel.read_all('Адреса-Микротов.xlsx')
        tmp = threading.Thread(target=update_ip, args=(tree, ind))
        tmp.run()
        messagebox.showinfo("Успешно", "Строка успешно удалена")
    else:
        messagebox.showwarning("Ошибка", "Закройте страницу изменения и повторите попытку")


def apply_change(selected: int, data: list, data_change: list[tk.Entry, tk.Entry], tree: tk.ttk.Treeview, ind: int):
    global global_data
    if not all((check_ip_in_excel(data_change[0].get(), data),
                check_name_in_excel(data_change[1].get(), excel.HEADERS[ind][0]))):
        if len(data) == 2:
            data.append(ping_file.ping_func(data_change[0].get()))
        tmp = [data_change[1].get(), data_change[0].get(), data[2]]
        change_window.destroy()
        change_button.configure(state=tk.NORMAL)
        change_page_opened.set(False)
        tree.item(selected, values=tmp)
        global_data[ind] = pd.DataFrame([tree.item(child)["values"][:2] for child in tree.get_children()],
                                        columns=excel.HEADERS[ind])
        excel.unite_to_exel(global_data)
        global_data = excel.read_all('Адреса-Микротов.xlsx')
        change_window.destroy()
        change_button.configure(state=tk.NORMAL)
        change_page_opened.set(False)
        messagebox.showinfo("Успешно", "Строка успешно изменена")
    else:
        change_window.destroy()
        change_button.configure(state=tk.NORMAL)
        change_page_opened.set(False)
        messagebox.showwarning("Ошибка", "Данные одинаковые")


def close_page(page_opened: tk.BooleanVar, page: tk.Toplevel, button: tk.Button, task=False, code_close=0):
    global global_data
    if code_close == 1:
        pass
    else:
        if task:
            schedule.clear(task)
        page_opened.set(False)
        try:
            button.configure(state=tk.NORMAL)
        except Exception as e:
            print(e)
        finally:
            page.destroy()


def pick_category(variable: tk.Variable, enter_name: tk.Entry, enter_IP: tk.Entry):
    global global_data
    category_and_IP = ['', '', '']
    category_and_IP[0] = variable.get()
    category_and_IP[1] = enter_name.get()
    category_and_IP[2] = enter_IP.get()
    if enter_name.get() != "" and enter_name.get() != "Название":
        if check_name_in_excel(category_and_IP[1], category_and_IP[0]):
            messagebox.showwarning("Ошибка", "Такое имя уже существует")
        elif check_ip_in_excel(category_and_IP[2]):
            pass
        else:
            for i, item in enumerate(excel.HEADERS):
                if category_and_IP[0] in item:
                    ind = i
            global_data[ind].loc[len(global_data[ind].index)] = [category_and_IP[1], category_and_IP[2]]
            global_data[ind] = global_data[ind].sort_index()
            excel.unite_to_exel(global_data)
            global_data = excel.read_all('Адреса-Микротов.xlsx')
            close_page(add_page_opened, add_window, add_button)
            messagebox.showinfo("Успешно", "Успешно добавлено")
    else:
        messagebox.showwarning("Ошибка", "Некорректно введено название")


def check_name_in_excel(enter_name: str, variable) -> bool:
    df = pd.read_excel('Адреса-Микротов.xlsx')
    name_columns = df[variable]
    for i in name_columns:
        if enter_name == i:
            return True


def main_window_closed():
    subprocess.Popen("taskkill /F /IM Main.exe", shell=False, encoding='utf-8')


def toggle_fullscreen(event: tk.Event):  # Создаем функцию, связан
    state = event.widget.attributes("-fullscreen")
    event.widget.attributes("-fullscreen", not state)


def exit_fullscreen(event: tk.Event):  # Создаем функцию, связанную с событием нажатия клавиши
    event.widget.attributes("-fullscreen", False)
    event.widget.geometry("1920x1080")  # Устанавливаем размеры окна после выхода из полноэкранного режима
    event.widget.update_idletasks()


def update_ip(tree: tk.ttk.Treeview, ind: int) -> tk.ttk.Treeview:
    global global_data
    tree.delete(*tree.get_children())
    global_data[ind] = ping_file.transact_data(global_data[ind])
    for i, item in enumerate(global_data[ind].values.tolist()):
        if '✅' in item:
            tree.insert(parent="", index=i, iid=i, values=item, tags="green")
        else:
            tree.insert(parent="", index=i, iid=i, values=item, tags="red")
    return tree


def offline_ip(tree: tk.ttk.Treeview) -> tk.ttk.Treeview:
    global global_data
    tree.delete(*tree.get_children())
    for i in global_data:
        for _, item in enumerate(ping_file.transact_data(i).values.tolist()):
            if '🔴' in item:
                tree.insert(parent="", index=END, values=item, tags="red")
    return tree


def settings_ip(tree: tk.ttk.Treeview, window: tk.Toplevel) -> tk.ttk.Treeview:
    global global_data
    tree.delete(*tree.get_children())
    ind = counter()
    flag = True
    try:
        from_csv = pd.read_csv('notification_data.csv')
    except:
        flag = False
    for i in global_data:
        for y, item in enumerate(i.values.tolist()):
            item = item[:2]
            if flag:
                if (from_csv['0'] == item[0]).any() or (from_csv['1'] == item[1]).any():
                    tmp = from_csv[from_csv['0'] == item[0]]
                    tmp1 = from_csv[from_csv['1'] == item[1]]
                    if (tmp['2'] == '☑').any() or (tmp1['2'] == '☑').any():
                        item.append('☑')
                    elif (tmp['2'] == '☐').any() or (tmp1['2'] == '☐').any():
                        item.append('☐')
                    if (tmp['3'] == '☑').any() or (tmp1['3'] == '☑').any():
                        item.append('☑')
                    elif (tmp['3'] == '☐').any() or (tmp1['3'] == '☐').any():
                        item.append('☐')
            else:
                item.append('☐')
                item.append('☐')
            str_ind = int(ind())
            tree.insert(parent="", index=str_ind, iid=str_ind, values=item)
    return tree


def your_copy(tree, window):
    window.clipboard_clear()
    window.clipboard_append(tree.item(tree.selection()[0], option='text'))


def popup_menu(event, tree, popup1):
    tree.identify_row(event.y)
    popup1.post(event.x_root, event.y_root)


def counter():
    i = 0

    def inner():
        nonlocal i
        i += 1
        return i

    return inner


def update_data():
    global global_data
    global_data = excel.read_all('Адреса-Микротов.xlsx')


def copy_from_treeview(tree, event):
    copy_values = []
    for each in tree.selection():
        try:
            copy_values.append(str(tree.item(each)["values"][int(tree.identify_column(event.x).replace("#", "")) - 1]))
        except:
            pass

    pyperclip.copy("\n".join(copy_values))


def main():
    global global_data, Agency_page_opened, Sklad_page_opened, Child_page_opened, CentOffice_page_opened, Korpus_page_opened, Offline_page_opened, add_page_opened, change_page_opened, Settings_page_opened, root, add_button, settings_button, change_button, Agency_button, Sklad_button, Child_button, CentOffice_button, Korpus_button, Offline_button
    root = tk.Tk()
    logo_image = Image.open("logo_V1.png")
    logo_image = logo_image.resize((179, 55))  # Изменение размеров изображения по желанию

    # Создание объекта PhotoImage из изображения
    logo_photo = PIL.ImageTk.PhotoImage(logo_image)

    # Создание виджета Label с изображением
    logo_label = tk.Label(root, image=logo_photo)
    logo_label.place(x=880.5, y=100)  # Можно использовать pack или grid, если предпочтительно

    # Установка масштабирования для Label
    root.grid_rowconfigure(0, weight=1)  # Установка растягивания строки
    root.grid_columnconfigure(0, weight=1)  # Установка растягивания столбца

    root.geometry("1920x1080")
    update_data()
    schedule.every(2).minutes.do(update_data)
    krd = threading.Thread(target=Main.start_updataes, daemon=True)
    krd.start()
    root.title("Главная страница")
    Agency_page_opened, Sklad_page_opened, Child_page_opened, CentOffice_page_opened, Korpus_page_opened, Offline_page_opened, add_page_opened, Settings_page_opened = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", exit_fullscreen)

    style = tk.ttk.Style()
    style.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 11), padding=35,
                    rowheight=30)  # Стиль списка
    style.configure("Treeview.Heading", font=('Arial', 15, 'bold'))  # Заголовки

    # Изменение цвета текста выделенной строки
    style.map("Treeview", foreground=[("selected", "!disabled", "white")],
              background=[("selected", "!disabled", "#0a676e")])

    # создание кнопок
    button_font = ctk.CTkFont(family="Arial", size=20)

    Agency_button = ctk.CTkButton(root, font=button_font, width=300, height=120, text="Страница представительств",
                                  command=open_Agency_page, corner_radius=200)
    Agency_button.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

    Sklad_button = ctk.CTkButton(root, font=button_font, width=300, height=120, text="Страница складов",
                                 command=open_Sklad_page)
    Sklad_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    Child_button = ctk.CTkButton(root, font=button_font, width=300, height=120,
                                 text="Страница дочерних предприятий",
                                 command=open_Child_page)
    Child_button.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    CentOffice_button = ctk.CTkButton(root, font=button_font, width=300, height=120,
                                      text="Страница центрального офиса",
                                      command=open_CentOffice_page)
    CentOffice_button.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

    Korpus_button = ctk.CTkButton(root, font=button_font, width=300, height=120, text="Страница корпусов",
                                  command=open_Korpus_page)
    Korpus_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    Offline_button = ctk.CTkButton(root, font=button_font, width=300, height=120, text="Список оффлайн серверов",
                                   command=open_Offline_page)
    Offline_button.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

    add_button = ctk.CTkButton(root, font=button_font, width=300, height=120, text="Страница добавления",
                               command=open_add_page)
    add_button.place(relx=0.6, rely=0.8, anchor=tk.CENTER)

    settings_button = ctk.CTkButton(root, font=button_font, width=300, height=120, text="Настройки",
                                    command=open_settings_page)
    settings_button.place(relx=0.4, rely=0.8, anchor=tk.CENTER)

    change_page_opened = tk.BooleanVar()
    root.protocol("WM_DELETE_WINDOW", main_window_closed)
    root.mainloop()
