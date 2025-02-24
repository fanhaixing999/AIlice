
STEP = 4096

class AScrollablePage():
    def __init__(self, functions: dict[str, str]):
        self.txt = None
        self.currentIdx = None
        self.functions = functions
        return
    
    def ConstructPrompt(self) -> str:
        ret = "This is a page of the results. To browse more results, you can use the following functions.\n"
        funcs = []
        if ('SCROLLDOWN' in self.functions) and (self.currentIdx + STEP < len(self.txt)):
            funcs.append(f"#scroll down the page: \n{self.functions['SCROLLDOWN']}<!||!>\n")
        if ('SCROLLUP' in self.functions) and (self.currentIdx > 0):
            funcs.append(f"#scroll up the page: \n{self.functions['SCROLLUP']}<!||!>\n")
        if ('SEARCHDOWN' in self.functions) and (self.currentIdx + STEP < len(self.txt)):
            funcs.append(f"#search content downward from the current location by exact match: \n{self.functions['SEARCHDOWN']}<!|query: str|!>\n")
        if ('SEARCHUP' in self.functions) and (self.currentIdx > 0):
            funcs.append(f"#search content upward from the current location by exact match: \n{self.functions['SEARCHUP']}<!|query: str|!>\n")
        return ret + "".join(funcs) if len(funcs) > 0 else ""
    
    def LoadPage(self, txt: str, initPosition: str):
        self.txt = txt
        self.currentIdx = {"TOP": 0, "BOTTOM": len(txt) - STEP}[initPosition]
        return
    
    def ScrollDown(self):
        self.currentIdx += STEP
        return
    
    def ScrollUp(self):
        self.currentIdx -= STEP
        return

    def SearchDown(self, query: str) -> bool:
        loc = self.txt.find(query, self.currentIdx if 0 < self.currentIdx else 0)
        self.currentIdx = (loc - STEP//2) if -1 != loc else self.currentIdx
        return (-1 != loc)
    
    def SearchUp(self, query: str) -> bool:
        loc = self.txt.rfind(query, 0, (self.currentIdx + 1) if 0 < (self.currentIdx + 1) else 0)
        self.currentIdx = (loc - STEP//2) if -1 != loc else self.currentIdx
        return (-1 != loc)
    
    def __call__(self) -> str:
        if (self.currentIdx >= len(self.txt)):
            return "EOF."
        elif ((self.currentIdx + STEP) <= 0):
            return "FILE HEADER REACHED."
        else:
            start = self.currentIdx if self.currentIdx >= 0 else 0
            end = (self.currentIdx + STEP) if (self.currentIdx + STEP) >= 0 else 0
            return self.txt[start:end] + "\n\n" + self.ConstructPrompt()