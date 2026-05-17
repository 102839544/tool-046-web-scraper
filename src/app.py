#!/usr/bin/env python3
"""
网页爬虫工具 - 简单网页内容抓取
"""
import sys, os, re, tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext
import urllib.request
import urllib.parse

class App:
    def __init__(self, root):
        self.root = root
        root.title("网页爬虫工具 v1.0")
        root.geometry("850x650")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#d32f2f", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🕷️ 网页爬虫工具", font=("Arial",14,"bold"),
                 fg="white", bg="#d32f2f").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # URL输入
        uf = tk.Frame(main)
        uf.pack(fill="x", pady=5)
        tk.Label(uf, text="网址：").pack(side="left")
        self.url_entry = tk.Entry(uf, font=("Arial",10), width=60)
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.url_entry.insert(0, "https://example.com")
        
        # 抓取按钮
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="抓取网页", command=self.fetch,
                  bg="#d32f2f", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="提取链接", command=self.extract_links,
                  padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="提取文本", command=self.extract_text,
                  padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="保存结果", command=self.save,
                  bg="#4caf50", fg="white", padx=15).pack(side="right", padx=5)
        
        # 结果
        self.result_txt = scrolledtext.ScrolledText(main, font=("Consolas",9), height=25)
        self.result_txt.pack(fill="both", expand=True, pady=5)
        
        self.status = tk.Label(main, text="输入网址后点击「抓取网页」",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def fetch(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入网址")
            return
        
        try:
            self.status.config(text="抓取中...")
            self.root.update()
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            with urllib.request.urlopen(req, timeout=20) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            
            self.result_txt.delete(1.0, "end")
            self.result_txt.insert(1.0, html)
            self.status.config(text=f"✅ 抓取成功（{len(html)} 字符）")
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status.config(text="❌ 抓取失败")
    
    def extract_links(self):
        html = self.result_txt.get(1.0, "end")
        if not html.strip():
            messagebox.showwarning("提示", "请先抓取网页")
            return
        
        pattern = r'href=["\']([^"\']+)["\']'
        links = re.findall(pattern, html, re.IGNORECASE)
        
        result = f"找到 {len(links)} 个链接：\n\n"
        for link in links[:100]:
            result += link + "\n"
        
        self.result_txt.delete(1.0, "end")
        self.result_txt.insert(1.0, result)
        self.status.config(text=f"✅ 提取了 {len(links)} 个链接")
    
    def extract_text(self):
        html = self.result_txt.get(1.0, "end")
        if not html.strip():
            messagebox.showwarning("提示", "请先抓取网页")
            return
        
        # 移除script和style标签
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        # 移除所有HTML标签
        text = re.sub(r"<[^>]+>", "", text)
        # 清理空白
        text = re.sub(r"\s+", " ", text).strip()
        
        self.result_txt.delete(1.0, "end")
        self.result_txt.insert(1.0, text)
        self.status.config(text="✅ 文本提取完成")
    
    def save(self):
        text = self.result_txt.get(1.0, "end")
        if not text.strip():
            messagebox.showwarning("提示", "没有内容可保存")
            return
        
        f = filedialog.asksaveasfilename(title="保存",
             defaultextension=".txt", filetypes=[("文本","*.txt"),("HTML","*.html")])
        if f:
            with open(f, "w", encoding="utf-8") as file:
                file.write(text)
            messagebox.showinfo("保存成功", f"已保存至：{f}")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
