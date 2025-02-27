def parse_emoji_data(data):
    out_ALL = "var ALL = ["
    out_ALL_KEYWORDS = "var ALL_KEYWORDS = ["

    ignored_groups = ["Component"]
    ignore_group = False
    first_group = True
    first_subgroup = True
    first_emoji_type = True
    for line in data.split('\n'):
        if "# group:" in line:
            tmp = line.split(':')
            group_name = tmp[1].strip()
            if not first_emoji_type:
                out_ALL += "],"
                out_ALL_KEYWORDS += "],"
                first_emoji_type = True

            if not first_group and not ignore_group:
                out_ALL += "]],"
                out_ALL_KEYWORDS += "]],"
                first_subgroup = True

            if group_name in ignored_groups:
                ignore_group = True
            else:
                ignore_group = False
            if not ignore_group:
                out_ALL += "\""+group_name+"\":["
                out_ALL_KEYWORDS += "\""+group_name+"\":["
                first_group = False
            
        
        if ignore_group:
            continue

        if "# subgroup:" in line:
            if not first_emoji_type:
                out_ALL += "],"
                out_ALL_KEYWORDS += "],"
                first_emoji_type = True
            if not first_subgroup:
                out_ALL += "],"
                out_ALL_KEYWORDS += "],"
            if not first_emoji_type:
                out_ALL += "],"
                out_ALL_KEYWORDS += "],"
            out_ALL += "["
            out_ALL_KEYWORDS += "["
            first_subgroup = False
        if ('fully-qualified' in line) and line[0] != '#':
            x = line.split('#', 1)[1].strip().split(' ')
            emoji = x[0]
            x = x[2:]
            keyword = ' '.join(x)

            # print(emoji)
            # print(keyword)

            
            if not first_emoji_type and ':' not in keyword:
                out_ALL += "],["
                out_ALL_KEYWORDS += "],["

            if first_emoji_type:
                first_emoji_type = False
                out_ALL += "["
                out_ALL_KEYWORDS += "["
            if not first_emoji_type and ':' in keyword:
                out_ALL += ","
                out_ALL_KEYWORDS += ","
            
            out_ALL += "'" + emoji + "'"
            out_ALL_KEYWORDS += '["' + keyword + '"],'
    out_ALL += ']]]'
    out_ALL_KEYWORDS += ']]]'
    return out_ALL, out_ALL_KEYWORDS

def main():
    with open('data.txt', 'r') as file:
        input_data = file.read()
    emojis, keywords = parse_emoji_data(input_data)
    with open('emojis.js', 'w') as emoji_file:
        emoji_file.write(emojis)
    
    with open('keywords.js', 'w') as keyword_file:
        keyword_file.write(keywords)
    print("done")

if __name__ == "__main__":
    main()
