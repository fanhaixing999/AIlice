import os
import json
import appdirs
from termcolor import colored

class AConfig():
    def __init__(self):
        self.maxMemory = {}
        self.quantization = None
        self.models = {
            "hf": {
                "modelWrapper": "AModelLLAMA",
                "modelList": {
                    "meta-llama/Llama-2-13b-chat-hf": {"formatter": "AFormatterLLAMA2", "contextWindow": 4096, "systemAsUser": False},
                    "meta-llama/Llama-2-70b-chat-hf": {"formatter": "AFormatterLLAMA2", "contextWindow": 4096, "systemAsUser": False},
                    "upstage/llama-30b-instruct-2048": {"formatter": "AFormatterSimple", "contextWindow": 2048, "systemAsUser": False},
                    "lmsys/vicuna-33b-v1.3": {"formatter": "AFormatterVicuna", "contextWindow": 2048, "systemAsUser": False},
                    "Phind/Phind-CodeLlama-34B-v2": {"formatter": "AFormatterSimple", "contextWindow": 4096, "systemAsUser": False},
                    "Xwin-LM/Xwin-LM-70B-V0.1": {"formatter": "AFormatterVicuna", "contextWindow": 4096, "systemAsUser": False},
                    "Xwin-LM/Xwin-LM-13B-V0.1": {"formatter": "AFormatterVicuna", "contextWindow": 4096, "systemAsUser": False},
                    "mistralai/Mistral-7B-Instruct-v0.1": {"formatter": "AFormatterLLAMA2", "contextWindow": 8192, "systemAsUser": False},
                    "Open-Orca/Mistral-7B-OpenOrca": {"formatter": "AFormatterChatML", "contextWindow": 8192, "systemAsUser": False},
                    "teknium/OpenHermes-2.5-Mistral-7B": {"formatter": "AFormatterChatML", "contextWindow": 8192, "systemAsUser": False},
                    "Intel/neural-chat-7b-v3-1": {"formatter": "AFormatterSimple", "contextWindow": 8192, "systemAsUser": False},
                    "amazon/MistralLite": {"formatter": "AFormatterAMAZON", "contextWindow": 16384, "systemAsUser": False},
                    "HuggingFaceH4/zephyr-7b-beta": {"formatter": "AFormatterZephyr", "contextWindow": 8192, "systemAsUser": False},
                    "THUDM/agentlm-13b": {"formatter": "AFormatterLLAMA2", "contextWindow": 4096, "systemAsUser": False},
                    "microsoft/Orca-2-13b": {"formatter": "AFormatterChatML", "contextWindow": 4096, "systemAsUser": False},
                    "01-ai/Yi-34B-Chat": {"formatter": "AFormatterChatML", "contextWindow": 32000, "systemAsUser": False},
                    "mistralai/Mixtral-8x7B-Instruct-v0.1": {"formatter": "AFormatterSimple", "contextWindow": 32000, "systemAsUser": False},
                    "ehartford/dolphin-2.5-mixtral-8x7b": {"formatter": "AFormatterChatML", "contextWindow": 16000, "systemAsUser": False},
                    "openchat/openchat_3.5": {"formatter": "AFormatterOpenChat", "contextWindow": 8192, "systemAsUser": False},
                    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO": {"formatter": "AFormatterChatML", "contextWindow": 32000, "systemAsUser": False},
                },
            },
            "peft": {
                "modelWrapper": "AModelLLAMA",
                "modelList": {
                    #"model/": {"formatter": "AFormatterChatML", "contextWindow": 8192, "systemAsUser": False}
                }
            },
            "oai": {"modelWrapper": "AModelChatGPT",
                    "apikey": None,
                    "baseURL": None,
                    "modelList": {
                        "gpt-4-0125-preview": {"contextWindow": 128000, "systemAsUser": False},
                        "gpt-4-turbo-preview": {"contextWindow": 128000, "systemAsUser": False},
                        "gpt-4-1106-preview": {"contextWindow": 128000, "systemAsUser": False},
                        "gpt-4-vision-preview": {"contextWindow": 128000, "systemAsUser": False},
                        "gpt-4": {"contextWindow": 8192, "systemAsUser": False},
                        "gpt-4-32k": {"contextWindow": 32768, "systemAsUser": False},
                        "gpt-4-0613": {"contextWindow": 8192, "systemAsUser": False},
                        "gpt-4-32k-0613": {"contextWindow": 32768, "systemAsUser": False},
                        "gpt-4-0314": {"contextWindow": 8192, "systemAsUser": False},
                        "gpt-4-32k-0314": {"contextWindow": 32768, "systemAsUser": False},
                        "gpt-3.5-turbo-1106": {"contextWindow": 16385, "systemAsUser": False},
                        "gpt-3.5-turbo": {"contextWindow": 4096, "systemAsUser": False},
                        "gpt-3.5-turbo-16k": {"contextWindow": 16385, "systemAsUser": False},
                        "gpt-3.5-turbo-instruct": {"contextWindow": 4096, "systemAsUser": False}
                        }},
        }
        self.temperature = 0.0
        self.flashAttention2 = False
        self.speechOn = False
        self.contextWindowRatio = 0.6
        if 'nt' == os.name:
            self.services = {
                "storage": {"cmd": "python -m ailice.modules.AStorageChroma --addr=tcp://127.0.0.1:59001", "addr": "tcp://127.0.0.1:59001"},
                "browser": {"cmd": "python -m ailice.modules.ABrowser --addr=tcp://127.0.0.1:59002", "addr": "tcp://127.0.0.1:59002"},
                "arxiv": {"cmd": "python -m ailice.modules.AArxiv --addr=tcp://127.0.0.1:59003", "addr": "tcp://127.0.0.1:59003"},
                "google": {"cmd": "python -m ailice.modules.AGoogle --addr=tcp://127.0.0.1:59004", "addr": "tcp://127.0.0.1:59004"},
                "duckduckgo": {"cmd": "python -m ailice.modules.ADuckDuckGo --addr=tcp://127.0.0.1:59005", "addr": "tcp://127.0.0.1:59005"},
                "scripter": {"cmd": "python -m ailice.modules.AScripter --addr=tcp://127.0.0.1:59000", "addr": "tcp://127.0.0.1:59000"},
                "speech": {"cmd": "python -m ailice.modules.ASpeech --addr=tcp://127.0.0.1:59006", "addr": "tcp://127.0.0.1:59006"},
            }
        else:
            self.services = {
                "storage": {"cmd": "python3 -m ailice.modules.AStorageChroma --addr=ipc:///tmp/AIliceStorage.ipc", "addr": "ipc:///tmp/AIliceStorage.ipc"},
                "browser": {"cmd": "python3 -m ailice.modules.ABrowser --addr=ipc:///tmp/ABrowser.ipc", "addr": "ipc:///tmp/ABrowser.ipc"},
                "arxiv": {"cmd": "python3 -m ailice.modules.AArxiv --addr=ipc:///tmp/AArxiv.ipc", "addr": "ipc:///tmp/AArxiv.ipc"},
                "google": {"cmd": "python3 -m ailice.modules.AGoogle --addr=ipc:///tmp/AGoogle.ipc", "addr": "ipc:///tmp/AGoogle.ipc"},
                "duckduckgo": {"cmd": "python3 -m ailice.modules.ADuckDuckGo --addr=ipc:///tmp/ADuckDuckGo.ipc", "addr": "ipc:///tmp/ADuckDuckGo.ipc"},
                "scripter": {"cmd": "python3 -m ailice.modules.AScripter --addr=tcp://127.0.0.1:59000", "addr": "tcp://127.0.0.1:59000"},
                "speech": {"cmd": "python3 -m ailice.modules.ASpeech --addr=ipc:///tmp/ASpeech.ipc", "addr": "ipc:///tmp/ASpeech.ipc"},
            }
        return

    def Initialize(self, needOpenaiGPTKey = False):
        configFile = appdirs.user_config_dir("ailice", "Steven Lu")
        try:
            os.makedirs(configFile)
        except OSError as e:
            pass
        configFile += "/config.json"
        
        oldDict = self.Load(configFile)
        needUpdate = (set(oldDict.keys()) != set(self.__dict__))
        self.__dict__ = {k: oldDict[k] if k in oldDict else v for k,v in self.__dict__.items()}
        
        needUpdate = needUpdate or (needOpenaiGPTKey and (self.models["oai"]["apikey"] is None))
        
        if needUpdate:
            print("config.json need to be updated.")
            print(colored("********************** Initialize *****************************", "yellow"))
            if self.models["oai"]["apikey"] is None:
                key = input(colored("Your openai chatgpt key (press Enter if not): ", "green"))
                self.models["oai"]["apikey"] = key if 1 < len(key) else None
            self.Store(configFile)
            print(colored("********************** End of Initialization *****************************", "yellow"))
        print(f"config.json is located at {configFile}")
        return

    def Load(self, configFile: str) -> dict:
        if os.path.exists(configFile):
            with open(configFile, "r") as f:
                return json.load(f)
        else:
            return dict()
    
    def Store(self, configFile: str):
        with open(configFile, "w") as f:
            json.dump(self.__dict__, f, indent=2)
        return
    
    
config = AConfig()