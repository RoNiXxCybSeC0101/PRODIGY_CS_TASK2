import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Initialize global variables
image_path = ""
image_encrypted = None
panelA = None
panelB = None
encryption_key = None  # This will store the encryption key

# Function to open the file dialog to select an image
def open_img():
    global image_path, panelA, panelB, encryption_key
    image_path = filedialog.askopenfilename(title="Select an Image")
    
    if image_path:
        img = Image.open(image_path)
        img_resized = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img_resized)
        
        # Hide buttons initially
        hide_buttons()
        
        if panelA is None or panelB is None:
            panelA = tk.Label(window, image=img_tk)
            panelA.image = img_tk
            panelA.place(x=50, y=150)
            panelB = tk.Label(window, image=img_tk)
            panelB.image = img_tk
            panelB.place(x=550, y=150)
        else:
            panelA.configure(image=img_tk)
            panelB.configure(image=img_tk)
            panelA.image = img_tk
            panelB.image = img_tk
        
        # Show buttons after image is loaded
        show_buttons()
        
        messagebox.showinfo("Image Loaded", "Image loaded successfully!")

# Function to hide buttons
def hide_buttons():
    save_button.place_forget()
    encrypt_button.place_forget()
    decrypt_button.place_forget()
    reset_button.place_forget()
    exit_button.place_forget()

# Function to show buttons horizontally with smaller size
def show_buttons():
    button_y = 580  # Set a constant y-coordinate for horizontal alignment
    button_x_start = 50  # Starting x-coordinate for the first button
    button_spacing = 250  # Horizontal spacing between buttons
    
    # Place smaller buttons horizontally below the image
    save_button.place(x=button_x_start, y=button_y, width=150, height=40)
    encrypt_button.place(x=button_x_start + button_spacing, y=button_y, width=150, height=40)
    decrypt_button.place(x=button_x_start + 2 * button_spacing, y=button_y, width=150, height=40)
    reset_button.place(x=button_x_start + 3 * button_spacing, y=button_y, width=150, height=40)
    exit_button.place(x=850, y=20, width=100, height=40)  # Keep the exit button where it was


# Function to encrypt the image using XOR encryption
def en_fun():
    global image_path, image_encrypted, panelB, encryption_key
    if image_path:
        # Open image in color (BGR format)
        img = cv2.imread(image_path)  # This reads in color by default (BGR)
        img = img.astype(np.uint8)
        
        # Generate a random encryption key (same size as image)
        encryption_key = np.random.randint(0, 256, img.shape, dtype=np.uint8)
        
        # Perform XOR encryption on all color channels
        encrypted_img = cv2.bitwise_xor(img, encryption_key)
        
        # Save encrypted image
        cv2.imwrite('image_encrypted.jpg', encrypted_img)
        image_encrypted = encrypted_img  # Store encrypted image in global variable
        
        img_encrypted = Image.open('image_encrypted.jpg')
        img_encrypted_resized = img_encrypted.resize((400, 400))
        img_encrypted_tk = ImageTk.PhotoImage(img_encrypted_resized)

        panelB.configure(image=img_encrypted_tk)
        panelB.image = img_encrypted_tk

        messagebox.showinfo("Encryption Status", "Image Encrypted successfully!")

# Function to decrypt the image using XOR decryption
def de_fun():
    global image_encrypted, panelB, encryption_key
    if image_encrypted is not None and encryption_key is not None:
        # Perform XOR decryption (same operation as encryption with the same key)
        decrypted_img = cv2.bitwise_xor(image_encrypted, encryption_key)
        
        # Save decrypted image
        cv2.imwrite('image_decrypted.jpg', decrypted_img)
        
        img_decrypted = Image.open('image_decrypted.jpg')
        img_decrypted_resized = img_decrypted.resize((400, 400))
        img_decrypted_tk = ImageTk.PhotoImage(img_decrypted_resized)

        panelB.configure(image=img_decrypted_tk)
        panelB.image = img_decrypted_tk

        messagebox.showinfo("Decryption Status", "Image Decrypted successfully!")
    else:
        messagebox.showerror("Error", "No image or key to decrypt!")

# Function to reset the image to the original one
def reset():
    global image_path, panelB
    if image_path:
        img = Image.open(image_path)
        img_resized = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img_resized)
        
        panelB.configure(image=img_tk)
        panelB.image = img_tk
        messagebox.showinfo("Reset", "Image reset to original format!")
    else:
        messagebox.showerror("Error", "No image to reset!")

# Function to save the encrypted/decrypted image
def save_img():
    global image_encrypted
    if image_encrypted is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if save_path:
            cv2.imwrite(save_path, image_encrypted)
            messagebox.showinfo("Success", "Image saved successfully!")
    else:
        messagebox.showerror("Error", "No image to save!")

# Function to exit the program
def exit_win():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Button hover effect function
def on_enter(event):
    event.widget.config(bg="#f1c40f")  # Light yellow for hover effect

def on_leave(event):
    event.widget.config(bg=event.widget.cget("bg"))  # Reset to original background color


# UI Elements
window = tk.Tk()
window.geometry("1000x750")
window.title("Image Encryption Decryption")
window.config(bg="#f0f0f0")

header_label = tk.Label(window, text="Image Encryption\nDecryption", font=("Arial", 30, "bold"), fg="#ff6347", bg="#f0f0f0")
header_label.place(x=270, y=30)

choose_button = tk.Button(window, text="Choose Image", command=open_img, font=("Arial", 16), bg="#4caf50", fg="white", relief="raised")
choose_button.place(x=50, y=100, width=200, height=50)

# Buttons initially hidden
save_button = tk.Button(window, text="Save Image", command=save_img, font=("Arial", 16), bg="#673ab7", fg="white", relief="raised")
encrypt_button = tk.Button(window, text="Encrypt", command=en_fun, font=("Arial", 16), bg="#2196f3", fg="white", relief="raised")
decrypt_button = tk.Button(window, text="Decrypt", command=de_fun, font=("Arial", 16), bg="#f44336", fg="white", relief="raised")
reset_button = tk.Button(window, text="Reset", command=reset, font=("Arial", 16), bg="#ffeb3b", fg="black", relief="raised")
exit_button = tk.Button(window, text="Exit", command=exit_win, font=("Arial", 16), bg="#f44336", fg="white", relief="raised")

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()

