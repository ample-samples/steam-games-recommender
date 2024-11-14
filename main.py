import customtkinter

from library_cache.cache import build_cache

def main():
    (cached_game_ids, new_cache) = build_cache()
    print(cached_game_ids)
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app_geometry = (800, 480)
    (app_x_res, app_y_res) = app_geometry
    app.geometry(f"{app_x_res}x{app_y_res}")

    text_box = customtkinter.CTkTextbox(app, app_x_res, app_y_res)
    text_box.insert("0.0" , ",\n".join(cached_game_ids))
    text_box.configure(state="disabled")
    text_box.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


    app.mainloop()

if __name__ == "__main__":  
    main()
