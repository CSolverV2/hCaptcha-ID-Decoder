import sys
import os
import requests
import jsbeautifier
from javascript import require
from utils.logger import Logger
import os
import sys

def suppress(func):
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w') 
        result = func(*args, **kwargs)
        sys.stdout.close() 
        sys.stdout = original_stdout
        return result
    return wrapper

log = Logger("CSolver")

class Translator:
    def __init__(self, version: str):
        self.v = version
        self.jsdom = require('jsdom')
        self.evaluate = require("vm").Script
        self.vm = self.jsdom.JSDOM("<title></title>", {"runScripts": "dangerously", "pretendToBeVisual": True}).getInternalVMContext()
        
    @suppress # shows some jsdom errs for me, but still works, so I wrote a suppression function
    def runner(self, _id: str) -> int:
        hsw = self.hsw()
        self.evaluate(hsw).runInContext(self.vm)
        event_id = self.evaluate(f"convert('{_id}')").runInContext(self.vm)
        return event_id
    
    def extract(self, _id: str) -> int:
        # might make it collect/convert all the events dynamically if i got time 
        __id = self.runner(_id)
        log.info(f"Got Event ID -> {_id} -> {__id}")
        return __id
    
    def hsw(self) -> None:
        if os.path.exists(f"./archive/{self.v}.js"):
            return open(f"./archive/{self.v}.js", 'r', encoding='utf-8').read()
        else:
            return self.modify()

    def modify(self) -> None:
        hsw = requests.get(f"https://newassets.hcaptcha.com/c/{self.v}/hsw.js").text
        hsw = hsw.replace("var hsw=", "let translate = []; var hsw=")

        func = hsw.split("{a:A,b:Q,cnt:1,dtor:3},")[1].split("=")[0]
        hsw = hsw.replace(f'++;try{{', f"++;translate.push({func});try{{")
        
        hsw = f"""
        {hsw} 
        hsw("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmIjowLCJzIjoyLCJ0IjoidyIsImQiOiJPNGR1R1R2MmczRlgvcTA4czNWeXI5cVl6N0hwVG1hTWlFWXZEa1VEVU9WcVE5ME9zMVJUMU1hUU5zMEV4UTJrRk5YRXpyWis2MDVsY0pSVllFNFpWNTFVM1FVK3RkcEVaZmZDZFpVT00xTWNWT2tnK01nSmVjNnhGcWplN2JReVRiR3lXZVJvNEFCL2dNVy9DT0U0VnF4bFVRb2pxL05la3E1N2tISGpKdXRGV1pRRHAxcms1UlQ0ZXJyKzMrTUlqdTZTeE1ZeEFJbjVZeEh1dWVoM2sydFF0Y09vSnR6cnAyZUxKWjduVlRkZVh1QmlHc2J4U2pZMkZWYlFrdjA9ZGVCKzZhU0ZEYW9uSlNDYyIsImwiOiIvYy82YjEyM2RjOWUwYjA5YmM5NmU5YmZlNDk5MGFmZGVlNWI3MWRjZWJjMjFjMjliZDBlY2JiYmU3ZDU4MDNiY2U4IiwiaSI6InNoYTI1Ni1BZUhGZHJSNnRuazhkWXNHV0hBOUUxa1RXTkt6VC9LWU1GM0VVYWk3U2VzPSIsImUiOjE3MzQ1MDI1NjYsIm4iOiJoc3ciLCJjIjoxMDAwfQ.qqUfdGA8oEERUKacs3wnaO9o_q7n6RwVcpMoPlUtk50")
        function convert(data) {{
            return translate[0](data)[0];
        }}
        """
        
        with open(f"./archive/{self.v}.js", 'w', encoding='utf-8') as f:
            f.write(jsbeautifier.beautify(hsw))
            
        return hsw

translator = Translator("6b123dc9e0b09bc96e9bfe4990afdee5b71dcebc21c29bd0ecbbbe7d5803bce8") # set to the version you want the event id for
translator.extract("14k") # Set the input to the encoded event id you want to decode 
