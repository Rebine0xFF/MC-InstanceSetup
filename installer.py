import os
import shutil
from datetime import datetime
import sys
from tkinter import Tk, filedialog, messagebox, Toplevel, Label, PhotoImage, Button


BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
# Single hidden Tk root used by dialogs
_root = Tk()
_root.withdraw()

def show_help_image(parent=_root):
    """Show an image to help the user locate the Minecraft folder.

    This creates a transient Toplevel window, displays the image if available,
    and blocks interaction with other windows until closed.
    """
    help_win = Toplevel(parent)
    help_win.title("Où trouver ton dossier minecraft ?")
    help_win.geometry("1920x1080")
    help_win.resizable(False, False)

    img_path = os.path.join(BASE_DIR, "minecraft_folder.png")
    if not os.path.exists(img_path):
        Label(help_win, text="(Image d'aide manquante : minecraft_folder.png)").pack(pady=20)
    else:
        img = PhotoImage(file=img_path)

        # Resize by subsample if image exceeds window size
        max_width, max_height = 1920, 1080
        if img.width() > max_width or img.height() > max_height:
            scale_w = max(1, img.width() // max_width)
            scale_h = max(1, img.height() // max_height)
            scale = max(scale_w, scale_h)
            img = img.subsample(scale, scale)

        lbl = Label(help_win, image=img)
        lbl.image = img
        lbl.pack(pady=10)

    Label(help_win, text="⚙️ Généralement : C:\\Users\\TonNom\\AppData\\Roaming\\.minecraft").pack(pady=10)
    Button(help_win, text="OK, j'ai compris", command=help_win.destroy).pack(pady=10)

    # Modal behaviour: prevent interaction with other windows until closed
    help_win.grab_set()
    parent.wait_window(help_win)

def select_directory():
    """Prompt the user to select the Minecraft folder via a directory picker."""
    # Use the single shared _root for dialogs
    if messagebox.askyesno("Aide", "Souhaites-tu voir une image pour t'aider à trouver ton dossier Minecraft ?"):
        show_help_image(_root)

    messagebox.showinfo("Installation", "Choisis ton dossier Minecraft. Plus vite que ça stp enfaite")
    directory = filedialog.askdirectory(title="Choisis ton dossier Minecraft", parent=_root)
    if not directory:
        messagebox.showwarning("Annulé", "Aucun dossier sélectionné. Installation annulée. Tu peux le faire, on croit en toi.")
        return None
    return directory


def backup_folder(folder_path, backup_name):
    """Create a timestamped backup of folder on the user's Desktop."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(desktop, f"{backup_name}_backup_{timestamp}")
    shutil.copytree(folder_path, backup_path)
    return backup_path

def copy_files(src_folder, dest_folder, extensions=None):
    """Copy files from src_folder to dest_folder; optionally filter by extensions."""
    if not os.path.exists(src_folder):
        print(f"❌ Dossier introuvable : {src_folder}")
        return

    os.makedirs(dest_folder, exist_ok=True)
    count = 0
    for file in os.listdir(src_folder):
        src = os.path.join(src_folder, file)
        dst = os.path.join(dest_folder, file)

        # If extensions are provided, only copy files matching them.
        if extensions:
            if not file.lower().endswith(tuple(extensions)):
                continue
            if not os.path.isfile(src):
                # skip directories or non-regular files when filtering by extension
                print(f"⏭ Skipping non-file entry: {src}")
                continue
            try:
                shutil.copy2(src, dst)
                count += 1
            except PermissionError:
                print(f"⚠️ Permission denied copying file: {src}")
            except Exception as e:
                print(f"⚠️ Error copying file {src}: {e}")
        else:
            # No extension filter: copy files and directories
            try:
                if os.path.isdir(src):
                    # If destination exists, remove it first to ensure fresh copy
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    count += 1
                else:
                    shutil.copy2(src, dst)
                    count += 1
            except PermissionError:
                print(f"⚠️ Permission denied copying entry: {src}")
            except Exception as e:
                print(f"⚠️ Error copying entry {src}: {e}")
    print(f"✅ {count} fichiers copiés depuis {src_folder}")

def handle_mods_installation(target_dir):
    """Install mods into the target directory with optional backup handling."""
    mods_dir = os.path.join(target_dir, "mods")
    mods_source = os.path.join(BASE_DIR, "mods_to_install")

    if os.path.exists(mods_dir) and os.listdir(mods_dir):
        choice = messagebox.askyesnocancel(
            "Mods existants",
            "Des fichiers sont déjà présents dans le dossier 'mods'.\n"
            "Oui = Tout supprimer.\n"
            "Non = Faire un backup sur le Bureau puis supprimer.\n"
            "Annuler = Garder les fichiers existants."
        )
        if choice is None:
            messagebox.showinfo("Annulé", "Installation annulée.")
            return False
        elif choice:
            shutil.rmtree(mods_dir)
            os.makedirs(mods_dir)
        else:
            backup_path = backup_folder(mods_dir, "mods")
            shutil.rmtree(mods_dir)
            os.makedirs(mods_dir)
            messagebox.showinfo("Backup créé", f"Backup sauvegardé sur le Bureau :\n{backup_path}")

    copy_files(mods_source, mods_dir, extensions=[".jar"])
    return True

def optional_install(target_dir, folder_name, display_name, extensions=None):
    """Optionally install additional folders (e.g., resourcepacks, shaderpacks)."""
    if messagebox.askyesno("Option", f"Souhaites-tu installer les {display_name} ?"):
        source = os.path.join(BASE_DIR, f"{folder_name}_to_install")
        dest = os.path.join(target_dir, folder_name)
        copy_files(source, dest, extensions)
        messagebox.showinfo("Terminé", f"{display_name.capitalize()} installés avec succès !")

def install_servers_dat(target_dir):
    """Copy servers.dat into the target directory if the user agrees."""
    servers_src = os.path.join(BASE_DIR, "servers.dat")
    if os.path.exists(servers_src) and messagebox.askyesno("Serveurs", "Souhaites-tu ajouter la liste des serveurs ?"):
        servers_dst = os.path.join(target_dir, "servers.dat")
        shutil.copy2(servers_src, servers_dst)
        messagebox.showinfo("Serveurs ajoutés", "Le fichier servers.dat a été ajouté avec succès.")

def main():
    target_dir = select_directory()
    if not target_dir:
        return

    if handle_mods_installation(target_dir):
        optional_install(target_dir, "resourcepacks", "packs de ressources", extensions=[".zip"])
        optional_install(target_dir, "shaderpacks", "packs de shaders", extensions=None)
        install_servers_dat(target_dir)
        messagebox.showinfo("Installation complète", "✅ Tous les éléments ont été installés avec succès ! 🎉")

if __name__ == "__main__":
    main()