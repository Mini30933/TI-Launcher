import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import subprocess
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

import gsudo

BG         = "#0e0e11"
CARD       = "#17171c"
TEXT       = "#f2f3f5"
SUBTEXT    = "#7d7f88"
BORDER     = "#25252c"
BORDER_HI  = "#34343d"
ACCENT     = "#4a90e2"
ACCENT_H   = "#5aa0f2"
BTN        = "#1b1b21"
BTN_HOVER  = "#232329"
DANGER     = "#e25a5a"
DANGER_H   = "#f26a6a"
OK         = "#27c93f"
WARN       = "#ffbd2e"
ERR        = "#ff5f5f"
HEADER_BG  = "#16161c"
CLOSE_H    = "#e25a5a"
MIN_H      = "#2e2e35"


class TrustedInstallerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("TrustedInstaller Launcher")
        self.root.geometry("540x660")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.overrideredirect(True)

        self.set_icon()
        self.build_ui()
        self.center_window()

        self._drag_x = 0
        self._drag_y = 0
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def center_window(self):
        self.root.update_idletasks()
        w, h = 540, 660
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def set_icon(self):
        size = 64
        img = tk.PhotoImage(width=size, height=size)
        img.put("#1f1f1f", to=(0, 0, size, size))
        img.put(ACCENT, to=(14, 8, 50, 14))
        img.put(ACCENT, to=(12, 14, 52, 36))
        img.put(ACCENT, to=(16, 36, 48, 44))
        img.put(ACCENT, to=(22, 44, 42, 52))
        img.put(ACCENT, to=(28, 52, 36, 56))
        img.put("#1f1f1f", to=(28, 22, 36, 30))
        img.put("#1f1f1f", to=(30, 30, 34, 40))
        self.root.iconphoto(True, img)
        self._icon = img

    # ================= UI =================
    def build_ui(self):
        # ---------- 标题栏 ----------
        header = tk.Frame(self.root, bg=HEADER_BG, height=86)
        header.pack(fill="x")
        header.pack_propagate(False)

        # 左侧蓝色装饰条
        tk.Frame(header, bg=ACCENT, width=3, height=34).place(x=20, y=26)

        # 标题
        tk.Label(header, text="TrustedInstaller",
                 bg=HEADER_BG, fg=TEXT,
                 font=("Segoe UI Semibold", 16)).place(x=34, y=18)

        # 副标题
        tk.Label(header, text="以 Windows 最高权限运行",
                 bg=HEADER_BG, fg=SUBTEXT,
                 font=("Segoe UI", 9)).place(x=36, y=50)

        # 右上角按钮
        self.btn_close = tk.Label(header, text="✕", bg=HEADER_BG,
                                  fg=SUBTEXT, font=("Segoe UI", 11),
                                  cursor="hand2", padx=12)
        self.btn_close.place(relx=1.0, x=-10, y=26, anchor="ne")
        self.btn_close.bind("<Enter>", lambda e: self.btn_close.config(
            bg=CLOSE_H, fg="white"))
        self.btn_close.bind("<Leave>", lambda e: self.btn_close.config(
            bg=HEADER_BG, fg=SUBTEXT))
        self.btn_close.bind("<Button-1>", lambda e: self.root.destroy())

        self.btn_min = tk.Label(header, text="—", bg=HEADER_BG,
                                fg=SUBTEXT, font=("Segoe UI", 11),
                                cursor="hand2", padx=12)
        self.btn_min.place(relx=1.0, x=-52, y=26, anchor="ne")
        self.btn_min.bind("<Enter>", lambda e: self.btn_min.config(
            bg=MIN_H, fg=TEXT))
        self.btn_min.bind("<Leave>", lambda e: self.btn_min.config(
            bg=HEADER_BG, fg=SUBTEXT))
        self.btn_min.bind("<Button-1>", lambda e: self.minimize())

        # 拖动
        for w in (header,):
            w.bind("<ButtonPress-1>", self.start_drag)
            w.bind("<B1-Motion>", self.do_drag)

        for child in header.winfo_children():
            if child not in (self.btn_close, self.btn_min):
                child.bind("<ButtonPress-1>", self.start_drag)
                child.bind("<B1-Motion>", self.do_drag)

        # 底部细线
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # ---------- 状态卡片 ----------
        status_wrap = tk.Frame(self.root, bg=BG)
        status_wrap.pack(fill="x", padx=26, pady=(20, 14))

        status_card = tk.Frame(status_wrap, bg=CARD,
                               highlightthickness=1,
                               highlightbackground=BORDER_HI)
        status_card.pack(fill="x")

        inner = tk.Frame(status_card, bg=CARD)
        inner.pack(fill="x", padx=18, pady=14)

        level = gsudo.is_admin()
        status_map = {
            0: ("普通用户", ERR),
            1: ("管理员", OK),
            2: ("SYSTEM", WARN),
            3: ("TrustedInstaller", ACCENT),
        }
        text, color = status_map.get(level, ("未知", SUBTEXT))

        dot = tk.Canvas(inner, width=12, height=12, bg=CARD,
                        highlightthickness=0)
        dot.create_oval(1, 1, 11, 11, fill=color, outline="")
        dot.pack(side="left", padx=(0, 10))

        tk.Label(inner, text="当前权限", bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 10)).pack(side="left")
        tk.Label(inner, text=text, bg=CARD, fg=color,
                 font=("Segoe UI Semibold", 11)).pack(side="left", padx=(8, 0))

        tk.Label(inner, text="首次运行弹 UAC", bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 9)).pack(side="right")

        bar_bg = tk.Frame(status_card, bg=BORDER, height=3)
        bar_bg.pack(fill="x", side="bottom")
        progress = {0: 0.15, 1: 0.5, 2: 0.75, 3: 1.0}.get(level, 0.1)
        bar_fill = tk.Frame(bar_bg, bg=color, height=3)
        bar_fill.place(relwidth=progress, relheight=1)

        # ---------- 按钮区 ----------
        pad = tk.Frame(self.root, bg=BG)
        pad.pack(fill="both", expand=True, padx=26, pady=4)

        self.make_button(pad, "T", "打开 TrustedInstaller CMD",
                         self.open_ti_cmd, primary=True)
        self.make_button(pad, "P", "打开 TrustedInstaller PowerShell",
                         self.open_ti_powershell, primary=True)
        self.make_button(pad, "M", "任务管理器 (TI 权限)",
                         self.open_ti_taskmgr)
        self.make_button(pad, "R", "运行... (Win+R 风格)",
                         self.open_run_dialog)
        self.make_button(pad, "E", "以 TrustedInstaller 运行程序...",
                         self.run_ti_program)
        self.make_button(pad, "X", "清理 gsudo 残留",
                         self.clean_gsudo, danger=True)

        # ---------- 底部 ----------
        tk.Frame(self.root, bg=BORDER, height=1).pack(
            fill="x", side="bottom")
        bottom = tk.Frame(self.root, bg=BG, height=34)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)
        tk.Label(bottom, text="TrustedInstaller · Windows 最高权限",
                 bg=BG, fg=SUBTEXT,
                 font=("Segoe UI", 9)).pack(side="left", padx=28)
        tk.Label(bottom, text="v1.0",
                 bg=BG, fg=BORDER_HI,
                 font=("Segoe UI Semibold", 9)).pack(side="right", padx=28)

    def make_button(self, parent, tag, text, command,
                    primary=False, danger=False):
        if danger:
            bg, hover, fg, accent = BTN, "#2a1414", DANGER, DANGER
        elif primary:
            bg, hover, fg, accent = BTN, BTN_HOVER, TEXT, ACCENT
        else:
            bg, hover, fg, accent = BTN, BTN_HOVER, TEXT, BORDER_HI

        # 外层边框统一宽度
        outer = tk.Frame(parent, bg=BORDER_HI)
        outer.pack(fill="x", pady=4)

        row = tk.Frame(outer, bg=bg)
        row.pack(fill="x", padx=1, pady=1)

        bar = tk.Frame(row, bg=bg, width=3)
        bar.pack(side="left", fill="y")

        icon_box = tk.Frame(row, bg=bg, width=34, height=34)
        icon_box.pack(side="left", padx=(12, 0), pady=10)
        icon_box.pack_propagate(False)
        icon_lbl = tk.Label(icon_box, text=tag, bg=bg, fg=accent,
                            font=("Segoe UI Semibold", 12))
        icon_lbl.pack(expand=True)

        lbl = tk.Label(row, text=text, bg=bg, fg=fg,
                       font=("Segoe UI", 11), anchor="w")
        lbl.pack(side="left", fill="x", expand=True, padx=(14, 16), pady=10)

        widgets = (row, bar, icon_box, icon_lbl, lbl)

        def on_enter(e):
            for w in widgets:
                w.config(bg=hover)
            bar.config(bg=accent)

        def on_leave(e):
            for w in widgets:
                w.config(bg=bg)
            bar.config(bg=bg)

        def on_press(e):
            for w in widgets:
                w.config(bg=accent)
            lbl.config(fg="white")
            icon_lbl.config(fg="white")

        def on_release(e):
            on_enter(e)

        def on_click(e):
            command()

        for w in widgets:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<ButtonPress-1>", on_press)
            w.bind("<ButtonRelease-1>", on_release)
            w.bind("<ButtonRelease-1>", on_click, add="+")

    # ================= 拖动 / 最小化 =================
    def start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()

        def restore(event=None):
            if self.root.state() == "normal":
                self.root.overrideredirect(True)
                self.root.unbind("<Map>")

        self.root.bind("<Map>", restore)

    # ================= 功能 =================
    def open_ti_cmd(self):
        def worker():
            try:
                gsudo.admin_subprocess.run(
                    'cmd.exe /c start "TI_CMD" cmd.exe /k '
                    '"title TrustedInstaller CMD && echo. '
                    '&& whoami /groups | findstr TrustedInstaller '
                    '&& echo. && echo [TrustedInstaller 已激活]"',
                    run_as_TrustedInstaller=True
                )
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "启动失败", "无法启动 TrustedInstaller CMD：\n" + str(e)))
        threading.Thread(target=worker, daemon=True).start()

    def open_ti_powershell(self):
        def worker():
            try:
                gsudo.admin_subprocess.run(
                    'cmd.exe /c start "TI_PS" powershell.exe -NoExit -Command '
                    '"Write-Host \'TrustedInstaller PowerShell\' -ForegroundColor Cyan; '
                    'whoami /groups | Select-String TrustedInstaller"',
                    run_as_TrustedInstaller=True
                )
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "启动失败", "无法启动 TrustedInstaller PowerShell：\n" + str(e)))
        threading.Thread(target=worker, daemon=True).start()

    def open_ti_taskmgr(self):
        def worker():
            try:
                gsudo.admin_subprocess.run(
                    'cmd.exe /c start "TI_TaskMgr" taskmgr.exe',
                    run_as_TrustedInstaller=True
                )
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "启动失败", "无法以 TI 启动任务管理器：\n" + str(e)))
        threading.Thread(target=worker, daemon=True).start()

    def open_run_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("运行")
        dlg.geometry("460x180")
        dlg.resizable(False, False)
        dlg.configure(bg=CARD)
        dlg.transient(self.root)
        dlg.grab_set()

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 460) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 180) // 2
        dlg.geometry(f"+{x}+{y}")
        dlg.configure(highlightthickness=1, highlightbackground=BORDER_HI)

        tk.Label(dlg, text="以 TrustedInstaller 权限运行",
                 bg=CARD, fg=TEXT,
                 font=("Segoe UI Semibold", 12)).pack(
            anchor="w", padx=20, pady=(20, 4))
        tk.Label(dlg, text="输入命令，回车执行",
                 bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(0, 12))

        wrap = tk.Frame(dlg, bg=BG, highlightthickness=1,
                        highlightbackground=BORDER_HI)
        wrap.pack(fill="x", padx=20)

        entry = tk.Entry(wrap, font=("Consolas", 12),
                         bg=BG, fg=TEXT, insertbackground=ACCENT,
                         bd=0, relief="flat")
        entry.pack(fill="x", padx=12, pady=10)
        entry.focus_set()

        tk.Label(dlg, text="例：cmd /c notepad   或   taskmgr",
                 bg=CARD, fg=SUBTEXT, font=("Segoe UI", 9)).pack(
            anchor="w", padx=20, pady=(8, 0))

        def do_run(event=None):
            cmd = entry.get().strip()
            if not cmd:
                return
            dlg.destroy()
            self._run_ti_command(cmd)

        entry.bind("<Return>", do_run)

        btns = tk.Frame(dlg, bg=CARD)
        btns.pack(fill="x", padx=20, pady=16)
        tk.Button(btns, text="取消", command=dlg.destroy,
                  bg=BTN, fg=SUBTEXT, bd=0, relief="flat",
                  activebackground=BTN_HOVER, activeforeground=TEXT,
                  font=("Segoe UI", 10), padx=18, pady=6,
                  cursor="hand2").pack(side="right")
        tk.Button(btns, text="运行", command=do_run,
                  bg=ACCENT, fg="white", bd=0, relief="flat",
                  activebackground=ACCENT_H, activeforeground="white",
                  font=("Segoe UI Semibold", 10), padx=18, pady=6,
                  cursor="hand2").pack(side="right", padx=(0, 8))

    def _run_ti_command(self, cmd):
        def worker():
            try:
                gsudo.admin_subprocess.run(
                    f'cmd.exe /c start "TI_Run" cmd.exe /k "{cmd}"',
                    run_as_TrustedInstaller=True
                )
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "运行失败", f"无法以 TI 运行：\n{cmd}\n\n{e}"))
        threading.Thread(target=worker, daemon=True).start()

    def run_ti_program(self):
        path = filedialog.askopenfilename(
            title="选择要以 TrustedInstaller 运行的程序",
            filetypes=[("可执行文件", "*.exe"),
                       ("批处理文件", "*.bat;*.cmd"),
                       ("所有文件", "*.*")]
        )
        if not path:
            return

        def worker():
            try:
                gsudo.admin_subprocess.run(
                    f'cmd.exe /c start "TI_App" "{path}"',
                    run_as_TrustedInstaller=True
                )
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "运行失败", "无法以 TrustedInstaller 运行：\n" + path + "\n\n" + str(e)))
        threading.Thread(target=worker, daemon=True).start()

    def clean_gsudo(self):
        def worker():
            try:
                r1 = subprocess.run(
                    ["sc", "query", "type=", "service", "state=", "all"],
                    capture_output=True, text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                services, cur = [], None
                for line in r1.stdout.splitlines():
                    line = line.strip()
                    if line.startswith("SERVICE_NAME:"):
                        cur = line.split(":", 1)[1].strip()
                    elif cur and "gsudo" in cur.lower():
                        if cur not in services:
                            services.append(cur)
                    if cur and not line:
                        cur = None

                r2 = subprocess.run(
                    ["schtasks", "/query", "/fo", "CSV", "/nh"],
                    capture_output=True, text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                tasks = []
                for line in r2.stdout.splitlines():
                    if "gsudo" in line.lower():
                        name = line.split(",")[0].strip().strip('"')
                        if name and name not in tasks:
                            tasks.append(name)

                deleted_s, deleted_t = [], []
                for s in services:
                    d = subprocess.run(["sc", "delete", s],
                                       capture_output=True, text=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                    if d.returncode == 0:
                        deleted_s.append(s)
                for t in tasks:
                    d = subprocess.run(["schtasks", "/delete", "/tn", t, "/f"],
                                       capture_output=True, text=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                    if d.returncode == 0:
                        deleted_t.append(t)

                msg = (
                    "扫描完成\n\n"
                    f"发现服务：{len(services)} 个\n"
                    f"删除服务：{len(deleted_s)} 个\n\n"
                    f"发现任务：{len(tasks)} 个\n"
                    f"删除任务：{len(deleted_t)} 个"
                )
                if not services and not tasks:
                    msg = "扫描完成，未发现 gsudo 残留。"
                self.root.after(0, lambda: messagebox.showinfo("清理结果", msg))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "清理失败", "清理过程出错：\n" + str(e)))
        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrustedInstallerLauncher(root)
    root.mainloop()