# # These tools are for creating matrices with the annotation tags added automatically

def example_matrix_tooltips():
    # For generating the latex for t_{in \rightarrow out} matrix
    s = ''
    for row in range(4):
        for column in range(4):
            c, r = f'{column:02b}', f'{row:02b}'
            s += f'\\class{{t_amp_{c}_{r}}}{{t_{{{c}\\to {r}}}}} & '
        s = s[:-2]
        s += '\\\\\n'
    print(s)


def example_matrix_metadata():
    # For generating the metadata for t_{in \rightarrow out} matrix
    msg = """
        "t_amp_{c}_{r}": {{
          "meaning": "This is the amplitude of this operation transforming the state <code>{c}</code> to <code>{r}</code>."
        }},
    """
    s = ''
    for row in range(4):
        for column in range(4):
            c, r = f'{column:02b}', f'{row:02b}'
            s += msg.format(c=c, r=r)
    s = s[:-2]
    print(s)


def matrix_tooltips(gate):
    # For making latex w/ tooltips from a matrix
    s = ''
    size = len(gate[0])
    for row in range(size):
        for column in range(size):
            c, r = f'{column:02b}', f'{row:02b}'
            s += f'\\class{{t_amp_{c}_{r}}}{{{gate[row][column]}}} & '
        s = s[:-2]
        s += '\\\\\n'
    print(s)
