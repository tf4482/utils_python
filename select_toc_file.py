import os

def select_toc_file(directory):

    def list_toc_files(directory):

        return [f for f in os.listdir(directory) if f.endswith('.toc')]

    def display_menu(files, selected_index):

        os.system('cls' if os.name == 'nt' else 'clear')
        for index, file in enumerate(files):
            if index == selected_index:
                print(f"> {file}")
            else:
                print(f"  {file}")

    toc_files = list_toc_files(directory)

    if not toc_files:
        print(f"Keine .toc-Dateien im Verzeichnis '{directory}' gefunden.")
        return None

    selected_index = 0
    while True:
        display_menu(toc_files, selected_index)
        print("\nMit den Pfeiltasten navigieren (w/s), Auswahl mit Enter.")
        print("Abbrechen mit q.")

        key = input("Eingabe: ").lower()

        if key == 'w':
            selected_index = (selected_index - 1) % len(toc_files)
        elif key == 's':
            selected_index = (selected_index + 1) % len(toc_files)
        elif key == '':
            return os.path.join(directory, toc_files[selected_index])
        elif key == 'q':
            print("Auswahl abgebrochen.")
            return None
