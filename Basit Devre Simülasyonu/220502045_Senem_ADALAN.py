import tkinter as tk
from tkinter import Menu
import tkinter.messagebox as messagebox

# Global olarak seçilen kapı türünü ve özelliklerini saklayacak değişkenler
selected_gate = None
led_checkbox_var = None
gate_properties = {}
gate_instances = []
connection_elements = []

# Türkçe-İngilizce renk eşlemeleri
color_mapping = {
    "Kırmızı": "Red",
    "Yeşil": "Green",
    "Mavi": "Blue",
    "Sarı": "Yellow",
    "Pembe": "Pink",
    "Turuncu": "Orange",
    "Mor": "Purple",
    "Siyah": "Black",
    "Beyaz": "White",
    "Gri": "Gray",
    "Kahverengi": "Brown",
    "Lacivert": "Navy"
}

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Basit Mantık Devre Simülasyonu")
root.geometry("800x700")

# Sol çerçeve (300 px genişliğinde)
left_frame = tk.Frame(root, width=300, bg="lightgray")
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Sağ çerçeve (500 px genişliğinde)
right_frame = tk.Frame(root, width=500, bg="white", highlightbackground="black", highlightthickness=1)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Sağ çerçevede Uygulama Ekranı başlığı
app_screen_label = tk.Label(right_frame, text="Uygulama Ekranı", bg="white", font=("Arial", 16))
app_screen_label.pack(pady=10)

