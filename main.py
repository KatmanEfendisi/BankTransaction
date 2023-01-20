import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar, DateEntry
import dbfile
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image



class Front:
    def __init__(self, master):
        self.obj = dbfile.OneUser()
        self.master = master
        self.login()


    def login(self):
        """LOGIN PAGE contains three actions - LOGIN, CREATE, Forgot Password"""
        try:
            self.frame_body.pack_forget()
            self.frame_menu.pack_forget()
            self.frame_header.pack_forget()
        except:
            pass

        self.master.geometry('640x360+300+100')
        self.master.title('Banka ')
        self.menu_count = 0
        self.logo = PhotoImage(file='logo.png').subsample(4, 4)

        self.frame_header = ttk.Frame(self.master)
        self.frame_header.pack()

        ttk.Label(self.frame_header, image=self.logo).grid(
            row=0, column=0, rowspan=3)
        ttk.Label(self.frame_header, text='Bankaya hoş geldiniz!').grid(
            row=0, column=1, columnspan=2)

        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))

        ttk.Label(self.frame_body, text='Kullanıcı Adı:').grid(
            row=0, column=1, padx=10, pady=10, sticky='sw')
        ttk.Label(self.frame_body, text='Şifre:').grid(
            row=1, column=1, padx=10, pady=10, sticky='sw')
        self.user = ttk.Entry(self.frame_body, width=24, font=('Arial', 10))
        self.psd = ttk.Entry(self.frame_body, width=24, font=('Arial', 10))
        self.user.grid(row=0, column=2)
        self.psd.grid(row=1, column=2)
        self.psd.config(show='*')

        def temp_action():
            self.log_name = self.user.get()
            self.log_pass = self.psd.get()

            self.uid, self.vname, self.vemail, self.vaddress, self.vdob, self.vphone, self.vpass, self.vupi, self.vrecent, self.profile_photo, self.ouid, self.vbank, self.vacc, self.vbal = self.obj.get_details(
                self.log_name)

            if self.log_name == self.vname and self.log_pass == self.vpass:
                messagebox.showinfo(
                    title='Hoş geldiniz', message='Hoş geldiniz {}'.format(self.log_name))
                self.home()
            else:
                messagebox.showerror(
                    title='Geçersiz', message='Lütfen kullanıcı adınızı veya şifrenizi kontrol edin')

        ttk.Button(self.frame_body, text="Kaydet", command=temp_action).grid(
            row=2, column=0, padx=10, pady=10, columnspan=2)
        ttk.Button(self.frame_body, text="Hesap oluştur", command=self.create).grid(
            row=2, padx=10, pady=10, column=2, stick='se')
        ttk.Button(self.frame_body, text="Parolanızı mı unuttunuz?", command=self.forgot).grid(
            row=3, column=1, columnspan=2, padx=10, pady=10)


    def forgot(self):
        """Forgot Page leads to entering email and expects otp, which will be sent to the email"""
        self.master.geometry('680x410+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        ttk.Label(self.frame_body, text='Email adresini gir:').grid(
            row=0, column=1, padx=10, pady=10, sticky='sw')
        self.otpemail = ttk.Entry(
            self.frame_body, width=24, font=('Arial', 10))
        self.otpemail.grid(row=0, column=2)

        def on_click_email():
            if self.obj.send_otp(self.otpemail.get()) == 1:
                messagebox.showinfo(
                    title='OTP gönderme', message='E-postaya gönderilen OTP: {}'.format(self.otpemail.get()))
                self.otppage()
            else:
                messagebox.showerror(
                    title='Geçersiz', message='Verilen e-postaya sahip bir hesap yok')
        ttk.Button(self.frame_body, text="OTP gönderme", command=on_click_email).grid(
            row=1, column=1, columnspan=2, padx=10, pady=10)
        ttk.Button(self.frame_body, text="İptal", command=self.already).grid(
            row=2, column=1, columnspan=2, padx=10, pady=10)

    def otppage(self):
        def temp_otp_action():
            self.otpvalue = self.otpvalue.get()
            if self.obj.check_otp(self.otpvalue):
                self.change_pass_in_otp()
            else:
                messagebox.showerror(
                    title='Geçersiz', message='Yanlış OTP')
                self.already()
        self.master.geometry('680x410+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))

        ttk.Label(self.frame_body, text='Otp yi girin: ').grid(
            row=0, column=1, padx=10, pady=10, sticky='sw')
        self.otpvalue = ttk.Entry(
            self.frame_body, width=24, font=('Arial', 10))
        self.otpvalue.grid(row=0, column=2)
        ttk.Button(self.frame_body, text="Giriş", command=temp_otp_action).grid(
            row=1, column=1, columnspan=2, padx=10, pady=10)
        ttk.Button(self.frame_body, text="İptal", command=self.already).grid(
            row=2, column=1, columnspan=2, padx=10, pady=10)

    def change_pass_in_otp(self):
        self.master.geometry('680x410+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        self.uid, self.vname, self.vemail, self.vaddress, self.vdob, self.vphone, self.vpass, self.vupi, self.vrecent, self.profile_photo, self.ouid, self.vbank, self.vacc, self.vbal = self.obj.get_details_email()
        self.password_change()

        def temp_pass_action():
            if self.edit_sp.get() == self.edit_fp.get():
                self.obj.otp_change_password(
                    self.otpemail.get(), self.edit_fp.get())
                messagebox.showinfo(title='Başarılı',
                                    message='Parola başarıyla değiştirildi')
                self.home()
            else:
                messagebox.showerror(
                    title='Geçersiz', message='Parolalar eşleşmedi')
        ttk.Button(self.frame_body, text='Kaydet', command=temp_pass_action).grid(
            row=3, padx=10, pady=10, column=0, columnspan=2)



    def edit_photo(self):
        """Here the image file will be saved as a blob to the database.
        We read the file in binary mode, and get the resultant file and pass to the database
        for updating the image column of the database."""
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File",
                                                   filetypes=(("Image files",
                                                               "*.jpg*"),
                                                              ("Image files",
                                                               "*.png*"),
                                                              ("Image files",
                                                               "*.gif*"),
                                                              ("Image files",
                                                               "*.jpeg*"),
                                                              ("all files",
                                                               "*.*")))
        if self.filename:
            with open(self.filename, 'rb') as file:
                self.imgobj = file.read()
            self.profile_photo = self.obj.insert_blob(self.imgobj)
            self.profile()

    def create_photo(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File",
                                                   filetypes=(("Image files",
                                                               "*.jpg*"),
                                                              ("Image files",
                                                               "*.png*"),
                                                              ("Image files",
                                                               "*.gif*"),
                                                              ("Image files",
                                                               "*.jpeg*"),
                                                              ("all files",
                                                               "*.*")))
        if self.filename:
            with open(self.filename, 'rb') as file:
                self.imgobj = file.read()

    def menu_ini(self):
        self.frame_menu = ttk.Frame(self.master)
        self.frame_menu.pack()
        self.frame_menu.config(relief=RIDGE)
        self.homebut = ttk.Button(
            self.frame_menu, text="Ana sayfa", command=self.home)
        self.homebut.grid(row=0, column=0)
        self.probut = ttk.Button(
            self.frame_menu, text="Profil", command=self.profile)
        self.probut.grid(row=0, column=1)
        self.fribut = ttk.Button(
            self.frame_menu, text="Arkadaşlar", command=self.friends)
        self.fribut.grid(row=0, column=2)
        self.tranbut = ttk.Button(
            self.frame_menu, text="Transfer miktarı", command=self.transfer)
        self.tranbut.grid(row=0, column=3)
        self.seabut = ttk.Button(
            self.frame_menu, text="Arama", command=self.search)
        self.seabut.grid(row=0, column=4)

    def home(self):
        """The home page shows the profile pic of the user, and basic description.
        The profile picture will be displayed only if the user has a profile picture uploaded."""
        if self.menu_count ==0:
            self.menu_ini()
            self.menu_count = 1

        self.master.geometry('640x430+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))

        if self.profile_photo:
            with open('current.jpg', 'wb') as file:
                file.write(self.profile_photo)

            image = Image.open('current.jpg')
            image = image.resize((80, 80))
            self.newpython = ImageTk.PhotoImage(image)

            ttk.Label(self.frame_body, image=self.newpython).grid(
                row=0, column=0)

        ttk.Button(self.frame_body, text="Hesap Bakiyesini Kontrol Edin",
                   command=self.check_balance).grid(row=1, padx=30, pady=5, column=1)
        ttk.Button(self.frame_body, text="Son İşlemleri Görüntüle",
                   command=self.transaction_history).grid(row=2, padx=30, pady=10, column=1)
        ttk.Button(self.frame_body, text="Kullanım Grafiğini Kontrol Edin",
                   command=self.graphpage).grid(row=3, padx=30, pady=10, column=1)
        ttk.Button(self.frame_body, text="Çıkış Yap", command=self.login).grid(
            row=4, padx=30, pady=10, column=1)
        ttk.Label(self.frame_body, wraplength=300, text="Bankaya hoş geldiniz. Bu, herkese hızlı bir şekilde para aktarmanın basit, hızlı ve zarif bir yoludur. Daha fazla özellik için keşfedin.").grid(
            row=0, padx=20, pady=30, column=1)

    def graphpage(self):
        """Utilizes the matplotlib graph inside a canvas which is from FigureCanvasTkAgg Class"""
        self.master.geometry('790x560+250+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        self.user_list = self.obj.retrieve_recent(self.uid)
        if self.user_list:
            self.user_list = eval(self.user_list)
            n = len(self.user_list)
            ttk.Button(self.frame_body, text="Geri dön", command=self.home).pack()
            ttk.Button(self.frame_body, text="Kullanım Geçmişini Temizle",
                       command=self.clear_usage).pack()
            fig = Figure(figsize=(5, 5))
            plot1 = fig.add_subplot(111)
            plot1.plot(range(n), self.user_list)
            plot1.set_xlabel('İşlemler')
            plot1.set_ylabel('Her İşlemden sonraki tutar')

            canvas = FigureCanvasTkAgg(fig, master=self.frame_body)
            canvas.draw()
            canvas.get_tk_widget().pack()
        else:
            self.master.geometry('640x430+300+100')
            ttk.Label(self.frame_body, text="Henüz İşlem Yapmadınız. ").grid(
                row=1, padx=5, pady=5, column=0)
            ttk.Button(self.frame_body, text='Geri dön',
                       command=self.home).grid(row=2, padx=5, pady=5, column=0, columnspan=2)

    def clear_usage(self):
        value = messagebox.askyesno(
            title='Kullanım Geçmişi Temizlensin mi?', message='Kullanım Geçmişi Temizlensin mi? Kullanım geçmişinizi silmek istediğinizden emin misiniz?')
        if value == True:
            self.obj.clear_recent(self.uid)
            self.home()

    def create(self):
        self.master.geometry('680x410+300+100')

        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))

        ttk.Label(self.frame_body, text="İsim: ").grid(
            row=0, padx=5, pady=5, column=0)
        ttk.Label(self.frame_body, text="Email: ").grid(
            row=1, padx=5, pady=5, column=0)
        ttk.Label(self.frame_body, text="DOB: ").grid(
            row=2, padx=5, pady=5, column=0)
        ttk.Label(self.frame_body, text="Telefon: ").grid(
            row=3, padx=5, pady=5, column=0)
        ttk.Label(self.frame_body, text="Adres: ").grid(
            row=4, padx=5, pady=5, column=0)
        ttk.Label(self.frame_body, text="Bir parola girin: ").grid(
            row=5, padx=5, pady=5, column=0)
        ttk.Label(self.frame_body, text="Şifreyi yeniden gir: ").grid(row=6,
                                                                    padx=5, pady=5, column=0)
        ttk.Label(self.frame_body, text="Banka: ").grid(
            row=0, padx=5, pady=5, column=2)
        ttk.Label(self.frame_body, text="Hesap numarası: ").grid(
            row=1, padx=5, pady=5, column=2)
        ttk.Label(self.frame_body, text="Bir UPI anahtarı girin: ").grid(
            row=2, padx=5, pady=5, column=2)
        ttk.Label(self.frame_body, text="UPI anahtarını tekrar girin: ").grid(row=3,
                                                                   padx=5, pady=5, column=2)
        ttk.Label(self.frame_body, text="Profil Resmi Yükle: ").grid(row=4,
                                                                         padx=5, pady=5, column=2)

        self.name = ttk.Entry(self.frame_body, text="İsim: ")
        self.name.grid(row=0, padx=5, pady=5, column=1)
        self.email = ttk.Entry(self.frame_body, text="Email: ")
        self.email.grid(row=1, padx=5, pady=5, column=1)

        self.dob = DateEntry(self.frame_body, width=18, background='lightblue', foreground='black',
                             borderwidth=2, year=2000, month=1, day=1, date_pattern='dd/MM/yyyy')
        self.dob.grid(row=2, padx=5, pady=5, column=1)

        self.phone = ttk.Entry(self.frame_body, text="Telefon: ")
        self.phone.grid(row=3, padx=5, pady=5, column=1)
        self.address = ttk.Entry(self.frame_body, text="Adres: ")
        self.address.grid(row=4, padx=5, pady=5, column=1)
        self.pswd = ttk.Entry(self.frame_body, text="Bir parola girin: ")
        self.pswd.grid(row=5, padx=5, pady=5, column=1)
        self.pswd.config(show='*')
        self.repswd = ttk.Entry(self.frame_body, text="Şifreyi yeniden gir: ")
        self.repswd.grid(row=6, padx=5, pady=5, column=1)
        self.repswd.config(show='*')

        self.bank = ttk.Combobox(self.frame_body, width=18)
        self.bank.grid(row=0, padx=5, pady=5, column=3)
        self.bank.set('Bankanızı seçin')
        self.bankoptions = ['Vakıfbank', 'Ziraat', 'Halkbank', 'Yapı Kredi']
        self.bank.config(values=self.bankoptions)

        self.acc = ttk.Entry(self.frame_body, text="Hesap numarası: ")
        self.acc.grid(row=1, padx=5, pady=5, column=3)
        self.upi = ttk.Entry(self.frame_body, text="Bir UPI anahtarı girin: ")
        self.upi.grid(row=2, padx=5, pady=5, column=3)
        self.upi.config(show='*')
        self.reupi = ttk.Entry(self.frame_body, text="UPI anahtarını tekrar girin: ")
        self.reupi.grid(row=3, padx=5, pady=5, column=3)
        self.reupi.config(show='*')
        button_explore = ttk.Button(self.frame_body,
                                    text="Profil Resmi Yükle",
                                    command=self.create_photo)
        button_explore.grid(column=3, row=4)

        ttk.Button(self.frame_body, text='Oluştur', command=self.temp_action2).grid(
            row=7, padx=5, pady=5, column=1, sticky='ne')
        ttk.Button(self.frame_body, text='İptal', command=self.edit_cancel_create).grid(
            row=7, padx=5, pady=5, column=2, sticky='nw')
        ttk.Label(self.frame_body, text='Zaten hesabınız var mı?').grid(
            row=8, padx=5, pady=5, column=1, columnspan=2)
        ttk.Button(self.frame_body, text='Kayıt ol',
                   command=self.already).grid(row=9, padx=5, pady=5, column=1, columnspan=2)

    def already(self):
        self.frame_header.pack_forget()
        self.frame_body.pack_forget()
        self.login()

    def temp_action2(self):
        self.vname = self.name.get()
        self.vemail = self.email.get()
        self.vdob = self.dob.get()
        self.vphone = self.phone.get()
        self.vaddress = self.address.get()
        self.vfirstpass = self.pswd.get()
        self.vsecondpass = self.repswd.get()
        self.vupi = self.upi.get()
        self.vreupi = self.reupi.get()
        self.vbank = self.bank.get()
        self.vacc = self.acc.get()

        print(self.vdob)
        pattern = re.match(
            r'[a-zA-Z0-9.-]+@[a-zA-z-]+\.(com|edu|net)', self.vemail)
        if not self.vname.isalpha():
            messagebox.showerror(title='Geçersiz isim',
                                 message='Lütfen geçerli bir isim girin')
            self.create()
        if not pattern:
            messagebox.showerror(title='Geçersiz e-posta',
                                 message='Lütfen geçerli eposta adresini giriniz')
            self.create()
        elif not self.vphone.isnumeric():
            messagebox.showerror(title='Geçersiz numara',
                                 message='Geçerli bir telefon numarası giriniz')
            self.create()

        elif self.vfirstpass != self.vsecondpass:
            messagebox.showerror(title='Geçersiz şifre',
                                 message="Şifreler eşleşmedi")
            self.create()
        elif self.vbank not in self.bankoptions:
            messagebox.showerror(title='Geçersiz Banka',
                                 message="Lütfen geçerli bir banka seçin")
            self.create()

        elif not self.vacc.isnumeric():
            messagebox.showerror(title='Geçersiz hesap numarası',
                                 message='Lütfen geçerli bir Hesap Numarası girin')
            self.create()
        elif self.vreupi != self.vupi:
            messagebox.showerror(title='Geçersiz UPI anahtarları',
                                 message="UPI Anahtarları eşleşmedi")
            self.create()

        else:
            if (self.obj.insert_record(self.vname, self.vemail, self.vdob, self.vphone, self.vaddress, self.vfirstpass, self.vupi, self.vbank, self.vacc)) == 1:

                messagebox.showinfo(
                    title='Hoşgeldiniz', message='Hoş geldin {}'.format(self.vname))
                self.uid, self.vname, self.vemail, self.vaddress, self.vdob, self.vphone, self.vpass, self.vupi, self.vrecent, self.profile_photo, self.ouid, self.vbank, self.vacc, self.vbal = self.obj.get_details(
                    self.vname)
                self.profile_photo = self.obj.insert_blob(self.imgobj)
                self.home()

            else:
                messagebox.showerror(
                    title='Geçersiz hesap', message='Belirtilen bankada hesap yok')

    def profile(self):
        self.master.geometry('640x540+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        #self.profile_photo contains the binary data. We are opening a new file, and naming it as jpg files
        #And then the self.profile_photo contents are written into the new file.
        if self.profile_photo:
            with open('current.jpg', 'wb') as file:
                file.write(self.profile_photo)

            image = Image.open('current.jpg')
            image = image.resize((80, 80))
            self.newpython = ImageTk.PhotoImage(image)

            ttk.Label(self.frame_body, image=self.newpython).grid(
                row=0, column=0, columnspan=2)

        ttk.Label(self.frame_body, text='İsim: ').grid(
            row=1, padx=10, pady=10, column=0, sticky='nw')
        ttk.Label(self.frame_body, text=self.vname).grid(
            row=1, padx=10, pady=10, column=1, sticky='nw')
        ttk.Label(self.frame_body, text='Email Adres: ').grid(
            row=2, padx=10, pady=10, column=0, sticky='nw')
        ttk.Label(self.frame_body, text=self.vemail).grid(
            row=2, padx=10, pady=10, column=1, sticky='nw')
        ttk.Label(self.frame_body, text='Doğum tarihi: ').grid(
            row=3, padx=10, pady=10, column=0, sticky='nw')
        ttk.Label(self.frame_body, text=self.vdob).grid(
            row=3, padx=10, pady=10, column=1, sticky='nw')
        ttk.Label(self.frame_body, text='Telefon: ').grid(
            row=4, padx=10, pady=10, column=0, sticky='nw')
        ttk.Label(self.frame_body, text=self.vphone).grid(
            row=4, padx=10, pady=10, column=1, sticky='nw')
        ttk.Label(self.frame_body, text='Adres: ').grid(
            row=5, padx=10, pady=10, column=0, sticky='nw')
        ttk.Label(self.frame_body, text=self.vaddress).grid(
            row=5, padx=10, pady=10, column=1, sticky='nw')
        ttk.Label(self.frame_body, text='Banka: ').grid(
            row=6, padx=10, pady=10, column=0, sticky='nw')
        ttk.Label(self.frame_body, text=self.vbank).grid(
            row=6, padx=10, pady=10, column=1, sticky='nw')
        ttk.Label(self.frame_body, text='Hesap numarası: ').grid(
            row=7, padx=10, pady=10, column=0, sticky='nw')
        ttk.Label(self.frame_body, text=self.vacc).grid(
            row=7, padx=10, pady=10, column=1, sticky='nw')
        ttk.Button(self.frame_body, text='Profili Düzenle', command=self.edit).grid(
            row=8, padx=10, pady=20, column=0, columnspan=2)

    def edit(self):
        self.master.geometry('640x520+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))

        ttk.Button(self.frame_body, text='Geri dön', command=self.profile).grid(
            row=6, padx=10, pady=10, column=0, sticky='nw')
        if self.profile_photo:
            with open('current.jpg', 'wb') as file:
                file.write(self.profile_photo)
            image = Image.open('current.jpg')
            image = image.resize((80, 80))
            self.newpython = ImageTk.PhotoImage(image)
            ttk.Label(self.frame_body, image=self.newpython).grid(
                row=0, column=0, columnspan=2)

        button_explore = ttk.Button(self.frame_body,
                                    text="Profil Resmini Değiştir/Yükle",
                                    command=self.edit_photo)
        button_explore.grid(column=0, row=1, columnspan=2)

        ttk.Label(self.frame_body, text='Email: ').grid(
            row=2, padx=10, pady=10, column=0)
        self.edit_mail = ttk.Entry(self.frame_body)
        self.edit_mail.grid(row=2, column=1)
        self.edit_mail.insert(0, self.vemail)

        ttk.Label(self.frame_body, text='Telefon: ').grid(
            row=3, padx=10, pady=10, column=0)
        self.edit_mob = ttk.Entry(self.frame_body)
        self.edit_mob.grid(row=3, column=1)
        self.edit_mob.insert(0, self.vphone)
        ttk.Label(self.frame_body, text='Adres: ').grid(
            row=4, padx=10, pady=10, column=0)
        self.edit_add = ttk.Entry(self.frame_body)
        self.edit_add.grid(row=4, column=1)
        self.edit_add.insert(0, self.vaddress)
        ttk.Button(self.frame_body, text='Kaydet', command=self.save_changes).grid(
            row=5, padx=10, pady=10, column=0, sticky='ne')
        ttk.Button(self.frame_body, text='İptal', command=self.edit_cancel).grid(
            row=5, padx=10, pady=10, column=1)
        ttk.Button(self.frame_body, text='Şifre değiştir', command=self.psd_change).grid(
            row=6, padx=10, pady=10, column=1, columnspan=2)

    def password_change(self):
        ttk.Label(self.frame_body, text='Yeni şifreyi girin: ').grid(
            row=1, padx=10, pady=10, column=0)
        self.edit_fp = ttk.Entry(self.frame_body)
        self.edit_fp.grid(row=1, column=1)
        self.edit_fp.config(show='*')
        ttk.Label(self.frame_body, text='Şifreyi yeniden gir: ').grid(row=2,
                                                                    padx=10, pady=10, column=0)
        self.edit_sp = ttk.Entry(self.frame_body)
        self.edit_sp.grid(row=2, column=1)
        self.edit_sp.config(show='*')

    def psd_change(self):
        self.master.geometry('640x440+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        ttk.Label(self.frame_body, text='Güncel şifrenizi giriniz: ').grid(
            row=0, padx=10, pady=10, column=0)
        self.check_pass = ttk.Entry(self.frame_body)
        self.check_pass.grid(row=0, column=1)
        self.check_pass.config(show='*')
        self.password_change()
        ttk.Button(self.frame_body, text='Kaydet', command=self.save_password).grid(
            row=3, padx=10, pady=10, column=0, columnspan=2)
        ttk.Button(self.frame_body, text='Geri dön', command=self.edit).grid(
            row=3, padx=10, pady=10, column=1, columnspan=2)

    def validate_password(self):
        print(self.check_pass, self.vpass)
        if self.check_pass.get() == self.vpass:
            if self.edit_sp.get() == self.edit_fp.get():
                self.obj.change_password(self.vname, self.edit_fp.get())
                messagebox.showinfo(title='Başarılı',
                                    message='Parola başarıyla değiştirildi')
                self.home()
            else:
                messagebox.showerror(
                    title='Geçersiz', message='Parolalar eşleşmedi')
        else:
            messagebox.showerror(title='Geçersiz', message='Geçersiz şifre')

    def save_password(self):
        self.validate_password()
        self.psd_change()

    def save_changes(self):
        temp = messagebox.askyesno(
            title='Parayı öde', message='Değişiklikleri kaydetmek istediğinizden emin misiniz?')
        if temp == True:
            self.vemail = self.edit_mail.get()
            self.vphone = self.edit_mob.get()
            self.vaddress = self.edit_add.get()
            self.obj.update_record(self.uid, self.vemail,
                                   self.vphone, self.vaddress)
            messagebox.showinfo(
                title='Başarılı', message='Profil bilgileri başarıyla değiştirildi')
            self.profile()

    def edit_cancel2(self):
        value = messagebox.askyesno(
            title='Değişiklikleri iptal et?', message='Değişikliklerinizi iptal etmek istediğinizden emin misiniz?')
        if value == True:
            self.acc_tran.delete(0, END)
            self.money_tran.delete(0, END)

    def edit_cancel_create(self):
        value = messagebox.askyesno(
            title='Değişiklikleri iptal et?', message='Değişikliklerinizi iptal etmek istediğinizden emin misiniz??')
        if value == True:
            self.name.delete(0, END)
            self.email.delete(0, END)
            self.dob.delete(0, END)
            self.phone.delete(0, END)
            self.address.delete(0, END)
            self.pswd.delete(0, END)
            self.repswd.delete(0, END)
            self.upi.delete(0, END)
            self.reupi.delete(0, END)

    def edit_cancel(self):
        newedit_mail = self.edit_mail.get()
        newedit_mob = self.edit_mob.get()
        newedit_add = self.edit_add.get()
        value = messagebox.askyesno(
            title='Değişiklikleri iptal et?', message='Değişikliklerinizi iptal etmek istediğinizden emin misiniz?')
        if value == True and newedit_mail != self.vemail:
            self.edit_mail.delete(0, END)
            self.edit_mail.insert(0, self.vemail)
            if newedit_mob != self.vphone:
                self.edit_mob.delete(0, END)
                self.edit_mob.insert(0, self.vphone)
            if newedit_add != self.vaddress:
                self.edit_add.delete(0, END)
                self.edit_add.insert(0, self.vaddress)

    def transaction_history_friend(self, value):
        """In this method, the transact table from the database is queried, where the user sent and the friend received
        or the user received from a friend. If the user was a sender in a transaction, a red colored label denotes
        a transaction history with the friend, money sent, and time. If the user was a receiver, then a green label
        indicates the same details"""
        self.master.geometry('740x560+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        up_body = ttk.Frame(self.frame_body)
        up_body.pack()
        up_body.config(relief=RIDGE, padding=(30, 15))
        canvas = Canvas(self.frame_body)
        self.scroll = ttk.Scrollbar(
            self.frame_body, orient=VERTICAL, command=canvas.yview)
        self.scrollable = ttk.Frame(canvas)
        self.scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        facc, self.friend_obj = self.obj.friend_info(value)
        self.vals = self.obj.transaction_history(self.vacc)
        if self.friend_obj:
            with open('friend.jpg', 'wb') as file:
                file.write(self.friend_obj)

            image = Image.open('friend.jpg')
            image = image.resize((80, 80))
            self.friend_image = ImageTk.PhotoImage(image)
            ttk.Label(up_body, text=value).grid(
                row=1, column=0)
            ttk.Label(up_body, image=self.friend_image).grid(
                row=0, column=0)

        else:
            ttk.Label(up_body, text=value).grid(
                row=0, column=0)
        ttk.Label(up_body, text="Son İşlemler", font="Times 16 bold").grid(
            row=2, column=0, padx=10, pady=1)
        canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        canvas.configure(yscrollcommand=self.scroll.set)
        for j, i in enumerate(self.vals):
            if str(i[0]) == self.vacc and str(i[1]) == facc:
                self.message = f'A gönderildi {i[5]} Rs. {i[2]} on {i[3][:19]}'
                ttk.Label(self.scrollable, text=self.message, foreground="red",
                          font="Times 14 bold").grid(row=j+1, column=0,  pady=10, sticky='w')
            elif str(i[1]) == self.vacc and str(i[0]) == facc:
                self.message = f'Alınan {i[4]} Rs. {i[2]} on {i[3]}'
                ttk.Label(self.scrollable, text=self.message,
                          foreground="green",
                          font="Times 14 bold").grid(row=j+1, column=0, pady=10, sticky='e')
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

    def friends(self):
        def pay_friend(value):
            self.frame_body.pack_forget()
            self.frame_body = ttk.Frame(self.master)
            self.frame_body.pack()
            self.frame_body.config(relief=RIDGE, padding=(30, 15))
            ttk.Label(self.frame_body, text="Miktarı girin").grid(
                row=0, padx=10, pady=10, column=0)
            self.money_tran_friend = ttk.Entry(self.frame_body)
            self.money_tran_friend.grid(row=0, padx=10, pady=10, column=1)
            ttk.Button(self.frame_body, text='Öde', command=lambda: self.pay_tran_friend(
                value)).grid(row=2, padx=10, pady=10, column=0, sticky='ne')
            ttk.Button(self.frame_body, text='İptal', command=self.edit_cancel2).grid(
                row=2, padx=10, pady=10, column=1)

        def pay_friend_interm(value):
            self.transaction_history_friend(value)
            ttk.Button(self.frame_body, text='Öde',
                       command=lambda: pay_friend(value)).pack()#callback to a local function
            ttk.Button(self.frame_body, text='Geri dön',
                       command=self.friends).pack()

        self.master.geometry('640x430+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        up_body = ttk.Frame(self.frame_body)
        up_body.pack()
        up_body.config(relief=RIDGE, padding=(30, 15))
        canvas = Canvas(self.frame_body)
        scroll = ttk.Scrollbar(
            self.frame_body, orient=VERTICAL, command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        self.vals = self.obj.transaction_history(self.vacc)
        ttk.Label(up_body, text="Arkadaşlar", font="Times 16 bold").grid(
            row=0, column=0, padx=10, pady=1)
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        self.friend_set = set()
        for j, i in enumerate(self.vals):
            if str(i[0]) == self.vacc or str(i[1]) == self.vacc:
                self.friend_set.add(i[5])
        self.friend_set.discard(self.vname)
        self.friend_set = list(self.friend_set)
        self.friend_list = self.friend_set.copy()
        while self.friend_set:
            value = self.friend_set.pop()
            ttk.Button(scrollable, text=value,
                       command=lambda value=value: pay_friend_interm(value)).pack()#callback to a local function
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def pay_tran_friend(self, value):
        self.text_for_check()
        ttk.Button(self.frame_body, text='Tamam', command=lambda: self.after_pay_tran_friend(
            value)).grid(row=1, padx=10, pady=10, column=1)

    def after_pay_tran_friend(self, value):
        self.hereamount = self.upi_validation()
        if self.hereamount == -1:
            messagebox.showerror(title='Geçersiz UPI anahtarı',
                                 message='Geçersiz UPI anahtarı')
            self.friends()
        else:
            friendmoney = self.money_tran_friend.get()
            if not friendmoney.isnumeric():
                messagebox.showerror(title='Geçersiz Nakit',
                                     message='Lütfen geçerli bir Nakit girin')
            else:
                temp = messagebox.askyesno(
                    title='Parayı öde', message='Ödemek istediğinden emin misin {} a:["{}"]'.format(friendmoney, value))
                if temp == True:
                    self.return_tran = self.obj.pay_friend(
                        self.uid, self.vname, value, int(friendmoney))
                    if self.return_tran == 'lowbal':
                        messagebox.showerror(
                            title='Yetersiz bakiye', message='Düşük Bakiye')
                    elif self.return_tran == -1:
                        messagebox.showerror(
                            title='Bir şeyler yanlış gitti', message='Lütfen hesap numarasını kontrol edin ve tekrar deneyin')
                    else:
                        messagebox.showinfo(
                            title='Başarılı', message='İşlem Başarılı')
                        self.friends()

    def text_for_check(self):
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        ttk.Label(self.frame_body, text="UPI anahtarınızı girin: ").grid(
            row=0, padx=10, pady=10, column=0)
        self.check_upi = ttk.Entry(self.frame_body)
        self.check_upi.grid(row=0, padx=10, pady=10, column=1)
        self.check_upi.config(show='*')

    def check_balance(self):
        self.text_for_check()
        ttk.Button(self.frame_body, text='OK', command=self.check_balance2).grid(
            row=1, padx=10, pady=10, column=1)

    def check_balance2(self):
        self.hereamount = self.upi_validation()
        if self.hereamount == -1:
            messagebox.showerror(title='Geçersiz UPI anahtarı',
                                 message='Geçersiz UPI anahtarı')
            self.home()
        else:
            ttk.Label(self.frame_body, text="Hesap Bakiyeniz:{} ".format(
                self.hereamount)).grid(row=0, padx=10, pady=10, column=0)
            ttk.Button(self.frame_body, text='Geri dön', command=self.home).grid(
                row=1, padx=10, pady=10, column=0)

    def upi_validation(self):
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        self.upi_val = self.check_upi.get()
        print(self.uid, self.upi_val, sep='\n')
        self.amount = self.obj.check_balance(self.uid, self.upi_val)
        return self.amount


    def transaction_history(self):
        """In this method, the transact table from the database is queried, where either sending or receiving
        the current user is involved. If the user was a sender in a transaction, a red colored label denotes
        a transaction history with receiver, money sent, and time. If the user was a receiver, then a green label
        indicates the same details"""
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        up_body = ttk.Frame(self.frame_body)
        up_body.pack()
        up_body.config(relief=RIDGE, padding=(30, 15))
        canvas = Canvas(self.frame_body)
        self.scroll = ttk.Scrollbar(
            self.frame_body, orient=VERTICAL, command=canvas.yview)
        self.scrollable = ttk.Frame(canvas)
        self.scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        self.vals = self.obj.transaction_history(self.vacc)
        ttk.Label(up_body, text="Son İşlemler", font="Times 16 bold").grid(
            row=0, column=0, padx=10, pady=1)
        canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        canvas.configure(yscrollcommand=self.scroll.set)
        for j, i in enumerate(self.vals):
            if str(i[0]) == self.vacc:
                self.message = f'a gönderildi {i[5]} Rs. {i[2]} on {i[3][:19]}'
                ttk.Label(self.scrollable, text=self.message, foreground="red",
                          font="Times 14 bold").grid(row=j+1, column=0,  pady=10, sticky='w')
            elif str(i[1]) == self.vacc:
                self.message = f'Alınan {i[4]} Rs. {i[2]} on {i[3]}'
                ttk.Label(self.scrollable, text=self.message,
                          foreground="green",
                          font="Times 14 bold").grid(row=j+1, column=0, pady=10, sticky='e')
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

    def transfer(self):
        self.master.geometry('640x430+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        ttk.Label(self.frame_body, text="Hesap Numarasını Girin").grid(
            row=0, padx=10, pady=10, column=0)
        ttk.Label(self.frame_body, text="Miktarı girin").grid(
            row=1, padx=10, pady=10, column=0)
        self.acc_tran = ttk.Entry(self.frame_body)
        self.acc_tran.grid(row=0, padx=10, pady=10, column=1)
        self.money_tran = ttk.Entry(self.frame_body)
        self.money_tran.grid(row=1, padx=10, pady=10, column=1)
        ttk.Button(self.frame_body, text='Öde', command=self.pay_tran).grid(
            row=2, padx=10, pady=10, column=0, sticky='ne')
        ttk.Button(self.frame_body, text='İptal', command=self.edit_cancel2).grid(
            row=2, padx=10, pady=10, column=1)

    def pay_tran(self):
        self.text_for_check()
        ttk.Button(self.frame_body, text='Tamam', command=self.after_pay_tran).grid(
            row=1, padx=10, pady=10, column=1)

    def after_pay_tran(self):
        self.hereamount = self.upi_validation()
        if self.hereamount == -1:
            messagebox.showerror(title='Geçersiz UPI anahtarı',
                                 message='Geçersiz UPI anahtarı')
            self.transfer()
        else:
            self.money_tr = self.money_tran.get()
            self.acc_tr = self.acc_tran.get()
            if not self.money_tr.isnumeric():
                messagebox.showerror(title='Geçersiz Nakit',
                                     message='Lütfen geçerli bir Nakit girin')
            elif not self.acc_tr.isnumeric():
                messagebox.showerror(
                    title='Geçersiz hesap numarası', message='Lütfen geçerli bir hesap numarası girin')
            elif self.acc_tr == self.vacc:
                messagebox.showerror(
                    title='Hesap Numarası size ait olamaz', message='Hesap numaranızı girdiniz')
            else:
                temp = messagebox.askyesno(
                    title='Parayı öde', message='Ödemek istediğinden emin misin {} hesabına:["{}"]'.format(self.money_tr, self.acc_tr))
                if temp == True:
                    self.return_tran = self.obj.pay(
                        self.acc_tr, int(self.money_tr))
                    if self.return_tran == 'lowbal':
                        messagebox.showerror(
                            title='Yetersiz bakiye', message='Düşük Bakiye')
                    elif self.return_tran == -1:
                        messagebox.showerror(
                            title='Bir şeyler yanlış gitti', message='Lütfen hesap numarasını kontrol edin ve tekrar deneyin')
                    else:
                        messagebox.showinfo(
                            title='Başarılı', message='İşlem Başarılı')
                        self.transfer()

    def search(self):
        def pay_friend(value):
            self.frame_body.pack_forget()
            self.frame_body = ttk.Frame(self.master)
            self.frame_body.pack()
            self.frame_body.config(relief=RIDGE, padding=(30, 15))
            ttk.Label(self.frame_body, text="Miktarı girin").grid(
                row=0, padx=10, pady=10, column=0)
            self.money_tran_friend = ttk.Entry(self.frame_body)
            self.money_tran_friend.grid(row=0, padx=10, pady=10, column=1)
            ttk.Button(self.frame_body, text='Öde', command=lambda: self.pay_tran_friend(
                value)).grid(row=2, padx=10, pady=10, column=0, sticky='ne')
            ttk.Button(self.frame_body, text='İptal', command=self.search).grid(
                row=2, padx=10, pady=10, column=1)

        def pay_friend_interm(value):
            self.transaction_history_friend(value)
            ttk.Button(self.frame_body, text='Öde',
                       command=lambda: pay_friend(value)).pack()
            ttk.Button(self.frame_body, text='Geri dön',
                       command=self.search).pack()

        def search_list():
            searchval = self.search_friend.get()
            resultname = self.obj.search_friend(searchval)
            if resultname != self.vname:
                ttk.Button(self.frame_body, text=resultname, command=lambda: pay_friend_interm(
                    resultname)).grid(row=3, padx=10, pady=10, column=0)
        self.master.geometry('640x430+300+100')
        self.frame_body.pack_forget()
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack()
        self.frame_body.config(relief=RIDGE, padding=(30, 15))
        self.search_var = StringVar()
        self.search_var.set('Arama işleminizi seçin')
        ttk.Label(self.frame_body, textvariable=self.search_var).grid(
            row=1, padx=10, pady=10, column=0)
        search_combo = ttk.Combobox(
            self.frame_body, textvariable=self.search_var)
        search_combo.grid(row=0, padx=10, pady=10, column=1)
        search_combo.set('Nasıl Arama Yapılacağını Belirtin: ')
        search_combo.config(values=('İsme Göre Ara: ', 'Telefona Göre Ara: '))
        self.search_friend = ttk.Entry(self.frame_body)
        self.search_friend.grid(row=1, padx=10, pady=10, column=1)
        self.search_result = ttk.Button(
            self.frame_body, text="Arama", command=search_list)
        self.search_result.grid(row=2, padx=10, pady=10, column=1)


root = Tk()
app = Front(root)
root.mainloop()
