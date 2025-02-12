import streamlit as st
import graphviz

def generate_graphviz_code(table_input, layout):
    rows = table_input.strip().split('\n')
    graphviz_code = f"digraph G {{\n  rankdir={layout};\n"

    for row in rows:
        content, predecessors, shape = row.split(',')
        shape = 'ellipse' if shape.strip().lower() == 'ellipse' else 'box'
        graphviz_code += f'  {content} [label="{content}", shape={shape}];\n'
        if predecessors:
            for predecessor in predecessors.split():
                graphviz_code += f'  {predecessor} -> {content};\n'

    graphviz_code += "}"
    return graphviz_code

def main():
    st.title("Graphviz Graph Generator")

    table_input = st.text_area("Table Input (CSV format):", height=200, placeholder="content,predecessors,format")
    layout = st.selectbox("Layout (TB or LR):", ["TB", "LR"])

    if st.button("Generate Graph"):
        graphviz_code = generate_graphviz_code(table_input, layout)
        graph = graphviz.Source(graphviz_code)
        st.graphviz_chart(graph)

if __name__ == "__main__":
    main()