# Sağ çerçevede canvas oluştur
canvas = tk.Canvas(right_frame, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Sağ tıklama menüsü
def show_properties(event, element_type, properties):
    menu = Menu(root, tearoff=0)
    for key, value in properties.items():
        menu.add_command(label=f"{key}: {value}")
    menu.post(event.x_root, event.y_root)


def create_input_box(x, y, color="red", start_value="0"):
    square_size = 15
    square = canvas.create_rectangle(x, y, x + square_size, y + square_size, outline="black", fill=color)
    text_x = x + square_size / 2
    text_y = y + square_size / 2
    text = canvas.create_text(text_x, text_y, text=start_value, font=("Arial", 11), fill="white", anchor="center")

    def update_properties():
        properties = {"Etiket": "Giriş Kutusu", "Renk": canvas.itemcget(square, "fill"), "Başlangıç Değeri": canvas.itemcget(text, "text")}
        return properties

    gate_instances.append((square, text))

    def on_right_click(event):
        properties = update_properties()
        menu = Menu(root, tearoff=0)
        menu.add_command(label="Renk Değiştir", command=lambda: change_color("Giriş Kutusu", square))
        for key, value in properties.items():
            menu.add_command(label=f"{key}: {value}")
        menu.post(event.x_root, event.y_root)

    canvas.tag_bind(square, '<Button-3>', on_right_click)
    canvas.tag_bind(text, '<Button-3>', on_right_click)

    def start_move(event):
        canvas.scan_mark(event.x, event.y)

    def move_element(event):
        x0, y0 = canvas.coords(square)[:2]
        dx = event.x - x0
        dy = event.y - y0
        canvas.move(square, dx, dy)
        canvas.move(text, dx, dy)

    canvas.tag_bind(square, "<ButtonPress-1>", start_move)
    canvas.tag_bind(square, "<B1-Motion>", move_element)
    canvas.tag_bind(text, "<ButtonPress-1>", start_move)
    canvas.tag_bind(text, "<B1-Motion>", move_element)

    def change_value(event):
        current_value = canvas.itemcget(text, "text")
        new_value = "1" if current_value == "0" else "0"
        canvas.itemconfig(text, text=new_value)

    canvas.tag_bind(text, "<Double-1>", change_value)

    def print_value():
        print(f"Giriş Kutusu Değeri: {canvas.itemcget(text, 'text')}")

    return square, text, print_value


# LED ve Çıkış Kutusu'nu oluşturmak için create_output_box fonksiyonu:
def create_output_box(x, y, is_led=False):
    square_size = 15
    square = canvas.create_oval(x, y, x + square_size, y + square_size, outline="black", fill="red")
    text_x = x + square_size / 2
    text_y = y + square_size / 2
    text = canvas.create_text(text_x, text_y, text="", font=("Arial", 11), fill="white", anchor="center")
    
    def update_properties():
        etiket = "LED" if is_led else "Çıkış Kutusu"
        properties = {"Etiket": etiket, "Renk": canvas.itemcget(square, "fill"), "Sonuç": canvas.itemcget(text, "text")}
        return properties

    def on_right_click(event):
        properties = update_properties()
        menu = Menu(root, tearoff=0)
        menu.add_command(label="Renk Değiştir", command=lambda: change_color_output_box(square))
        for key, value in properties.items():
            menu.add_command(label=f"{key}: {value}")
        menu.post(event.x_root, event.y_root)

    canvas.tag_bind(square, '<Button-3>', on_right_click)
    canvas.tag_bind(text, '<Button-3>', on_right_click)

    return square, text


def change_color(element_type, item):
    color_var = tk.StringVar()
    color_var.set("Kırmızı")  # Varsayılan renk

    dialog = tk.Toplevel(root)
    dialog.title("Renk Değiştir")
    dialog.geometry("200x100")

    label = tk.Label(dialog, text=f"Yeni renk seçiniz:")
    label.pack(pady=(5, 3))

    color_menu = tk.OptionMenu(dialog, color_var, *color_mapping.keys())
    color_menu.pack(pady=(0, 5))

    def submit_color():
        color = color_mapping[color_var.get()]  # Türkçe rengi İngilizceye çevir
        canvas.itemconfig(item, fill=color)
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Tamam", command=submit_color)
    submit_button.pack(pady=(1, 10))


def change_color_output_box(item):
    color_var = tk.StringVar()
    color_var.set("Kırmızı")  # Varsayılan renk

    dialog = tk.Toplevel(root)
    dialog.title("Renk Değiştir")
    dialog.geometry("200x100")

    label = tk.Label(dialog, text=f"Yeni renk seçiniz:")
    label.pack(pady=(5, 3))

    color_menu = tk.OptionMenu(dialog, color_var, *color_mapping.keys())
    color_menu.pack(pady=(0, 5))

    def submit_color():
        color = color_mapping[color_var.get()]  # Türkçe rengi İngilizceye çevir
        canvas.itemconfig(item, fill=color)
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Tamam", command=submit_color)
    submit_button.pack(pady=(1, 10))


# Kapı oluşturma ve sağ tıklama işlevselliği
def create_gate_with_inputs(gate_name, input_count):
    gate_width = 100
    gate_height = 60
    gate_x = 150
    gate_y = 100

    # Dikdörtgen oluştur
    gate_rect = canvas.create_rectangle(gate_x, gate_y, gate_x + gate_width, gate_y + gate_height, fill="white", outline="black")
    gate_text = canvas.create_text(gate_x + gate_width / 2, gate_y + gate_height / 2, text=gate_name)
    
    # Giriş çizgilerini ve giriş kutularını oluştur
    input_lines = []
    input_boxes = []  # Yeni eklenen giriş kutularını saklamak için liste
    for i in range(int(input_count)):
        line_y = gate_y + (i + 1) * (gate_height / (int(input_count) + 1))
        input_line = canvas.create_line(gate_x - 20, line_y, gate_x, line_y)
        input_lines.append(input_line)

        # Giriş kutusu oluştur ve print_value fonksiyonunu al
        input_box_x = gate_x - 35  # Gate'in solundan 35 piksel solunda
        input_box_y = line_y - 7.5  # Çizgiye göre hizalama
        input_box, input_text, print_value = create_input_box(input_box_x, input_box_y)
        input_boxes.append((input_box, input_text))

    # Çıkış çizgisini oluştur
    output_line = canvas.create_line(gate_x + gate_width, gate_y + gate_height / 2, gate_x + gate_width + 20, gate_y + gate_height / 2)

    gate_instances.append((gate_rect, gate_text, input_lines, output_line, input_boxes))

    def on_right_click(event):
        properties = {"Etiket": gate_name, "Bağlantı Giriş Sayısı": input_count}
        show_properties(event, gate_name, properties)

    canvas.tag_bind(gate_rect, '<Button-3>', on_right_click)
    canvas.tag_bind(gate_text, '<Button-3>', on_right_click)

    def start_move(event):
        canvas.scan_mark(event.x, event.y)

    def move_gate(event):
        x, y = canvas.coords(gate_rect)[:2]
        dx = event.x - x
        dy = event.y - y
        canvas.move(gate_rect, dx, dy)
        canvas.move(gate_text, dx, dy)
        for line in input_lines:
            canvas.move(line, dx, dy)
        for box, text in input_boxes:
            canvas.move(box, dx, dy)
            canvas.move(text, dx, dy)
        canvas.move(output_line, dx, dy)

    canvas.tag_bind(gate_rect, "<ButtonPress-1>", start_move)
    canvas.tag_bind(gate_rect, "<B1-Motion>", move_gate)
    canvas.tag_bind(gate_text, "<ButtonPress-1>", start_move)
    canvas.tag_bind(gate_text, "<B1-Motion>", move_gate)

    return print_value


# Giriş kutusu oluşturma ve sağ tıklama işlevselliği
def create_io_image(element_type, label, color=None, start_value=None):
    if element_type == "Çıkış Kutusu" or element_type == "LED":
        radius = 7.5
        x, y = 50, 50  
        circle = canvas.create_oval(x, y, x + 2 * radius, y + 2 * radius, outline="black", fill=color)

        def update_properties():
            properties = {"Etiket": element_type, "Renk": canvas.itemcget(circle, "fill")}
            return properties

        gate_instances.append((circle,))

        def on_right_click(event):
            properties = update_properties()
            menu = Menu(root, tearoff=0)
            menu.add_command(label="Renk Değiştir", command=lambda: change_color(element_type, circle))
            for key, value in properties.items():
                menu.add_command(label=f"{key}: {value}")
            menu.post(event.x_root, event.y_root)

        canvas.tag_bind(circle, '<Button-3>', on_right_click)

        def start_move(event):
            canvas.scan_mark(event.x, event.y)

        def move_element(event):
            x0, y0, _, _ = canvas.coords(circle)
            dx = event.x - x0
            dy = event.y - y0
            canvas.move(circle, dx, dy)

        canvas.tag_bind(circle, "<ButtonPress-1>", start_move)
        canvas.tag_bind(circle, "<B1-Motion>", move_element)
    else:
        square_size = 15
        x, y = 100, 100  
        square = canvas.create_rectangle(x, y, x + square_size, y + square_size, outline="black", fill=color)
        text_x = x + square_size / 2
        text_y = y + square_size / 2
        text = canvas.create_text(text_x, text_y, text=start_value, font=("Arial", 11), fill="white", anchor="center")

        def update_properties():
            properties = {"Etiket": element_type, "Renk": canvas.itemcget(square, "fill"), "Başlangıç Değeri": canvas.itemcget(text, "text")}
            return properties

        gate_instances.append((square, text))

        def on_right_click(event):
            properties = update_properties()
            menu = Menu(root, tearoff=0)
            menu.add_command(label="Renk Değiştir", command=lambda: change_color(element_type, square))
            for key, value in properties.items():
                menu.add_command(label=f"{key}: {value}")
            menu.post(event.x_root, event.y_root)

        canvas.tag_bind(square, '<Button-3>', on_right_click)
        canvas.tag_bind(text, '<Button-3>', on_right_click)

        def start_move(event):
            canvas.scan_mark(event.x, event.y)

        def move_element(event):
            x0, y0 = canvas.coords(square)[:2]
            dx = event.x - x0
            dy = event.y - y0
            canvas.move(square, dx, dy)
            canvas.move(text, dx, dy)

        canvas.tag_bind(square, "<ButtonPress-1>", start_move)
        canvas.tag_bind(square, "<B1-Motion>", move_element)
        canvas.tag_bind(text, "<ButtonPress-1>", start_move)
        canvas.tag_bind(text, "<B1-Motion>", move_element)

        def change_value(event):
            current_value = canvas.itemcget(text, "text")
            new_value = "1" if current_value == "0" else "0"
            canvas.itemconfig(text, text=new_value)

        canvas.tag_bind(text, "<Double-1>", change_value)

        def start_move(event):
            canvas.scan_mark(event.x, event.y)

        def move_element(event):
            x0, y0 = canvas.coords(square)[:2]
            dx = event.x - x0
            dy = event.y - y0
            canvas.move(square, dx, dy)
            canvas.move(text, dx, dy)

        canvas.tag_bind(square, "<ButtonPress-1>", start_move)
        canvas.tag_bind(square, "<B1-Motion>", move_element)
        canvas.tag_bind(text, "<ButtonPress-1>", start_move)
        canvas.tag_bind(text, "<B1-Motion>", move_element)

        def change_value(event):
            current_value = canvas.itemcget(text, "text")
            new_value = "1" if current_value == "0" else "0"
            canvas.itemconfig(text, text=new_value)

        canvas.tag_bind(text, "<Double-1>", change_value)


def create_connection_line(color, label):
    # Çizginin başlangıç ve bitiş noktalarının koordinatları
    start_x, start_y = None, None
    line = canvas.create_line(0, 0, 0, 0, fill=color, width=2, tags=label)

    # Başlangıç noktasını güncelleyen fonksiyon
    def start_draw(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    def draw_line(event):
        nonlocal start_x, start_y
        end_x, end_y = event.x, event.y
        canvas.coords(line, start_x, start_y, end_x, end_y)

    def update_properties():
        properties = {"Etiket": "Çizgi Çizme", "Renk": canvas.itemcget(line, "fill")}
        return properties

    def on_right_click(event):
        properties = update_properties()
        menu = Menu(root, tearoff=0)
        menu.add_command(label="Renk Değiştir", command=lambda: change_color("Çizgi Çizme", line))
        for key, value in properties.items():
            menu.add_command(label=f"{key}: {value}")
        menu.post(event.x_root, event.y_root)
        canvas.unbind("<Button-1>")
        canvas.unbind("<B1-Motion>")

    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw_line)

    canvas.tag_bind(line, '<Button-3>', on_right_click)

    def end_draw(event):
        canvas.unbind("<Button-1>")
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<ButtonRelease-1>")

    canvas.bind("<ButtonRelease-1>", end_draw)


def create_connection_node(color):
    x1, y1 = 50, 50
    x2, y2 = 65, 65
    round_radius = 3  # Yumuşatma yarıçapı

    # Dikdörtgenin köşelerini yuvarlatmak için köşelerdeki noktaları hesapla
    points = [x1 + round_radius, y1,x2 - round_radius, y1,x2, y1 + round_radius,x2, y2 - round_radius,x2 - round_radius, y2,x1 + round_radius, y2,x1, y2 - round_radius,x1, y1 + round_radius]

    node = canvas.create_polygon(points, outline="black", fill=color)
    connection_elements.append(node)

    def start_move(event):
        canvas.scan_mark(event.x, event.y)

    def move_node(event):
        x, y = canvas.coords(node)[:2]
        canvas.move(node, event.x - x, event.y - y)

    canvas.tag_bind(node, "<ButtonPress-1>", start_move)
    canvas.tag_bind(node, "<B1-Motion>", move_node)

    def update_properties():
        properties = {"Etiket": "Bağlantı Düğümü", "Renk": canvas.itemcget(node, "fill")}
        return properties

    def on_right_click(event):
        properties = update_properties()
        menu = Menu(root, tearoff=0)
        menu.add_command(label="Renk Değiştir", command=lambda: change_color("Bağlantı Düğümü", node))
        for key, value in properties.items():
            menu.add_command(label=f"{key}: {value}")
        menu.post(event.x_root, event.y_root)

    canvas.tag_bind(node, '<Button-3>', on_right_click)


# Kapı özellikleri diyalogları
def open_gate_properties_dialog(gate_name):
    global led_checkbox_var
    dialog = tk.Toplevel(root)
    dialog.title(f"{gate_name} Özellikleri")
    dialog.geometry("300x150")

    label = tk.Label(dialog, text=f"{gate_name} için bağlantı giriş sayısını giriniz:")
    label.pack(pady=(5, 3))

    input_count_label = tk.Label(dialog, text="Bağlantı Giriş Sayısı:")
    input_count_label.pack(pady=(5, 2))
    input_count_entry = tk.Entry(dialog)
    input_count_entry.pack(pady=(0, 5))

    led_checkbox_var = tk.BooleanVar()
    led_checkbox = tk.Checkbutton(dialog, text="LED mi?", variable=led_checkbox_var)
    led_checkbox.pack()

    def submit_properties():
        input_count = input_count_entry.get()
        create_gate_with_inputs(gate_name, input_count)
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Tamam", command=submit_properties)
    submit_button.pack(pady=(1, 10))

    def show_gate_properties(event):
        properties = {"Etiket": gate_name, "Bağlantı Giriş Sayısı": input_count_entry.get()}
        show_properties(event, gate_name, properties)

    dialog.bind('<Button-3>', show_gate_properties)


def open_io_properties_dialog(element_type):
    dialog = tk.Toplevel(root)
    dialog.title(f"{element_type} Özellikleri")
    dialog.geometry("300x200")

    if element_type == "Giriş Kutusu":
        label = tk.Label(dialog, text=f"{element_type} için renk ve başlangıç bilgilerini giriniz:")
        label.pack(pady=(5, 3))
    else:
        label = tk.Label(dialog, text=f"{element_type} için renk bilgisini seçiniz:")
        label.pack(pady=(5, 3))

    color_label = tk.Label(dialog, text="Renk:")
    color_label.pack(pady=(5, 2))
    color_var = tk.StringVar(dialog)
    color_var.set("Kırmızı")  # Varsayılan renk
    color_menu = tk.OptionMenu(dialog, color_var, *color_mapping.keys())
    color_menu.pack(pady=(0, 5))

    if element_type == "Giriş Kutusu":
        start_value_label = tk.Label(dialog, text="Başlangıç Değeri:")
        start_value_label.pack(pady=(5, 2))
        start_value_entry = tk.Entry(dialog)
        start_value_entry.pack(pady=(0, 5))

    def submit_properties():
        color = color_mapping[color_var.get()]  # Türkçe rengi İngilizceye çevir
        if element_type == "Giriş Kutusu":
            start_value = start_value_entry.get()
            if start_value not in ["0", "1"]:
                messagebox.showerror("Hata", "Başlangıç değeri yalnızca '0' veya '1' olabilir.")
                return
            create_io_image(element_type, element_type, color, start_value)
        else:
            create_io_image(element_type, element_type, color)
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Tamam", command=submit_properties)
    submit_button.pack(pady=(10, 10))


def open_connection_properties_dialog(connection_type):
    dialog = tk.Toplevel(root)
    dialog.title(f"{connection_type} Özellikleri")
    dialog.geometry("250x150")

    label = tk.Label(dialog, text=f"{connection_type} için renk bilgisini seçiniz:")
    label.pack(pady=(5, 3))

    color_label = tk.Label(dialog, text="Renk:")
    color_label.pack(pady=(5, 2))

    colors = ["Kırmızı", "Yeşil", "Mavi", "Sarı", "Pembe", "Turuncu", "Mor", "Siyah", "Beyaz", "Gri", "Kahverengi", "Lacivert"]
    color_var = tk.StringVar(dialog)
    color_var.set(colors[0])
    color_menu = tk.OptionMenu(dialog, color_var, *colors)
    color_menu.pack(pady=(0, 5))

    def submit_properties():
        color = color_mapping[color_var.get()]  # Türkçe rengi İngilizceye çevir
        if connection_type == "Çizgi Çizme":
            create_connection_line(color, connection_elements)
        elif connection_type == "Bağlantı Düğümü":
            create_connection_node(color)
        dialog.destroy()
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Tamam", command=submit_properties)
    submit_button.pack(pady=(1, 10))


def run_simulation():
    global led_checkbox_var
    for instance in gate_instances:
        if len(instance) == 5:  # Gate'ler
            if "NAND Gate" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                and_result = all(input_values)
                nand_result = not and_result

                # Çıkış kutusunu veya LED'i oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if nand_result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if nand_result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)
            
            elif "AND Gate" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                # AND gate işlemi
                result = all(input_values)

                # Çıkış kutusunu oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)

            elif "XNOR Gate" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                # XNOR kapısı işlemi
                xor_result = input_values[0] ^ input_values[1]
                result = not xor_result

                # Çıkış kutusunu oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)

            elif "NOR Gate" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                # NOR gate işlemi
                notgate = any(input_values)
                result = not notgate

                # Çıkış kutusunu oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)

            elif "XOR Gate" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                # XOR kapısı işlemi
                result = input_values[0] ^ input_values[1]

                # Çıkış kutusunu oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)
                
            elif "OR Gate" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                # OR gate işlemi
                result = any(input_values)

                # Çıkış kutusunu oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)
        
            elif "NOT Gate" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                # NOT gate işlemi
                result = not input_values[0]

                # Çıkış kutusunu oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)
                
            elif "Buffer" in canvas.itemcget(instance[1], 'text'):
                input_boxes = instance[4]
                input_values = [canvas.itemcget(text, "text") for _, text in input_boxes]
                input_values = list(map(int, input_values))  # String değerleri int'e çevir

                # BUFFER gate işlemi
                result = input_values[0]

                # Çıkış kutusunu oluştur
                gate_x, gate_y = canvas.coords(instance[0])[:2]
                is_led = led_checkbox_var.get() == 1  # LED seçiliyse True olacak
                output_square, output_text = create_output_box(gate_x + 120, gate_y + 22, is_led=is_led)

                if is_led:
                    canvas.itemconfig(output_text, text="")
                    if result == 0:
                        canvas.itemconfig(output_square, fill="#fa8072")
                    else:
                        canvas.itemconfig(output_square, fill="red")
                else:
                    output_value = "1" if result else "0"
                    canvas.itemconfig(output_text, text=output_value)
                    canvas.itemconfig(output_square, fill="red")

                # Bağlantı çizgisi oluştur
                output_line = instance[3]
                canvas.coords(output_line, gate_x + 100, gate_y + 30, gate_x + 120, gate_y + 30)


#Uygulama ekranında yer alan tüm araçları silen fonksiyon
def reset():
    canvas.delete("all")
    gate_instances.clear()
    connection_elements.clear()


# Tüm kapıların çıkış kutularını silen fonksiyon
def stop():
    for instance in gate_instances:
        if len(instance) == 5:  # Kapılar
            gate_x, gate_y = canvas.coords(instance[0])[:2]
            overlapping_items = canvas.find_overlapping(gate_x + 200, gate_y, gate_x + 130, gate_y + 30)
            for item in overlapping_items:
                if item != instance[0]:  
                    canvas.delete(item)


# Sol çerçevede Araçlar başlığı
tools_label = tk.Label(left_frame, text="Araçlar", bg="lightgray", font=("Arial", 16))
tools_label.pack(pady=(10, 0))

# Mantık Kapıları
logic_gates_label = tk.Label(left_frame, text="Mantık Kapıları", bg="lightgray", font=("Arial", 12))
logic_gates_label.pack(pady=(15, 2))

# Mantık Kapıları için butonlar
not_gate_button = tk.Button(left_frame, text="NOT Gate", width=20, command=lambda: open_gate_properties_dialog("NOT Gate"))
not_gate_button.pack(pady=2)

buffer_button = tk.Button(left_frame, text="Buffer", width=20, command=lambda: open_gate_properties_dialog("Buffer"))
buffer_button.pack(pady=2)

and_gate_button = tk.Button(left_frame, text="AND Gate", width=20, command=lambda: open_gate_properties_dialog("AND Gate"))
and_gate_button.pack(pady=2)

or_gate_button = tk.Button(left_frame, text="OR Gate", width=20, command=lambda: open_gate_properties_dialog("OR Gate"))
or_gate_button.pack(pady=2)

nand_gate_button = tk.Button(left_frame, text="NAND Gate", width=20, command=lambda: open_gate_properties_dialog("NAND Gate"))
nand_gate_button.pack(pady=2)

nor_gate_button = tk.Button(left_frame, text="NOR Gate", width=20, command=lambda: open_gate_properties_dialog("NOR Gate"))
nor_gate_button.pack(pady=2)

xor_gate_button = tk.Button(left_frame, text="XOR Gate", width=20, command=lambda: open_gate_properties_dialog("XOR Gate"))
xor_gate_button.pack(pady=2)

xnor_gate_button = tk.Button(left_frame, text="XNOR Gate", width=20, command=lambda: open_gate_properties_dialog("XNOR Gate"))
xnor_gate_button.pack(pady=2)

# Giriş-Çıkış Elemanları
io_elements_label = tk.Label(left_frame, text="Giriş-Çıkış Elemanları", bg="lightgray", font=("Arial", 12))
io_elements_label.pack(pady=(15,2))

# Giriş-Çıkış Elemanları için butonlar
input_box_button = tk.Button(left_frame, text="Giriş Kutusu", width=20, command=lambda: open_io_properties_dialog("Giriş Kutusu"))
input_box_button.pack(pady=2)

output_box_button = tk.Button(left_frame, text="Çıkış Kutusu", width=20, command=lambda: open_io_properties_dialog("Çıkış Kutusu"))
output_box_button.pack(pady=2)

led_button = tk.Button(left_frame, text="LED", width=20, command=lambda: open_io_properties_dialog("LED"))
led_button.pack(pady=2)

# Bağlantı Elemanları
connection_elements_label = tk.Label(left_frame, text="Bağlantı Elemanları", bg="lightgray", font=("Arial", 12))
connection_elements_label.pack(pady=(15,2))

# Bağlantı Elemanları için butonlar
draw_line_button = tk.Button(left_frame, text="Çizgi Çizme", width=20, command=lambda: open_connection_properties_dialog("Çizgi Çizme"))
draw_line_button.pack(pady=2)

connection_node_button = tk.Button(left_frame, text="Bağlantı Düğümü", width=20, command=lambda: open_connection_properties_dialog("Bağlantı Düğümü"))
connection_node_button.pack(pady=2)

# Kontrol Tuşları
control_buttons_label = tk.Label(left_frame, text="Kontrol Tuşları", bg="lightgray", font=("Arial", 12))
control_buttons_label.pack(pady=(15, 2))

# Kontrol Tuşları için butonlar
run_button = tk.Button(left_frame, text="Çalıştır", width=20, command=run_simulation)
run_button.pack(pady=2)

reset_button = tk.Button(left_frame, text="Reset", width=20, command=reset)
reset_button.pack(pady=2)

stop_button = tk.Button(left_frame, text="Durdur", width=20, command=stop)
stop_button.pack(pady=2)

# Mainloop
root.mainloop()