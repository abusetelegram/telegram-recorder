# 使用说明

## 使用前
- 请先补全 `data.py` 内客户端ID和Hash
- 依赖包：`pip3 install telethon`

## 工具说明
- `login.py` 用于登陆
- `list.py` 用于获取当前账号所有聊天记录的 ID  
    - 然后就可以补全监控列表了，可以填入多个，用逗号隔开。填入对应ID即可
    - `fwd_channel` 是目的地，超级群或者频道ID均可
- `main.py` 跑起来！

前台运行，用个screen套住就好

## 几个注意事项

- `fwd_channel`虽然是个数组，但是默认只会用到第一个进行转发，如果你需要多个转发，请自行修改`main.py`内`destination`
- `mtype` 用于控制发送消息的具体信息程度，如果想要显示全部请改为`all`