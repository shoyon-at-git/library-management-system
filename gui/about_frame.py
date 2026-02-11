import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class AboutFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        title = tk.Label(self, text="About HSTU Library", bg="white",
                 fg="#0b3c5d", font=("Segoe UI", 20, "bold"), justify="center")
        title.pack(pady=(0, 12))

        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=15)

        # Images container
        imgs_frame = tk.Frame(top, bg="white")
        imgs_frame.pack(fill="x")

        # Try multiple filename variants (library1, library-1, library_1) and extensions
        bases = ["library1", "library-1", "library_1", "library 1"]
        img_names = [bases, [b.replace("1","2") for b in bases], [b.replace("1","3") for b in bases]]
        exts = [".jpg", ".jpeg", ".png"]
        self.photos = []

        def find_image_for_variants(variants):
            images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
            for v in variants:
                for e in exts:
                    p = os.path.join(images_dir, v + e)
                    if os.path.exists(p):
                        return p
            return None

        for variants in img_names:
            path = find_image_for_variants(variants)
            display_name = variants[0] + "*"
            if path:
                try:
                    img = Image.open(path)
                    img.thumbnail((240, 160))
                    ph = ImageTk.PhotoImage(img)
                    lbl = tk.Label(imgs_frame, image=ph, bg="white")
                    lbl.image = ph
                    lbl.pack(side="left", padx=8, pady=8)
                    self.photos.append(ph)
                except Exception:
                    lbl = tk.Label(imgs_frame, text=os.path.basename(path), bg="#ecf0f1", width=34, height=10)
                    lbl.pack(side="left", padx=8, pady=8)
            else:
                lbl = tk.Label(imgs_frame, text=display_name + "\n(not found)", bg="#ecf0f1", width=34, height=10)
                lbl.pack(side="left", padx=8, pady=8)

        # Text area with scrollbar
        text_frame = tk.Frame(self, bg="white")
        text_frame.pack(fill="both", expand=True, padx=15, pady=(10,15))

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set,
                   bg="white", bd=0, font=("Segoe UI", 10), fg="#333")
        long_text = (
            "Hajee Mohammad Danesh Science and Technology University is only a Science and Technology University for north region of the country. "
            "The library is called the heart of an institution. University creates knowledge through the research and the library of the university preserves the all kind of research results (knowledge). "
            "So the library has been playing an enormous role for conducting research, lesson preparing and learning.\n\n"
            "Activities and Facilities:\n\n"
            "HSTU Library is a well furnished multi storied building. It is doing its daily activities by different sections, such as: Acquisition section, Circulation section, Processing section and Reference section which are situated at different location in the Library Building. Administrative section of the library does the administrative activities. Acquisition Section is always working hard to collect the all kind of required documents of the users. Recently it has collected a great deal of different types of books for different faculties of this university. Circulation section sets on the ground floor of the library building. All the researchers, students and teachers of this university may borrow their required books as per rule from the Circulation Section for reading the book outside of the library or home. Only those books that are more than 2 copies are available for loan to students/ teachers/ researchers. Processing section is doing an important job. It prepares the catalogue and classification all kind of documents by using the AACR-2 code and D.D.C. scheme. It is located on the ground floor of the library building. Reference section is another important section. It is situated at the first floor and second floor of the building. Teachers, researchers and students may read the rare documents sitting in the Reference Section. It also provides photocopy facility against a nominal fee. Another important service of this section is current awareness service. It regularly sends the list of current received documents to the faculties. Thesis, 73 titled home and abroad journals and 15 Daily newspapers are kept at the 2nd floor of the building. All kind of users can read the journal, daily newspaper and thesis here. There is a cyber center in the Library. All users may use the cyber center against a nominal fee.\n\n"
            "Mission:\n\n"
            "The Library's mission is to provide comprehensive resources and services in support of the research, teaching and learning needs of the University community.\n\n"
            "Vision:\n\n"
            "Build up a world-class Knowledge Resource Centre and provide innovative services and collections to the research, teaching and learning communities by using latest technology.\n\n"
            "LIBRARY RESOURCES:\n\n"
            "1. Printed Books: 23,105\n"
            "2. THESIS: 800\n"
            "3. Audio-Visual Materials: 300 nos\n"
            "4. PERIODICAL:\n"
            "a) Printed Journals: 89 (National and International)\n"
            "b) E-Journals: HSTU Library is getting access over 4o thousand titled e-journals of 35 publishers through BIP Consortium, University Grants Commission Digital Library (UDL), HINARI, OARESCIENCES and AGORA.\n"
            "c) E-books: HSTU Library is getting access over 7053 titled e-books of different subjects through University Grants Commission Digital Library (UDL).\n\n"
            "Library Hour:\n\n"
            "The Library shall be opened from 8:00 am to 7:00 pm. It shall be wholly closed on university holidays.\n\n"
            "Library User Policy:\n\n"
            "1. A teacher may borrow up to 5 books for 30 days and a student/ a researcher may also borrow up to 3 books for 20 days at any given time.\n"
            "2. All personal bags, coats, jackets, umbrellas, etc. are to be kept in the pigeonhole near the security desk.\n"
            "3. Group study, gossiping, discussions, eating, drinking, and smoking are strictly prohibited inside the Library.\n"
            "4. All students are requested to handle with care all the fittings, fixtures, furniture, equipment, books, journals, CD's computers, etc. of the Library and should leave them neat and tidy after use.\n"
            "5. Mobile phone cannot be used inside the Library.\n"
            "6. No book shall be issued to students for use in reading room or home within the last half hour previous to daily closing.\n"
        )
        # Insert line-by-line and tag headings (lines that end with ':' ) as bold
        import tkinter.font as tkfont
        bold_font = tkfont.Font(font=text.cget("font"))
        bold_font.configure(weight="bold")
        text.tag_configure("heading", font=bold_font)

        for line in long_text.splitlines(True):
            start = text.index(tk.INSERT)
            text.insert(tk.INSERT, line)
            end = text.index(tk.INSERT)
            if line.strip().endswith(":"):
                text.tag_add("heading", start, end)

        text.config(state="disabled")
        text.pack(fill="both", expand=True, side="left")
        scrollbar.config(command=text.yview)