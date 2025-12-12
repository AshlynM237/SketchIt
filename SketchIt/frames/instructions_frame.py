import customtkinter as ctk
import os
import re
from tkinter import font as tkfont
from tkinter.scrolledtext import ScrolledText


class InstructionsFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.switch_callback = switch_callback

        ctk.CTkLabel(self, text="📘 How to Play SketchIt", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        # Load instructions from markdown file
        instructions_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instructions.md")
        instructions_content = self.load_instructions(instructions_path)

        # Create a styled text widget for markdown rendering
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Get current appearance mode for theme-aware colors
        appearance_mode = ctk.get_appearance_mode()
        is_dark = appearance_mode == "Dark" or appearance_mode == "dark"
        
        # Set colors based on theme
        bg_color = "#212121" if is_dark else "#FFFFFF"
        fg_color = "#FFFFFF" if is_dark else "#000000"
        code_bg = "#2A2A2A" if is_dark else "#F0F0F0"
        code_fg = "#FFD700" if is_dark else "#D2691E"
        
        # Use tkinter Text widget with customtkinter styling for better markdown support
        self.textbox = ScrolledText(text_frame, width=70, height=25, wrap="word", 
                                    bg=bg_color, fg=fg_color, 
                                    insertbackground=fg_color,
                                    font=tkfont.Font(family="Helvetica", size=11),
                                    relief="flat", borderwidth=0)
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure text tags for markdown formatting
        self.configure_text_tags()
        
        # Render markdown content
        self.render_markdown(instructions_content)
        self.textbox.configure(state="disabled")

        ctk.CTkButton(self, text="Back to Menu", command=lambda: self.switch_callback("matchmaking")).pack(pady=10)

    def load_instructions(self, file_path):
        """Load instructions from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "# Instructions\n\nInstructions file not found. Please create `instructions.md`."
        except Exception as e:
            return f"# Error\n\nCould not load instructions: {str(e)}"

    def configure_text_tags(self):
        """Configure text tags for markdown formatting."""
        # Get current appearance mode for theme-aware colors
        appearance_mode = ctk.get_appearance_mode()
        is_dark = appearance_mode == "Dark" or appearance_mode == "dark"
        
        # Header colors - use theme accent colors
        h1_color = "#4A9EFF" if is_dark else "#1A5F9F"
        h2_color = "#5FB3FF" if is_dark else "#2A7FBF"
        h3_color = "#7FC7FF" if is_dark else "#3A9FDF"
        bullet_color = "#4A9EFF" if is_dark else "#1A5F9F"
        code_bg = "#2A2A2A" if is_dark else "#F0F0F0"
        code_fg = "#FFD700" if is_dark else "#D2691E"
        
        # Header styles
        self.textbox.tag_configure("h1", font=tkfont.Font(family="Helvetica", size=20, weight="bold"),
                                   foreground=h1_color, spacing1=10, spacing3=5)
        self.textbox.tag_configure("h2", font=tkfont.Font(family="Helvetica", size=16, weight="bold"),
                                   foreground=h2_color, spacing1=8, spacing3=4)
        self.textbox.tag_configure("h3", font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                                   foreground=h3_color, spacing1=6, spacing3=3)
        
        # Text styles
        self.textbox.tag_configure("bold", font=tkfont.Font(family="Helvetica", size=11, weight="bold"))
        self.textbox.tag_configure("italic", font=tkfont.Font(family="Helvetica", size=11, slant="italic"))
        self.textbox.tag_configure("code", font=tkfont.Font(family="Courier", size=10),
                                   background=code_bg, foreground=code_fg)
        
        # List styles
        self.textbox.tag_configure("list_item", spacing1=2, spacing3=2)
        self.textbox.tag_configure("bullet", foreground=bullet_color)

    def render_markdown(self, markdown_text):
        """Render markdown text with formatting."""
        lines = markdown_text.split('\n')
        
        for line in lines:
            # Handle headers
            if line.startswith('###'):
                text = line[3:].strip()
                if text:
                    self.insert_formatted_text(text + "\n", "h3")
                else:
                    self.textbox.insert("end", "\n")
            elif line.startswith('##'):
                text = line[2:].strip()
                if text:
                    self.insert_formatted_text(text + "\n", "h2")
                else:
                    self.textbox.insert("end", "\n")
            elif line.startswith('#'):
                text = line[1:].strip()
                if text:
                    self.insert_formatted_text(text + "\n", "h1")
                else:
                    self.textbox.insert("end", "\n")
            # Handle numbered lists
            elif re.match(r'^\d+\.\s', line):
                text = line[line.find('.') + 1:].strip()
                self.textbox.insert("end", "  ", "list_item")
                self.insert_formatted_text(text, "list_item")
                self.textbox.insert("end", "\n", "list_item")
            # Handle bullet lists
            elif line.strip().startswith('-') or line.strip().startswith('*'):
                text = line.strip()[1:].strip()
                self.textbox.insert("end", "  • ", ("list_item", "bullet"))
                self.insert_formatted_text(text, "list_item")
                self.textbox.insert("end", "\n", "list_item")
            # Handle empty lines
            elif not line.strip():
                self.textbox.insert("end", "\n")
            # Handle regular text
            else:
                self.insert_formatted_text(line)
                self.textbox.insert("end", "\n")
    
    def insert_formatted_text(self, text, base_tag=None):
        """Insert text with inline markdown formatting applied."""
        if base_tag is None:
            base_tag = []
        elif isinstance(base_tag, str):
            base_tag = [base_tag]
        
        # Process inline formatting: bold, italic, code
        # We'll process in order: code, bold, italic (to avoid conflicts)
        parts = []
        remaining = text
        
        # Find all formatting markers
        markers = []
        
        # Find code blocks first (highest priority)
        for match in re.finditer(r'`([^`]+)`', remaining):
            markers.append(('code', match.start(), match.end(), match.group(1)))
        
        # Find bold text (**text** or __text__)
        for match in re.finditer(r'\*\*([^*]+)\*\*|__([^_]+)__', remaining):
            # Skip if inside a code block
            if not any(m[0] == 'code' and m[1] <= match.start() < m[2] for m in markers):
                markers.append(('bold', match.start(), match.end(), match.group(1) or match.group(2)))
        
        # Find italic text (*text* or _text_) - but not if it's part of bold
        for match in re.finditer(r'(?<!\*)\*([^*]+)\*(?!\*)|(?<!_)_([^_]+)_(?!_)', remaining):
            # Skip if inside a code block or bold
            if not any(m[0] in ['code', 'bold'] and m[1] <= match.start() < m[2] for m in markers):
                markers.append(('italic', match.start(), match.end(), match.group(1) or match.group(2)))
        
        # Sort markers by position
        markers.sort(key=lambda x: x[1])
        
        # Build text parts
        last_pos = 0
        for marker_type, start, end, content in markers:
            # Add text before marker
            if start > last_pos:
                plain_text = remaining[last_pos:start]
                if plain_text:
                    parts.append(('plain', plain_text, base_tag))
            
            # Add formatted text
            if marker_type == 'code':
                parts.append(('code', content, base_tag + ['code']))
            elif marker_type == 'bold':
                parts.append(('bold', content, base_tag + ['bold']))
            elif marker_type == 'italic':
                parts.append(('italic', content, base_tag + ['italic']))
            
            last_pos = end
        
        # Add remaining text
        if last_pos < len(remaining):
            plain_text = remaining[last_pos:]
            if plain_text:
                parts.append(('plain', plain_text, base_tag))
        
        # If no formatting found, just insert plain text
        if not parts:
            if base_tag:
                self.textbox.insert("end", text, tuple(base_tag) if len(base_tag) > 1 else base_tag[0])
            else:
                self.textbox.insert("end", text)
        else:
            # Insert all parts
            for part_type, content, tags in parts:
                if tags:
                    tag = tuple(tags) if len(tags) > 1 else tags[0]
                    self.textbox.insert("end", content, tag)
                else:
                    self.textbox.insert("end", content)
