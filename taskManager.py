import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk


class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Management Program")
        self.geometry("600x350")  
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        self.tasks = []

        welcome_label = ctk.CTkLabel(
            self, text="Welcome to Task Management App, Dzikrirazzan!", font=("Helvetica", 22, "bold")
        )
        welcome_label.pack(pady=10)

        self.add_button = ctk.CTkButton(
            self, text="Add Task", command=self.open_add_task_window, width=300
        )
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(
            self, width=50, height=10, font=("Helvetica", 12)
        )
        self.task_listbox.pack(pady=10)

        self.load_button = ctk.CTkButton(
            self, text="Load Tasks", command=self.load_tasks, width=300
        )
        self.load_button.pack(pady=5)

        self.save_button = ctk.CTkButton(
            self, text="Save Tasks", command=self.save_tasks, width=300
        )
        self.save_button.pack(pady=5)

        self.edit_task_index = None
        self.add_window = None
        self.edit_window = None

        self.task_listbox.bind("<Double-Button-1>", self.show_selected_task)

    def open_add_task_window(self):
        if self.add_window is None or not self.add_window.winfo_exists():
            self.add_window = ctk.CTkToplevel(self)
            self.add_window.title("Add Task")
            self.add_window.geometry("400x200")

            task_entry = ctk.CTkEntry(
                self.add_window, width=300
            )
            task_entry.pack(pady=10)
            task_entry.insert(0, "Enter task name")
            task_entry.bind("<FocusIn>", lambda event: self.clear_placeholder_text(
                task_entry, "Enter task name"))
            task_entry.bind("<FocusOut>", lambda event: self.restore_placeholder_text(
                task_entry, "Enter task name"))

            description_entry = ctk.CTkEntry(
                self.add_window, width=300
            )
            description_entry.pack(pady=5)
            description_entry.insert(
                0, "Enter task description") 
            description_entry.bind("<FocusIn>", lambda event: self.clear_placeholder_text(
                description_entry, "Enter task description"))
            description_entry.bind("<FocusOut>", lambda event: self.restore_placeholder_text(
                description_entry, "Enter task description"))

            priority_combobox = ctk.CTkComboBox(
                self.add_window, values=["Low", "Medium", "High"], width=297, state="readonly"
            )
            priority_combobox.pack(pady=5)
            priority_combobox.set("Select priority") 
            priority_combobox.bind("<<ComboboxSelected>>", lambda event: self.clear_placeholder_text(
                priority_combobox, "Select priority"))

            add_button = ctk.CTkButton(
                self.add_window, text="Add Task", command=lambda: self.add_task(task_entry, description_entry, priority_combobox), width=300
            )
            add_button.pack(pady=5)

    def add_task(self, task_entry, description_entry, priority_combobox):
        task = task_entry.get()
        description = description_entry.get()
        priority = priority_combobox.get()
        if task and priority:
            new_task = {"task": task, "description": description, "priority": priority}

            # Menentukan posisi yang tepat berdasarkan prioritas
            if priority == "High":
                self.tasks.insert(0, new_task)  # Prioritas High di atas
            elif priority == "Medium":
                high_index = next((index for index, task in enumerate(self.tasks) if task['priority'] == 'High'), -1)
                self.tasks.insert(high_index + 1, new_task)  # Prioritas Medium di tengah
            elif priority == "Low":
                medium_index = next((index for index, task in enumerate(self.tasks) if task['priority'] == 'Medium'), -1)
                if medium_index == -1:
                    self.tasks.append(new_task)  # Jika tidak ada Medium, Prioritas Low di bawah
                else:
                    self.tasks.insert(medium_index + 1, new_task)  # Prioritas Low di bawah Medium

            self.task_listbox.delete(0, tk.END)
            for task in self.tasks:
                self.task_listbox.insert(tk.END, self.get_task_display(task))
            task_entry.delete(0, ctk.END)
            description_entry.delete(0, ctk.END)
            priority_combobox.set("")
            self.add_window.destroy()
            self.add_window = None
        else:
            messagebox.showwarning("Invalid Input", "Please enter a task and select a priority.")

    def open_edit_task_window(self):
        selected_indices = self.task_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.edit_task_index = index
            task = self.tasks[index]

            if self.edit_window is None or not self.edit_window.winfo_exists():
                self.edit_window = ctk.CTkToplevel(self)
                self.edit_window.title("Edit Task")
                self.edit_window.geometry("400x200")

                task_entry = ctk.CTkEntry(
                    self.edit_window, width=300
                )
                task_entry.pack(pady=10)
                task_entry.insert(0, task["task"])

                description_entry = ctk.CTkEntry(
                    self.edit_window, width=300
                )
                description_entry.pack(pady=5)
                description_entry.insert(0, task["description"])

                priority_combobox = ctk.CTkComboBox(
                    self.edit_window, values=["Low", "Medium", "High"], width=297, state="readonly"
                )
                priority_combobox.pack(pady=5)
                priority_combobox.set(task["priority"])

                update_button = ctk.CTkButton(
                    self.edit_window, text="Update Task", command=lambda: self.update_task(task_entry, description_entry, priority_combobox), width=300
                )
                update_button.pack(pady=5)

                remove_button = ctk.CTkButton(
                    self.edit_window, text="Remove Task", command=self.remove_selected_task, width=300
                )
                remove_button.pack(pady=5)

    def update_task(self, task_entry, description_entry, priority_combobox):
        task = task_entry.get()
        description = description_entry.get()
        priority = priority_combobox.get()
        if task and priority and self.edit_task_index is not None:
            updated_task = {"task": task, "description": description, "priority": priority}
            self.tasks[self.edit_task_index] = updated_task

            self.tasks.sort(key=lambda x: self.priority_to_number(x['priority']), reverse=True)

        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, self.get_task_display(task))

        self.task_listbox.selection_clear(0, tk.END)
        self.task_listbox.selection_set(self.edit_task_index)

        self.edit_window.destroy()
        self.edit_window = None
        self.edit_task_index = None
        priority_combobox.set("")

    def priority_to_number(self, priority):
        if priority == "High":
            return 3
        elif priority == "Medium":
            return 2
        elif priority == "Low":
            return 1
        else:
            return 0

    def remove_selected_task(self):
        selected_indices = self.task_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.task_listbox.delete(index)
            removed_task = self.tasks.pop(index)
            self.edit_window.destroy()

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = []
                lines = file.readlines()
                for line in lines:
                    task, description, priority = line.strip().split(",")
                    self.tasks.append(
                        {"task": task, "description": description, "priority": priority})
            self.task_listbox.delete(0, tk.END)
            for task in self.tasks:
                self.task_listbox.insert(tk.END, self.get_task_display(task))
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "No tasks file found.")

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(
                    f"{task['task']},{task['description']},{task['priority']}\n")
        messagebox.showinfo("Save Successful", "Tasks saved successfully.")

    def get_task_display(self, task):
        return f"{task['task']} - {task['priority']}"

    def show_selected_task(self, event):
        selected_indices = self.task_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            task = self.tasks[index]
            self.open_edit_task_window()

    def clear_placeholder_text(self, entry_widget, placeholder_text):
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, ctk.END)

    def restore_placeholder_text(self, entry_widget, placeholder_text):
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder_text)


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()