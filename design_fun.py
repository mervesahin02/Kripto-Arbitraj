from PIL import Image, ImageDraw, ImageTk

def create_gradient_label(canvas, x, y, text, font=("Arial", 14, "bold"), width=200, height=40, color1="#a9a9a9"
                          ,color2="#4f4f4f"):
    """Canvas üzerinde gradient bir etiket oluşturur."""
    image = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Gradient renk çizimi
    for i in range(height):
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 + (r2 - r1) * (i / height))
        g = int(g1 + (g2 - g1) * (i / height))
        b = int(b1 + (b2 - b1) * (i / height))
        color = (r, g, b, 255)
        draw.line((0, i, width, i), fill=color)

    # Canvas üzerinde görüntüyü ekle
    gradient_image = ImageTk.PhotoImage(image)
    canvas.create_image(x, y, image=gradient_image, anchor="nw")
    canvas.image_refs.append(gradient_image)

    # Metin ekle
    canvas.create_text(x + width // 2, y + height // 2, text=text, font=font, fill="white")

def create_rounded_button(canvas, x, y, text, command, width=150, height=50, color="#4caf50"):
    """Canvas üzerinde yuvarlatılmış bir buton oluşturur."""

    def on_click(event):
        # Basılma animasyonu: Rengi değiştir
        draw.rounded_rectangle((0, 0, width, height), radius, fill="#c0c0c0")  # Daha koyu bir renk
        button_image_pressed = ImageTk.PhotoImage(button_bg)
        canvas.itemconfig(button, image=button_image_pressed)
        canvas.image_refs.append(button_image_pressed)

        # Komutu çalıştır ve animasyonu geri al
        command()
        canvas.after(200, lambda: canvas.itemconfig(button, image=button_image))  # 200 ms sonra eski hali

    def on_enter(event):
        canvas.config(cursor="hand2")  # Fare imlecini değiştir

    def on_leave(event):
        canvas.config(cursor="")  # Fare imlecini varsayılana döndür

    # Yuvarlak köşeli arka plan oluştur
    radius = 20
    button_bg = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(button_bg)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    button_image = ImageTk.PhotoImage(button_bg)

    # Canvas üzerinde butonu çiz
    button = canvas.create_image(x, y, image=button_image, anchor="nw")
    canvas.image_refs.append(button_image)

    # Buton üzerine metin ekle
    text_id = canvas.create_text(x + width // 2, y + height // 2, text=text, font=("Arial", 12, "bold"),
                                 fill="white")

    # Tıklama ve fare olaylarını bağla
    canvas.tag_bind(button, "<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)
    canvas.tag_bind(button, "<Enter>", on_enter)
    canvas.tag_bind(button, "<Leave>", on_leave)
    canvas.tag_bind(text_id, "<Enter>", on_enter)
    canvas.tag_bind(text_id, "<Leave>", on_leave)