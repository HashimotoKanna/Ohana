def cleanup_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


def get_syntax_error(e):
    if e.text is None:
        return f"```py\n{e.__class__.__name__}: {e}\n```"
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


def mention_to_user_id(mention):
    user_id = mention.strip("<@").strip(">")
    if user_id.find("!") != -1:
        user_id = user_id.strip("!")
    return int(user_id)
