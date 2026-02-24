import tkinter as tk

def calculate_sum():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        result = num1 + num2
        ans_label.config(text="အဖြေ: " + str(result))
    except ValueError:
        ans_label.config(text="ကျေးဇူးပြု၍ နံပါတ်များ ထည့်ပါ")

window = tk.Tk()
window.title("Calculator GUI")
window.geometry("300x200")

tk.Label(window, text="ပထမ ဂဏန်း:").pack(pady=5)
entry1 = tk.Entry(window)
entry1.pack()

tk.Label(window, text="ဒုတိယ ဂဏန်း:").pack(pady=5)
entry2 = tk.Entry(window)
entry2.pack()

btn = tk.Button(window, text="ေပါင်းမည်", command=calculate_sum, bg="yellow")
btn.pack(pady=20)

ans_label = tk.Label(window, text="အေြဖ: 0", font=("Arial", 16))
ans_label.pack()

window.mainloop()