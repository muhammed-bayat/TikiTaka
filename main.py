from tkinter import *
from tkinter import messagebox
import bluetooth

root = Tk()

sizex = 800
sizey = 500
posx = 40
posy = 20
root.title("TikiTaka")
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))


def yaz():
    nearby_devices = bluetooth.discover_devices(duration=2, lookup_names=True, flush_cache=True, lookup_class=False)
    lst.delete(0, END)
    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))
        lst.insert(END, name + ' || ' + addr)
        btn_baglan.pack(side='bottom', fill='both')
    if len(nearby_devices) < 1:
        lst.insert(END, "Eşleştirilebilir aygıt bulunamadı veya bluetooth kapalı")


def sec(event):
    widget = event.widget
    selection = widget.curselection()
    picked = widget.get(selection[0])
    addr = picked[-17:]
    return addr


def baglan():
    addr = lst.get(lst.curselection()[0])[-17:]

    messagebox.showinfo("Hata", "Bir cihaz seçin")

    print(addr)
    port = 4
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    try:
        sock.connect((addr, port))
        if lst.get(lst.curselection())[:8] != "Bağlandı":
            lst.insert(lst.curselection(), "Bağlandı - " + lst.get(lst.curselection()))
            lst.delete(lst.curselection())

    except Exception as e:
        messagebox.showinfo("Hata", "Bir hata ile karşılaşıldı: " + str(e))

    finally:
        sock.close()

lst = Listbox(root, font=("Courier", 15))
lst.insert(END, "Aygıtları listelemek için yenileyin")
lst.bind('<<ListboxSelect>>', sec)


btn_yenile = Button(root, font=("Courier", 15), command=yaz, text='Yenile', height=3)
btn_baglan = Button(root, font=("Courier", 15), comman=baglan, text="Bağlan", height=3)

btn_yenile.pack(side='bottom', fill='both')

lst.pack(side="top", fill="both", expand=True)
root.mainloop()
