actor_map = {
    'user': 'user',
    'ai': 'assistant',
    'assistant': 'assistant',
    'sys': 'system',
    'system': 'system'
}

def parse_messages(msg: str):
    lines = msg.strip().splitlines()
    current_actor = "user"

    out = []
    curr_text = []

    def flush():
        if len(curr_text) > 0:
            out.append({'role': current_actor, 'content': '\n'.join(curr_text)})
        curr_text.clear()

    for line in lines:
        if any(f':{_}:' in line for _ in actor_map.keys()):
            parts = line.strip().split(':', maxsplit=2)
            if len(parts[0]) > 0:
                curr_text.append(parts[0].strip())
            abbreviated_actor = parts[1]
            if abbreviated_actor not in actor_map:
                raise RuntimeError(f'Unknown actor {abbreviated_actor}')
            flush()
            current_actor = actor_map[abbreviated_actor]
            if len(parts[2]) > 0:
                curr_text.append(parts[2].strip())
        else:
            curr_text.append(line)
    flush()
    
    return out