import streamlit as st
import graphviz
import pandas as pd

def generate_graphviz_code(table_input, layout):
    graphviz_code = f"digraph G {{\n  rankdir={layout};\n"

    for index, row in table_input.iterrows():
        content = row['ID']
        description = row['Description']
        predecessors = row['Predecessor ID']
        shape = 'ellipse' if row['Format'].strip().lower() == 'ellipse' else 'box'
        graphviz_code += f'  {content} [label="{description}", shape={shape}];\n'
        if predecessors:
            for predecessor in predecessors.split():
                graphviz_code += f'  {predecessor} -> {content};\n'

    graphviz_code += "}"
    return graphviz_code

def main():
    st.title("Graphviz Graph Generator")

    # Create a table input widget using Streamlit's editable dataframe
    table_input = st.data_editor(
        pd.DataFrame(columns=['ID', 'Description', 'Predecessor ID', 'Format']),
        num_rows="dynamic",
        key="table_input"
    )

    layout = st.selectbox("Layout (TB or LR):", ["TB", "LR"])

    if st.button("Generate Graph"):
        if not table_input.empty:
            graphviz_code = generate_graphviz_code(table_input, layout)
            graph = graphviz.Source(graphviz_code)
            st.graphviz_chart(graph)
        else:
            st.warning("Please enter data in the table.")

if __name__ == "__main__":
    main()
