
import gradio as gr
from http import HTTPStatus
import dashscope
from dashscope.api_entities.dashscope_response import Role
import random
import os

dashscope.api_key = "XXX"


def tongyi_chat(input, history):
    
    msgs = [{'role': Role.SYSTEM, 'content':'You are a helpful assistant.'}]

    for human, ai in history:
        msgs.append({'role': Role.USER, 'content': human})
        msgs.append({'role': Role.ASSISTANT, 'content': ai})

    msgs.append({'role': Role.USER, 'content': input})

    responses = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_max,
        messages = msgs,
        seed = random.randint(1,10000),
        result_format = "message",
        stream = True
    )

    full_content = ''
    for resp in responses:
        result = resp.output.choices[0]
        if resp.status_code == HTTPStatus.OK:
            full_content += result['message']['content']
            yield result['message']['content']
        else:
            return f'Error when request, status code {resp.status_code}'

demo = gr.ChatInterface(
        tongyi_chat,
        submit_btn = "提交",
        retry_btn = "重试",
        clear_btn = "清除",
        undo_btn = "撤回",
    )

demo.launch()